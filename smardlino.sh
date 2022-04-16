#!/bin/bash


echo "Activating python virtual environment..."
source ./.venv/bin/activate

echo "Activated!"

echo "Starting the application..."
cd python/
pythonw3 ./gui_tp_os.py
