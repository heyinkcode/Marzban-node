import atexit
import json
import re
import subprocess
import threading
import time
from collections import deque
from contextlib import contextmanager

from config import DEBUG, SSL_CERT_FILE, SSL_KEY_FILE, XRAY_API_HOST, XRAY_API_PORT, INBOUNDS
from logger import logger
from outbound_profiles import apply_managed_outbounds


class XRayConfig(dict):
    """
    Loads Xray config json
    config must contain an inbound with the API_INBOUND tag name which handles API requests
    """

    def __init__(self, config: str, peer_ip: str):
        config = json.loads(config)

        self.api_host = XRAY_API_HOST
        self.api_port = XRAY_API_PORT
        self.ssl_cert = SSL_CERT_FILE
        self.ssl_key = SSL_KEY_FILE
        self.peer_ip = peer_ip

        super().__init__(config)
        # Optional panel extension; stock configs remain unchanged.
        apply_managed_outbounds(self)
        self._apply_api()

    def to_json(self, **json_kwargs):
        return json.dumps(self, **json_kwargs)

    def _apply_api(self):
        for inbound in self.get('inbounds', []).copy():
            if inbound.get('protocol') == 'dokodemo-door' and inbound.get('tag') == 'API_INBOUND':
                self['inbounds'].remove(inbound)
                
            elif INBOUNDS and inbound.get('tag') not in INBOUNDS:
                self['inbounds'].remove(inbound)

        for rule in self.get('routing', {}).get("rules", []):
            api_tag = self.get('api', {}).get('tag')
            if api_tag and rule.get('outboundTag') == api_tag:
                self['routing']['rules'].remove(rule)

        self["api"] = {
            "services": [
                "HandlerService",
                "StatsService",
                "LoggerService"
            ],
            "tag": "API"
        }
        self["stats"] = {}
        # The fixed core supports GetAllOnlineUsers. Enable the corresponding
        # policy per configured level while retaining every existing setting.
        levels = self.setdefault("policy", {}).setdefault("levels", {})
        levels.setdefault("0", {})
        for configured_inbound in self.get("inbounds", []):
            for client in configured_inbound.get("settings", {}).get("clients", []):
                levels.setdefault(str(client.get("level", 0)), {})
        for level in levels.values():
            level["statsUserOnline"] = True
        inbound = {
            "listen": self.api_host,
            "port": self.api_port,
            "protocol": "dokodemo-door",
            "settings": {
                "address": "127.0.0.1"
            },
            "streamSettings": {
                "security": "tls",
                "tlsSettings": {
                    "certificates": [
                        {
                            "certificateFile": self.ssl_cert,
                            "keyFile": self.ssl_key
                        }
                    ]
                }
            },
            "tag": "API_INBOUND"
        }
        try:
            self["inbounds"].insert(0, inbound)
        except KeyError:
            self["inbounds"] = []
            self["inbounds"].insert(0, inbound)

        rule = {
            "inboundTag": [
                "API_INBOUND"
            ],
            "source": [
                "127.0.0.1",
                self.peer_ip
            ],
            "outboundTag": "API",
            "type": "field"
        }
        try:
            self["routing"]["rules"].insert(0, rule)
        except KeyError:
            self["routing"] = {"rules": []}
            self["routing"]["rules"].insert(0, rule)


