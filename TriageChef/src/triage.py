"""Forensic Triage - Windows & macOS. Read-only. Usage: python src/triage.py --input ./samples/windows-triage --os windows --out ./reports/demo"""
import argparse, csv, hashlib, json, re, sys
from pathlib import Path
from datetime import datetime, timezone
sys.path.insert(0, str(Path(__file__).parent))
from cyberchef_bridge import build_cyberchef_url, suggest_recipe

IOC_PATTERNS = {
  "ipv4": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
  "domain": r"\b(?:[a-z0-9-]+\.)+(?:com|net|io|xyz|ru|top|pw|cc|onion)\b",
  "url": r"https?://[^\s'\"]+",
  "base64_powershell": r"(?:[A-Za-z0-9+/]{40,}={0,2})",
  "hex_blob": r"\b(?:[0-9a-fA-F]{32,})\b",
  "email": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
  "sha256": r"\b[a-f0-9]{64}\b",
  "md5": r"\b[a-f0-9]{32}\b",
}
SUSPICIOUS = ["powershell","-enc","-EncodedCommand","FromBase64String","Invoke-Expression","iex ","certutil","bitsadmin","rundll32","regsvr32","mshta","wscript","cscript","curl ","wget ","nc ","ncat","mimikatz","sekurlsa","lsass","psexec","bloodhound","sharphound","/tmp/","osascript","launchctl","curl -","base64 -d","chmod +x"]

def sha256(p: Path):
    h=hashlib.sha256()
    try:
        h.update(p.read_bytes()[:5_000_000])
    except Exception: return ""
    return h.hexdigest()

def scan_file(p: Path):
    try: text=p.read_bytes().decode("utf-8", errors="ignore")
    except Exception: return []
    findings=[]
    for i,line in enumerate(text.splitlines(),1):
        low=line.lower()
        if any(s.lower() in low for s in SUSPICIOUS):
            recipe=suggest_recipe(line)
            findings.append({"file":str(p),"line":i,"text":line.strip()[:500],"recipe":recipe,"cyberchef_url":build_cyberchef_url(recipe,line.strip())})
    return findings

def extract_iocs(text: str):
    out={}
    for k,pat in IOC_PATTERNS.items():
        vals=sorted(set(re.findall(pat,text)))
        if vals: out[k]=vals[:100]
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input", required=True); ap.add_argument("--os", choices=["windows","macos","auto"], default="auto"); ap.add_argument("--out", required=True)
    a=ap.parse_args()
    inp=Path(a.input); out=Path(a.out); out.mkdir(parents=True, exist_ok=True)
    os_name=a.os
    if os_name=="auto":
        txt=" ".join(p.name.lower() for p in inp.rglob("*") if p.is_file())
        os_name="macos" if ("launchagents" in txt or "tcc.db" in txt or "quarantine" in txt) else "windows"
    files=[p for p in inp.rglob("*") if p.is_file()]
    findings=[]; timeline=[]; all_text=""
    for p in files:
        findings+=scan_file(p)
        try: all_text+=p.read_bytes().decode("utf-8",errors="ignore")+"\n"
        except Exception: pass
        timeline.append({"timestamp":datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc).isoformat(),"artefact":str(p.relative_to(inp)),"sha256":sha256(p),"os":os_name})
    iocs=extract_iocs(all_text)
    timeline.sort(key=lambda x: x["timestamp"])
    with open(out/"timeline.csv","w",newline="") as f:
        w=csv.DictWriter(f, fieldnames=["timestamp","artefact","sha256","os"]); w.writeheader(); w.writerows(timeline)
    (out/"findings.json").write_text(json.dumps({"os":os_name,"files_scanned":len(files),"findings":findings,"iocs":iocs}, indent=2))
    (out/"iocs.json").write_text(json.dumps(iocs, indent=2))
    (out/"suspicious_strings.txt").write_text("\n".join(f["text"] for f in findings))
    md=f"# Triage Report - {os_name.upper()}\n\n- Generated: {datetime.now(timezone.utc).isoformat()}\n- Input: {inp}\n- Files scanned: {len(files)}\n- Findings: {len(findings)}\n\n## Findings (with CyberChef recipe)\n\n"
    for f in findings:
        md+=f"- **{f['file']}:{f['line']}** - `{f['text'][:200]}`\n  Recipe: `{f['recipe']}` | [Open in CyberChef]({f['cyberchef_url']})\n"
    md+="\n## IOCs\n\n```json\n"+json.dumps(iocs,indent=2)+"\n```\n\n## Timeline\nSee `timeline.csv`\n"
    (out/"report.md").write_text(md)
    print(f"Done: {len(files)} files, {len(findings)} findings -> {out}/report.md")

if __name__=="__main__": main()
