from queue import Queue
from time import sleep
import serial
import sys
from project_events import joystickEvent
from PyQt6.QtCore import QThread, pyqtSignal, QRunnable, QObject

def send_input(ser: serial, _input: str):
    if ser is not None:
        ser.write(str.encode(_input)) # Convert the decimal number to ASCII then send it to the Arduino
        ##print(ser.readline()) # Read the newest output from the Arduino (not used anymore)
        ## print(_input)
        ## sleep(0.2)

class ReadInputSignals(QObject):
    result = pyqtSignal(str)

class ReadInput(QRunnable):
    def __init__(self, ser: serial, signals: ReadInputSignals):
        super().__init__()
        self.ser = ser
        self.signals = signals

    def run(self):
        s = read_input(self.ser)
        self.signals.result.emit(s)

def read_input(ser: serial):

    if ser is not None:
        b = ser.readline()
        s = b.decode("utf-8").strip('\r\n')
        return s


def dev():
    print(sys.platform)
    if sys.platform == 'win32':
        ser = serial.Serial('COM10', 9600) # Establish the connection on a specific port
    elif sys.platform == 'linux':
        ser = serial.Serial('/dev/ttyACM1', 9600) # Establish the connection on a specific port

    while True:
        value = ""
        
        while value == "":  
            value = input("Type Input: ")
        
        ser.write(str.encode(value)) # Convert the decimal number to ASCII then send it to the Arduino
        ##print(ser.readline()) # Read the newest output from the Arduino
    