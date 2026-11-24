# CyberChef Guide for This Project

## Online vs Self-hosted
- Online: https://gchq.github.io/CyberChef/
- Self-host: `docker run -p 8080:8000 ghcr.io/gchq/cyberchef` — use for sensitive evidence, never paste real secrets to online tools.

## Magic Mode
For unknown blobs: use `magic.json` recipe. It auto-detects Base64/Hex/ROT13/XOR etc. Set depth 3.

## Common Triage Flows
1. **PowerShell `-EncodedCommand`**: `powershell-base64.json` — output is UTF-16LE, look for `IEX`, `DownloadString`, C2 domain.
2. **Hex / XOR payload**: `hex-to-text` then `xor-bruteforce` if still gibberish.
3. **URL / Quarantine**: `url-decode` repeatedly until readable.
4. **Timestamps**: macOS Cocoa Core Data = seconds since 2001-01-01. Convert: Unix = Cocoa + 978307200. Use `unix-timestamp` after adding offset.
5. **JWT / tokens**: `jwt-decode` — check `exp`, `iss`, scopes.

## Rules
- Never paste real victim credentials / PII into online CyberChef.
- Save every decode: recipe name + input hash + output in `report.md`.
- If Magic fails, try manual chain: From Hex -> XOR Brute -> From Base64 -> Decode text.
