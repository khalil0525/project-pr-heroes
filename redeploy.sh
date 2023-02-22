#!/bin/bash
cd project-pr-heroes
git fetch
git reset origin/main --hard
python -m venv python3-virtualenv
source python3-virtualenv/bin/activate
pip install -r requirements.txt
cd src
export FLASK_ENV=production
systemctl daemon-reload
systemctl restart myportfolio
