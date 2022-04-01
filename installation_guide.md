# Installation guide 

## Index
- Start project
- Execute the program

# Start project

```bash
sudo apt install python3
sudo apt install pip

python3 -m venv .venv
source .venv/bin/activate # on linux
source .venv/Scripts/activate # on windows
pip install -r requirements.txt
```
# Execute the program
```python
python3 gui_to_os.py ARG

# ARG is the path to the USB
# for example:
# python3 gui_to_os.py /dev/ttyACM0
```