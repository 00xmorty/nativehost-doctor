# NativeHost Doctor

Offline, read-only Chrome/Chromium native-messaging manifest preflight for macOS and Linux. Checks a named host against a supplied extension ID; reports only categorical results, not local paths or raw manifest values.

## Run

Requires Python 3.9+ (standard library only). Download the single-file asset from Releases, then:

```sh
python3 nativehost-doctor --host com.example.host --extension-id aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

Replace both sample values with your own host name and 32-character extension ID. Use `--browser chromium` for Chromium. To run tests from a source checkout: `python3 -m unittest discover -s tests -v`.

## Safety and limitations

No sudo, network, telemetry, file writes, permission changes or host execution. The tool reads only the two known manifest locations for the selected browser and uses metadata to check the referenced executable. It will not enumerate other hosts or detect conflicts with differently named manifests. Symlinked manifests are rejected. Some browser distributions use different paths; Firefox/Brave/Edge are unsupported. A successful preflight is **not** proof of a working browser-to-host connection, valid browser policy, actual runtime permissions or crash-free execution. Missing access is reported as UNKNOWN/UNREADABLE, not as absent. Do not publish raw manifests, extension logs or machine paths.

Report a bug with synthetic or redacted fixture data only; see SECURITY.md.
