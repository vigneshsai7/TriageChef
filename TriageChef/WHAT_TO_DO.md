# WHAT TO DO — Real Case Checklist

## ✅ DO
- [ ] Work on a COPY / exported artefacts, never live disk
- [ ] Record case name, date, hash of image, who gave it to you
- [ ] Run triage → save `reports/case-XXX/` locally (NOT in git if real)
- [ ] Decode every suspicious string in CyberChef, save recipe + output
- [ ] Build timeline: what happened first, what happened together?
- [ ] Check IOCs: VirusTotal (hash only), AbuseIPDB, URLScan — never upload victim file
- [ ] Map to MITRE, assign severity + verdict
- [ ] Write final report: Summary → Timeline → Findings → IOCs → Recommendations
- [ ] Redact PII before sharing / pushing to GitHub

## ❌ DO NOT
- [ ] Do NOT push real evidence, PII, credentials to GitHub
- [ ] Do NOT paste real secrets into online CyberChef
- [ ] Do NOT run / execute suspicious binaries from image
- [ ] Do NOT decrypt / crack passwords with this tool (out of scope)
- [ ] Do NOT delete / modify original image

## 📝 Final Report Template
```
# Case XXX — Triage Report
- Date / Analyst / Image Hash
- Summary (3-5 lines: what happened?)
- Timeline (from timeline.csv)
- Findings (artefact + decoded + MITRE + verdict each)
- IOCs (table)
- Recommendations (isolate, reset creds, block domain, etc.)
- Appendix: CyberChef recipes used
```

## 🎯 For Your GitHub Portfolio / Interview
- Pin this repo on your GitHub profile
- In README, link demo report: `reports/demo-windows/report.md`
- Be ready to explain: 1 artefact from Windows, 1 from macOS, 1 CyberChef decode