class XRayCore:
    def __init__(self,
                 executable_path: str = "/usr/bin/xray",
                 assets_path: str = "/usr/share/xray"):
        self.executable_path = executable_path
        self.assets_path = assets_path

        self.version = self.get_version()
        self.process = None
        self._last_config = None
        self._logs_thread = None
        self.restarting = False
        self._restart_lock = threading.Lock()

        self._logs_buffer = deque(maxlen=100)
        self._temp_log_buffers = {}
        self._on_start_funcs = []
        self._on_stop_funcs = []
        self._env = {
            "XRAY_LOCATION_ASSET": assets_path
        }

        atexit.register(self.stop)

    def get_version(self):
        cmd = [self.executable_path, "version"]
        output = subprocess.check_output(
            cmd, stderr=subprocess.STDOUT).decode('utf-8')
        m = re.match(r'^Xray (\d+\.\d+\.\d+)', output)
        if m:
            return m.groups()[0]

    def validate_config(self, config: XRayConfig):
        """Reject an invalid replacement before stopping the working core."""
        try:
            result = subprocess.run(
                [self.executable_path, "run", "-test", "-config", "stdin:"],
                input=config.to_json(), text=True, capture_output=True,
                env=self._env, timeout=15, check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise RuntimeError("Xray configuration preflight could not complete") from exc
        if result.returncode != 0:
            # Xray diagnostics can include credential-bearing config fragments.
            raise RuntimeError("Xray configuration preflight failed; current core was not changed")

    def __capture_process_logs(self):
        # A reader belongs to one process generation, never a replacement.
        process = self.process
        def capture_and_debug_log():
            while process:
                output = process.stdout.readline()
                if output:
                    output = output.strip()
                    self._logs_buffer.append(output)
                    for buf in list(self._temp_log_buffers.values()):
                        buf.append(output)
                    logger.debug(output)

                elif process.poll() is not None:
                    break

        def capture_only():
            while process:
                output = process.stdout.readline()
                if output:
                    output = output.strip()
                    self._logs_buffer.append(output)
                    for buf in list(self._temp_log_buffers.values()):
                        buf.append(output)

                elif process.poll() is not None:
                    break

        self._logs_thread = threading.Thread(target=capture_and_debug_log if DEBUG else capture_only, daemon=True)
        self._logs_thread.start()

    @contextmanager
    def get_logs(self):
        buf = deque(self._logs_buffer, maxlen=100)
        buf_id = id(buf)
        try:
            self._temp_log_buffers[buf_id] = buf
            yield buf
        except (EOFError, TimeoutError):
            pass
        finally:
            del self._temp_log_buffers[buf_id]
            del buf

    @property
    def started(self):
        if not self.process:
            return False

        if self.process.poll() is None:
            return True

        return False

    def start(self, config: XRayConfig, prevalidated: bool = False):
        if self.started is True:
            raise RuntimeError("Xray is started already")

        if not prevalidated:
            self.validate_config(config)

        if config.get('log', {}).get('logLevel') in ('none', 'error'):
            config['log']['logLevel'] = 'warning'

        cmd = [
            self.executable_path,
            "run",
            '-config',
            'stdin:'
        ]
        self.process = subprocess.Popen(
            cmd,
            env=self._env,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True
        )
        self.process.stdin.write(config.to_json())
        self.process.stdin.flush()
        self.process.stdin.close()
        self._last_config = config

        self.__capture_process_logs()

        # execute on start functions
        for func in self._on_start_funcs:
            threading.Thread(target=func).start()

    def stop(self):
        process = self.process
        if process is None:
            return
        running = process.poll() is None
        if running:
            process.terminate()
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=3)
        else:
            process.wait(timeout=3)
        self.process = None
        reader = getattr(self, "_logs_thread", None)
        if reader is not None and reader is not threading.current_thread():
            reader.join(timeout=2)
        for stream in (process.stdin, process.stdout, process.stderr):
            if stream is not None:
                stream.close()
        if not running:
            return
        logger.warning("Xray core stopped")

        # execute on stop functions
        for func in self._on_stop_funcs:
            threading.Thread(target=func).start()

    def restart(self, config: XRayConfig):
        if self.restarting is True:
            raise RuntimeError("XRAY_RESTART_BUSY")

        lock = getattr(self, "_restart_lock", None)
        if lock is None:
            lock = self._restart_lock = threading.Lock()
        if not lock.acquire(blocking=False):
            raise RuntimeError("XRAY_RESTART_BUSY")

        self.restarting = True
        previous = getattr(self, "_last_config", None)
        try:
            self.validate_config(config)
            logger.warning("Restarting Xray core...")
            self.stop()
            try:
                self.start(config, prevalidated=True)
                time.sleep(0.3)
                if not self.started:
                    raise RuntimeError("Replacement core exited")
            except Exception as exc:
                if previous is not None:
                    try:
                        self.stop()
                        self.start(previous, prevalidated=True)
                        time.sleep(0.3)
                        if not self.started:
                            raise RuntimeError("Previous core exited")
                    except Exception:
                        raise RuntimeError("XRAY_RESTART_FAILED_ROLLBACK_FAILED") from None
                    raise RuntimeError("XRAY_RESTART_FAILED_ROLLED_BACK") from None
                raise RuntimeError("XRAY_RESTART_FAILED_NO_PREVIOUS_CONFIG") from None
        finally:
            self.restarting = False
            lock.release()

    def on_start(self, func: callable):
        self._on_start_funcs.append(func)
        return func

    def on_stop(self, func: callable):
        self._on_stop_funcs.append(func)
        return func
