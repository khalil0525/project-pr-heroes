#!/bin/bash
tmux kill-session
cd project-pr-heroes
git fetch
git reset origin/main --hard
tmux new-session -d -s mysession
tmux send-keys -t mysession "python -m venv python3-virtualenv" Enter
tmux send-keys -t mysession "source python3-virtualenv/bin/activate" Enter
tmux send-keys -t mysession "pip install -r requirements.txt" Enter
tmux send-keys -t mysession "source python3-virtualenv/bin/activate" Enter
tmux send-keys -t mysession "cd src" Enter
tmux send-keys -t mysession "export FLASK_ENV=production" Enter
tmux send-keys -t mysession "flask run --host=192.241.147.151" Enter
tmux send-keys -t mysession "source python3-virtualenv/bin/activate" Enter
tmux detach
