from time import sleep
import serial

import sys


def dev():
    print(sys.platform)
    if sys.platform == 'win32':
        ser = serial.Serial('COM10', 9600) # Establish the connection on a specific port
    elif sys.platform == 'linux':
        ser = serial.Serial('/dev/ttyACM1', 19200) # Establish the connection on a specific port

    while True:
        value = ""
        
        while value != "red" and value != "blue" and value != "off":  
            value = input("Type command (red,blue,off) : ")
        
        ser.write(str.encode(value)) # Convert the decimal number to ASCII then send it to the Arduino
        print(ser.readline()) # Read the newest output from the Arduino
        sleep(.1) # Delay for one tenth of a second
    
    
def main():
    print("Main")

    
if __name__ == '__main__':
    # main()
    dev()