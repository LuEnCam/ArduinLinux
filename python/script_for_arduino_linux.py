from time import sleep
import serial

import sys


def send_input(ser: serial, _input: str):
    if ser is not None:
        ser.write(str.encode(_input)) # Convert the decimal number to ASCII then send it to the Arduino
        ##print(ser.readline()) # Read the newest output from the Arduino
        print(_input)
        sleep(0.2)
        


def dev():
    print(sys.platform)
    if sys.platform == 'win32':
        ser = serial.Serial('COM10', 9600) # Establish the connection on a specific port
    elif sys.platform == 'linux':
        ser = serial.Serial('/dev/ttyACM1', 19200) # Establish the connection on a specific port

    while True:
        value = ""
        
        while value == "":  
            value = input("Type Input: ")
        
        ser.write(str.encode(value)) # Convert the decimal number to ASCII then send it to the Arduino
        ##print(ser.readline()) # Read the newest output from the Arduino
    
    
def main():
    print("Main")

    
if __name__ == '__main__':
    # main()
    dev()