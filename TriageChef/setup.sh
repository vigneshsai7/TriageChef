#!/bin/bash
set -e
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
echo 'Setup done. Run: python tests/generate_fixtures.py --out ./samples'
