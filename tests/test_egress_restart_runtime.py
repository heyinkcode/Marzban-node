"""Real pinned-core preflight and startup rollback, loopback only."""
import json
import os
import socket
import time
import unittest
from pathlib import Path
from test_xray_preflight import XRayCore


class Config(dict):
    def to_json(self): return json.dumps(self)


@unittest.skipUnless(os.environ.get('XRAY_TEST_BINARY'),'explicit pinned core required')
class EgressRestartRuntimeTests(unittest.TestCase):
    def setUp(self):
        binary=os.environ['XRAY_TEST_BINARY']
        self.core=XRayCore(binary,str(Path(binary).parent)); self.addCleanup(self.core.stop)
        # Production Node runs on Linux; Windows Go runtime additionally needs
        # its OS directory when exercising that same minimal child environment.
        if os.name == 'nt': self.core._env['SystemRoot']=os.environ['SystemRoot']
        with socket.socket() as sock:
            sock.bind(('127.0.0.1',0)); self.port=sock.getsockname()[1]
        self.config=Config(inbounds=[{'listen':'127.0.0.1','port':self.port,'protocol':'socks','settings':{'auth':'noauth'}}],outbounds=[{'protocol':'freedom'}])
        self.core.start(self.config); self.wait_ready()

    def wait_ready(self):
        deadline=time.monotonic()+4
        while time.monotonic()<deadline:
            try:
                with socket.create_connection(('127.0.0.1',self.port),timeout=.2): return
            except OSError:time.sleep(.05)
        code=self.core.process.poll()
        diagnostic=self.core.process.stderr.read() if code is not None else list(self.core._logs_buffer)
        self.fail(f'Previous core listener not ready: process={code}; {diagnostic}')

    def test_real_invalid_config_does_not_stop_existing_process(self):
        pid=self.core.process.pid
        with self.assertRaisesRegex(RuntimeError,'preflight failed'):
            self.core.restart(Config(inbounds=[{'protocol':'unknown-invalid-protocol'}]))
        self.assertEqual(self.core.process.pid,pid);self.wait_ready()

    def test_real_bind_failure_restores_previous_core_listener(self):
        with socket.socket() as occupied:
            occupied.bind(('127.0.0.1',0)); occupied.listen()
            candidate=Config(inbounds=[{'listen':'127.0.0.1','port':occupied.getsockname()[1],'protocol':'socks','settings':{'auth':'noauth'}}],outbounds=[{'protocol':'freedom'}])
            with self.assertRaisesRegex(RuntimeError,'FAILED_ROLLED_BACK'):
                self.core.restart(candidate)
        self.wait_ready();self.assertTrue(self.core.started)
