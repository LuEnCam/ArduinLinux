@echo off

echo "Activating python virtual environment..."
call .venv/Scripts/activate.bat

echo "Activated!"

echo "Starting the application..."
cd python/
start /min pyw gui_tp_os.py
