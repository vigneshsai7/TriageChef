# Artefacts Catalogue

## Windows
| Artefact | Location | Proves | CyberChef Recipe |
|---|---|---|---|
| Prefetch | `Windows/Prefetch/*.pf` | Program executed, when, how often | - |
| Amcache | `Windows/AppCompat/Programs/Amcache.hve` | First run, SHA1, path | hex-to-text |
| Shimcache | `SYSTEM` hive | Executables loaded, even if deleted | - |
| SRUM | `Windows/System32/sru/SRUDB.dat` | App network + energy use | - |
| Security.evtx | `Windows/System32/winevt/Logs/` | Logon 4624/4625, 4672 admin | - |
| PowerShell Operational | Same | 4103/4104 script blocks | powershell-base64 |
| RunKeys / Services / Tasks | Registry + `Tasks/` | Persistence | base64-utf8 |
| LNK / JumpLists | `Recent/*.lnk`, `AutomaticDestinations/` | Files opened | - |
| Browser History | `WebCacheV01.dat`, Chrome History | URLs, downloads | url-decode |
| Recycle Bin | `$Recycle.Bin/$I*` | Deleted files | - |

## macOS
| Artefact | Location | Proves | CyberChef Recipe |
|---|---|---|---|
| Unified Logs | `private/var/db/diagnostics/*.tracev3` | Process, errors, logins | - |
| Spotlight | `.Spotlight-V100/store.db` | Files existed, even if deleted | - |
| fsevents | `.fseventsd/` | File create/modify/delete timeline | unix-timestamp |
| LaunchAgents/Daemons | `~/Library/LaunchAgents`, `/Library/LaunchDaemons` | Persistence | - |
| TCC.db | `~/Library/Application Support/com.apple.TCC/TCC.db` | Mic/camera/files consent | - |
| KnowledgeC.db | `~/Library/Application Support/Knowledge/knowledgeC.db` | App usage, unlocks | unix-timestamp |
| Quarantine | `QuarantineEventsV2` | Downloaded files, source URL | url-decode |
| Safari/Chrome History | `History.db` / `History` | URLs, downloads | url-decode |
| Shell History | `~/.zsh_history`, `~/.bash_history` | Commands typed | base64-utf8 |
| Login Items | `~/Library/Preferences/com.apple.loginitems.plist` | Auto-start apps | - |

## How to Document a Finding
1. Artefact + path + timestamp
2. Raw value (truncated)
3. CyberChef recipe used + decoded output
4. MITRE technique + severity (Low/Medium/High)
5. Verdict: Benign / Suspicious / Malicious
