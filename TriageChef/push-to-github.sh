#!/bin/bash
# Usage: ./push-to-github.sh <you>/forensic-triage-cyberchef
set -e
REPO=${1:-<you>/forensic-triage-cyberchef}
git init
git add .
git commit -m "feat: forensic triage + cyberchef mini-project" || true
git branch -M main
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/$REPO.git
git push -u origin main
echo "Pushed to https://github.com/$REPO"
