import subprocess
import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import Mock, patch


config = types.ModuleType("config")
for name, value in {
    "DEBUG": False, "SSL_CERT_FILE": "/tmp/cert", "SSL_KEY_FILE": "/tmp/key",
    "XRAY_API_HOST": "127.0.0.1", "XRAY_API_PORT": 62051, "INBOUNDS": [],
}.items():
    setattr(config, name, value)
logger = types.ModuleType("logger")
logger.logger = Mock()
with patch.dict(sys.modules, {"config": config, "logger": logger}):
    spec = importlib.util.spec_from_file_location(
        "xray_preflight_test_module", Path(__file__).resolve().parents[1] / "xray.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
XRayCore = module.XRayCore


class XRayPreflightTests(unittest.TestCase):
    def setUp(self):
        self.core = object.__new__(XRayCore)
        self.core.executable_path = "/usr/bin/xray"
        self.core._env = {"XRAY_LOCATION_ASSET": "/usr/share/xray"}
        self.core.restarting = False
        self.config = Mock()
        self.config.to_json.return_value = '{"outbounds":[]}'

    @patch.object(module.subprocess, "run")
    def test_validation_uses_core_test_mode(self, run):
        run.return_value.returncode = 0
        self.core.validate_config(self.config)
        args, kwargs = run.call_args
        self.assertEqual(args[0], ["/usr/bin/xray", "run", "-test", "-config", "stdin:"])
        self.assertEqual(kwargs["input"], self.config.to_json.return_value)

    @patch.object(module.subprocess, "run")
    def test_validation_failure_does_not_expose_core_diagnostic(self, run):
        run.return_value.returncode = 1
        run.return_value.stderr = "secret-password"
        with self.assertRaisesRegex(RuntimeError, "preflight failed") as error:
            self.core.validate_config(self.config)
        self.assertNotIn("secret-password", str(error.exception))

    @patch.object(module.subprocess, "run", side_effect=subprocess.TimeoutExpired("xray", 15))
    def test_timeout_is_reported_without_config(self, _run):
        with self.assertRaisesRegex(RuntimeError, "could not complete"):
            self.core.validate_config(self.config)

    def test_restart_keeps_running_core_when_validation_fails(self):
        self.core.validate_config = Mock(side_effect=RuntimeError("invalid"))
        self.core.stop = Mock()
        self.core.start = Mock()
        with self.assertRaisesRegex(RuntimeError, "invalid"):
            self.core.restart(self.config)
        self.core.stop.assert_not_called()
        self.core.start.assert_not_called()
        self.assertFalse(self.core.restarting)

    def test_failed_start_restores_last_running_configuration(self):
        previous=Mock(); self.core._last_config=previous
        self.core.validate_config=Mock(); self.core.stop=Mock()
        self.core.process=Mock(); self.core.process.poll.return_value=0
        def start(config,prevalidated):
            self.core.process.poll.return_value=0 if config is self.config else None
        self.core.start=Mock(side_effect=start)
        with patch.object(module.time,"sleep"),self.assertRaisesRegex(RuntimeError,"FAILED_ROLLED_BACK"):
            self.core.restart(self.config)
        self.assertEqual(self.core.start.call_args_list[-1].args,(previous,))
        self.assertFalse(self.core.restarting)

    def test_failed_rollback_is_not_reported_as_restored(self):
        self.core._last_config=Mock(); self.core.validate_config=Mock(); self.core.stop=Mock()
        self.core.start=Mock(side_effect=RuntimeError("secret-password"))
        with self.assertRaisesRegex(RuntimeError,"ROLLBACK_FAILED") as error:
            self.core.restart(self.config)
        self.assertNotIn("secret-password",str(error.exception)); self.assertFalse(self.core.restarting)

    def test_parallel_restart_is_not_acknowledged_as_success(self):
        self.core.restarting=True
        with self.assertRaisesRegex(RuntimeError,"RESTART_BUSY"):
            self.core.restart(self.config)


if __name__ == "__main__":
    unittest.main()
