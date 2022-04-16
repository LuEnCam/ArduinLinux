#!/bin/bash

echo Starting installer...


echo -e  "\nCreating python venv..."
python3 -m venv .venv


echo -e  "\nActivating python virtual environment..."
source ./.venv/bin/activate


echo -e  "\nInstalling requirements..."
pip3 install -r requirements.txt


echo -e  "\nNow connect your arduino board to your pc"
read

cd ./arduino-cli_0.21.1_Linux_64bit/

echo -e  "\nInstalling the platform..."
./arduino-cli core install arduino:avr


echo -e  "\nCompiling the sketch..."
./arduino-cli compile --fqbn arduino:avr:uno ../sketch_project/sketch_project.ino


echo -e  "\nUploading the sketch..."
echo "Which port ? (write /dev/tty3 for example): "
read com
echo "arduino is on port $com"
./arduino-cli upload -p dev/tty$com --fqbn arduino:avr:uno ../sketch_project/sketch_project.ino

echo.
echo Installation finished, you can now run the app.
pause
