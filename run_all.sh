#!/bin/bash
poetry run python threebodychat/Orchestrator.py &
poetry run python threebodychat/Maid.py &
poetry run python threebodychat/Master.py &
wait
