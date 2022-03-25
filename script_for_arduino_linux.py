from time import sleep
import serial
ser = serial.Serial('/dev/ttyACM1', 19200) # Establish the connection on a specific port

while True:
    value = ""
    
    while value != "red" and value != "blue" and value != "off":  
        value = input("Type command (red,blue,off) : ")
    
    ser.write(str.encode(value)) # Convert the decimal number to ASCII then send it to the Arduino
    print(ser.readline()) # Read the newest output from the Arduino
    sleep(.1) # Delay for one tenth of a second