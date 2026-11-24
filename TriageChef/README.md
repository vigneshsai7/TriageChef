# 🔍 Forensic Triage + CyberChef — Windows & macOS Image Triage

![Workflow](assets/01-workflow.png)

> **Mini-project for SOC / DFIR / CTF.** Triage a Windows **AND** macOS image, document every artefact, decode every suspicious string in **CyberChef**, and generate a clean report.
> **Read-only. No live acquisition. No decryption. No password cracking.**

[![CI](https://github.com/<you>/forensic-triage-cyberchef/actions/workflows/ci.yml/badge.svg)](https://github.com/<you>/forensic-triage-cyberchef/actions)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![OS](https://img.shields.io/badge/OS-Windows%20%7C%20macOS-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📸 What This Project Does

![Windows + macOS Artefacts](assets/02-windows-macos.png)

| OS | What we triage |
|---|---|
| **Windows** | Prefetch, Amcache, Shimcache, SRUM, `.evtx` (4624 / 4625 / 4672 / 4104), Registry (SAM / SYSTEM / SOFTWARE / NTUSER.DAT), RunKeys / Services / Scheduled Tasks, LNK / JumpLists, Browser History, Recycle Bin, MFT / USN |
| **macOS** | Unified Logs (`.tracev3`), Spotlight `store.db`, `fsevents`, LaunchAgents / LaunchDaemons, Login Items, `TCC.db`, `KnowledgeC.db`, QuarantineEventsV2, Safari / Chrome History, `.zsh_history` / `.bash_history` |
| **Both** | Timeline, IOCs (IP / domain / URL / hash / Base64 / hex), MITRE ATT&CK mapping, Severity |

---

## 🗂️ Repo Structure — What Is Where

![Repo Structure](assets/04-folder-structure.png)

```
forensic-triage-cyberchef/
├── README.md                  ← YOU ARE HERE — start here
├── HOW_TO_USE.md              ← Step-by-step, with screenshots / commands
├── WHAT_TO_DO.md              ← What to do with a real case, checklist
├── CONTRIBUTING.md            ← How to contribute
├── setup.sh / setup.bat       ← One-click setup
├── push-to-github.sh          ← One-click deploy to GitHub
├── src/
│   ├── triage.py              ← Main triage engine
│   ├── cyberchef_bridge.py    ← String → CyberChef recipe + URL
│   └── parsers/
│       ├── windows.py         ← Windows artefact checklist
│       ├── macos.py           ← macOS artefact checklist
│       └── common.py          ← MITRE mapping
├── cyberchef/                 ← 9 shareable CyberChef recipes (.json)
│   ├── powershell-base64.json
│   ├── base64-utf8.json
│   ├── hex-to-text.json
│   ├── url-decode.json
│   ├── rot13.json
│   ├── xor-bruteforce.json
│   ├── jwt-decode.json
│   ├── unix-timestamp.json
│   └── magic.json
├── docs/
│   ├── ARTEFACTS.md           ← Full artefact catalogue
│   ├── CYBERCHEF.md           ← CyberChef guide
│   └── SAMPLE-REPORT.md       ← Example report
├── assets/                    ← Images used in this README
├── samples/                   ← Synthetic fixtures (NO real evidence)
├── reports/                   ← YOUR output goes here (git-ignored)
├── tests/
│   ├── generate_fixtures.py
│   └── test_smoke.py
└── .github/workflows/ci.yml   ← CI: tests on every push
```

---

## 🚀 HOW TO USE — Quick Start (2 Minutes)

### Option A: Try Demo (No Evidence Needed) ⭐ Start Here

```bash
# 1. Clone
git clone https://github.com/<you>/forensic-triage-cyberchef.git
cd forensic-triage-cyberchef

# 2. Setup
./setup.sh
# Windows: setup.bat
# Manual: python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt

# 3. Create demo evidence
python tests/generate_fixtures.py --out ./samples

# 4. Run triage
python src/triage.py --input ./samples/windows-triage --os windows --out ./reports/demo-windows
python src/triage.py --input ./samples/macos-triage --os macos --out ./reports/demo-macos

# 5. Open report
cat reports/demo-windows/report.md
# or open reports/demo-windows/report.md in VS Code / GitHub
```

**You will get:**
```
reports/demo-windows/
├── report.md               ← Main report, with CyberChef links
├── timeline.csv            ← Sorted timeline
├── findings.json           ← All findings + recipes
├── iocs.json               ← IPs, domains, URLs, hashes
└── suspicious_strings.txt  ← Paste these into CyberChef
```

### Option B: Triage a Real Image / Export

```bash
# 1. Export artefacts from your image into a folder (DO NOT work on live disk)
#    Use FTK Imager / Arsenal Image Mounter / your lab tool to export.
#    Example layout:
#    ./evidence/
#      Windows/Prefetch/*.pf
#      Windows/System32/winevt/Logs/Security.evtx
#      Users/demo/NTUSER.DAT
#      macOS/Users/demo/Library/LaunchAgents/*.plist

# 2. Run — auto-detect OS
python src/triage.py --input ./evidence --out ./reports/case-001

# 3. Or force OS
python src/triage.py --input ./evidence --os windows --out ./reports/case-001-windows
python src/triage.py --input ./evidence --os macos   --out ./reports/case-001-macos
```

### Option C: CyberChef Only (Decode One String)

```bash
# 1. Open CyberChef
#    Online: https://gchq.github.io/CyberChef/
#    Local (for sensitive data): docker run -p 8080:8000 ghcr.io/gchq/cyberchef

# 2. Load recipe from cyberchef/ folder
#    CyberChef → Save/Load → Load recipe → paste cyberchef/powershell-base64.json

# 3. Paste suspicious string → Copy decoded output → Paste into your report
```

![CyberChef Decode Flow](assets/03-cyberchef.png)

---

## 🧪 CyberChef Recipes — Which One To Use?

| You See This | Use This Recipe | File |
|---|---|---|
| `powershell -enc SQBFA...` | PowerShell Base64 (UTF-16LE) | `powershell-base64.json` |
| `aGVsbG8gd29ybGQ=` | Generic Base64 | `base64-utf8.json` |
| `68656c6c6f...` (hex) | Hex → Text | `hex-to-text.json` |
| `http%3A%2F%2F...` | URL Decode | `url-decode.json` |
| `Uryyb Jbeyq` | ROT13 | `rot13.json` |
| Gibberish after Base64/Hex | XOR Brute Force | `xor-bruteforce.json` |
| `eyJhbGciOi...` (3 parts) | JWT Decode | `jwt-decode.json` |
| `1730000000` | Unix Timestamp | `unix-timestamp.json` |
| **Don't know what it is** | **Magic (auto-detect)** | `magic.json` ⭐ |

> **Rule:** Never paste real victim credentials / PII into online CyberChef. Use Docker local for sensitive cases.

Full guide: [`docs/CYBERCHEF.md`](docs/CYBERCHEF.md)

---

## 📋 WHAT TO DO — After You Run Triage

See full checklist: [`WHAT_TO_DO.md`](WHAT_TO_DO.md)

1. **Open `report.md`** — read findings top to bottom
2. **Open each CyberChef link** in the report — decode, copy output back into findings
3. **Check `timeline.csv`** — what happened first? What happened together?
4. **Check `iocs.json`** — any known-malicious IP / domain? Check VirusTotal (hash only, never upload file)
5. **Map to MITRE** — see `src/parsers/common.py` — e.g. PowerShell = T1059.001, Rundll32 = T1218.011
6. **Verdict each finding:** Benign / Suspicious / Malicious + Severity: Low / Medium / High
7. **Write `docs/findings.md`** (or update report) — Artefact + Path + Timestamp + Raw + Decoded + MITRE + Verdict
8. **Do NOT push real evidence to GitHub** — only push code + synthetic samples + redacted reports

---

## 🌐 Deploy To GitHub — Direct Deploy

### One-Click

```bash
./push-to-github.sh <you>/forensic-triage-cyberchef
# Windows: push-to-github.bat
```

### Manual (Copy-Paste)

```bash
git init
git add .
git commit -m "feat: forensic triage + cyberchef mini-project"
git branch -M main
git remote add origin https://github.com/<you>/forensic-triage-cyberchef.git
git push -u origin main
```

### After Push — Do These 3 Things

1. **GitHub → Settings → Pages** → Deploy from branch → `main` → `/docs` → Save (for demo)
2. **GitHub → About → Edit** → Add description + topics: `dfir forensic triage cyberchef windows macos soc`
3. **GitHub → README** — verify images load (they are in `assets/`)

CI runs automatically on every push: generates fixtures → runs Windows + macOS triage → fails if broken.

---

## 📚 Docs

| Doc | What It Has |
|---|---|
| [`HOW_TO_USE.md`](HOW_TO_USE.md) | Full step-by-step, Windows + macOS + Linux, screenshots, troubleshooting |
| [`WHAT_TO_DO.md`](WHAT_TO_DO.md) | Real-case checklist, how to document a finding, what NOT to do |
| [`docs/ARTEFACTS.md`](docs/ARTEFACTS.md) | Every artefact: location, what it proves, parser, CyberChef recipe |
| [`docs/CYBERCHEF.md`](docs/CYBERCHEF.md) | CyberChef guide, Magic mode, Cocoa timestamps, safety |
| [`docs/SAMPLE-REPORT.md`](docs/SAMPLE-REPORT.md) | Example report format |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to add a new artefact / recipe |

---

## ⚠️ Safety / Ethics

- Triage only, on images you are **authorised** to analyse (lab / CTF / your own / client with consent)
- **Never** upload real victim evidence, PII, credentials, or hashes of real cases to public GitHub
- Use synthetic fixtures in `samples/` for demos / screenshots
- This tool does **not** decrypt, crack passwords, or bypass security

## 🤝 Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) — add a new artefact = 1 entry in `docs/ARTEFACTS.md` + 1 parser line + 1 CyberChef recipe if needed.

## 📄 License

MIT — see [`LICENSE`](LICENSE)
