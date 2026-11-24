# Contributing
1. Fork → branch `feat/<name>` → PR
2. Add artefact: update `docs/ARTEFACTS.md` + `src/parsers/windows.py` or `macos.py`
3. Add recipe: add `cyberchef/<name>.json` + entry in `cyberchef/README.md`
4. Test: `python tests/generate_fixtures.py --out ./samples && python src/triage.py --input ./samples/windows-triage --os windows --out ./reports/test`
5. Never commit real evidence.
