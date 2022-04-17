#!/bin/bash


echo "Activating python virtual environment..."
source ./.venv/bin/activate

echo "Activated!"

echo "Starting the application..."
cd python/
python3 ./gui_tp_os.py
