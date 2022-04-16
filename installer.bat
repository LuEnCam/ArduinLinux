@echo off

echo Starting installer...

echo Creating python venv...
py -m venv .venv

echo Activating python virtual environment...
call .venv/Scripts/activate.bat

echo Installing requirements...
pip install -r requirements.txt

echo Installation finished, you can now run the app.
pause
