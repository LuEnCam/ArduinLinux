# Installation guide

## Index

- Upload script to arduino
- Start project
- Execute the program

## Upload script to arduino

Open the sketch in sketch_project/ on [arduino IDE](https://www.arduino.cc/en/software).

Connect your arduino.

Upload it with the arrow button on the top left of the IDE.

## Start project

### on linux

```bash

sudo apt install python3
sudo apt install pip

python3 -m venv ./.venv
source ./.venv/bin/activate

pip install -r requirements.txt
```

### on windows

install [python3 with pip](https://www.python.org/downloads/)

```cmd

py -m venv .venv
call .venv/Scripts/activate.bat

pip install -r requirements.txt
```

## Execute the program

### linux

```python
source ./.venv/bin/activate
python3 ./gui_to_os.py
```

### winows

```python
call .venv/Scripts/activate.bat
py gui_to_os.py
```
