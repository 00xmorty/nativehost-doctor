import importlib.machinery
import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / 'nativehost-doctor'
spec = importlib.util.spec_from_loader('nativehost', importlib.machinery.SourceFileLoader('nativehost', str(SOURCE)))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
HOST = 'com.example.host'
ORIGIN = 'chrome-extension://' + 'a' * 32 + '/'


class DoctorTest(unittest.TestCase):
    def test_platform_locations(self):
        self.assertEqual(str(mod.locations('chrome', 'darwin', '/tmp/home')[1]), '/Library/Google/Chrome/NativeMessagingHosts')
        self.assertEqual(str(mod.locations('chromium', 'darwin', '/tmp/home')[1]), '/Library/Application Support/Chromium/NativeMessagingHosts')
        self.assertEqual(str(mod.locations('chrome', 'linux', '/tmp/home')[1]), '/etc/opt/chrome/native-messaging-hosts')
        self.assertEqual(str(mod.locations('chromium', 'linux', '/tmp/home')[1]), '/etc/chromium/native-messaging-hosts')

    def test_manifest_states(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / 'host.json'
            binary = Path(tmp) / 'binary'
            self.assertEqual(mod.inspect_manifest(file, HOST, ORIGIN), 'MISSING')
            data = {'name': HOST, 'type': 'stdio', 'description': 'fixture', 'allowed_origins': [ORIGIN], 'path': str(binary)}
            file.write_text(json.dumps(data))
            self.assertEqual(mod.inspect_manifest(file, HOST, ORIGIN), 'BINARY_OR_MANIFEST_MISSING')
            binary.write_text('#!/bin/sh\nexit 0\n')
            os.chmod(binary, 0o700)
            self.assertEqual(mod.inspect_manifest(file, HOST, ORIGIN), 'PREFLIGHT_OK_NOT_CONNECTION_PROOF')
            data['allowed_origins'] = []
            file.write_text(json.dumps(data))
            self.assertEqual(mod.inspect_manifest(file, HOST, ORIGIN), 'ORIGIN_NOT_ALLOWED')
            data['allowed_origins'] = [ORIGIN]
            data['path'] = 'relative'
            file.write_text(json.dumps(data))
            self.assertEqual(mod.inspect_manifest(file, HOST, ORIGIN), 'INVALID_BINARY_PATH')
            file.write_text('{')
            self.assertEqual(mod.inspect_manifest(file, HOST, ORIGIN), 'INVALID_JSON_SCHEMA')
            file.unlink()
            file.symlink_to(binary)
            self.assertEqual(mod.inspect_manifest(file, HOST, ORIGIN), 'UNSAFE_OR_OVERSIZE')

if __name__ == '__main__':
    unittest.main()
