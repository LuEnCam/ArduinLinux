@echo off

echo Starting installer...

echo.
echo Creating python venv...
py -m venv ./.venv

echo.
echo Activating python virtual environment...
call ./.venv/Scripts/activate.bat

echo.
echo Installing requirements...
pip install -r ./requirements.txt

echo.
echo Now connect your arduino board to your pc
pause

cd ./arduino-cli_0.21.1_Windows_64bit
echo.
echo Installing the platform...
./arduino-cli.exe core install arduino:avr

echo.
echo Compiling the sketch...
./arduino-cli.exe compile --fqbn arduino:avr:uno ../sketch_project/sketch_project.ino

echo.
echo Uploading the sketch...
set /p com=Which port ? (only the number):\ntips: you can see it by right-clicking on windows logo -> Device Manager -> Ports -> COM
echo arduino is on port COM%com%
./arduino-cli.exe upload -p COM%com% --fqbn arduino:avr:uno ../sketch_project/sketch_project.ino

echo.
echo Installation finished, you can now run the app.
pause
