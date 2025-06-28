#!/bin/bash
pkill -f threebodychat/Orchestrator.py
pkill -f threebodychat/Maid.py
pkill -f threebodychat/Master.py
sleep 1
poetry run python threebodychat/Orchestrator.py &
poetry run python threebodychat/Maid.py &
poetry run python threebodychat/Master.py &
wait
