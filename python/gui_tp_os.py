import sys
from typing import IO
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QSlider, QLabel, QTextEdit, QTextEdit, QLineEdit, QMessageBox
from PyQt6.QtWidgets import QVBoxLayout, QGridLayout
from screeninfo import get_monitors
from functools import partial
import project_events
import script_for_arduino_linux as script
import serial
from serial.tools import list_ports
from time import sleep



# get width and height of main monitor
def get_main_monitor_info():
    monitor = get_monitors()[0]
    return monitor.width, monitor.height	

# compute the app size based on the main monitor size
def compute_app_size(width, height):
    # based on 1920x1080
    prefered_width = 800
    prefered_height = 600
    app_width = width/1920 * prefered_width
    app_height = height/1080 * prefered_height
    return int(app_width), int(app_height)

def get_center_app_position(monitor_width, monitor_height, app_width, app_height):
    return int(monitor_width/2 - app_width/2), int(monitor_height/2 - app_height/2)

class MainWindow(QWidget):
    def __init__(self, **kwargs):
        '''
        optionnal kwargs:
        btnState: boolean # initial state of the LED
        '''
        project_events.joystickEvent += self.joystickEventThing

        super().__init__()
        
        # set title
        self.setWindowTitle('ARDUINO I COMMAND THEE')
        
        # set size of the app
        monitor_width, monitor_height = get_main_monitor_info()
        self.app_width, self.app_height = compute_app_size(monitor_width, monitor_height)
        
        self.setFixedSize(self.app_width, self.app_height)
        
        # move the window
        c_with, c_height = get_center_app_position(monitor_width, monitor_height, self.app_width, self.app_height)
        self.move(c_with, c_height)
        
        del monitor_width, monitor_height, c_with, c_height
        
        self.list_of_ports = []
         
        for comport in serial.tools.list_ports.comports():
            self.list_of_ports.append(comport.device)
                
        self.serial = None
        
        self.create_ui(**kwargs)
        
        
    def create_ui(self, **kwargs):
        
        # create the title labels
        LEDTitle = QLabel('LED')
        JoystickTitle = QLabel('Joystick')
        LEDTitle.setStyleSheet('font-weight: bold; font-size: 16px;')
        JoystickTitle.setStyleSheet('font-weight: bold; font-size: 16px;')
        
        self.hue = 0
        self.sat = 0
        self.on_off = 0
            
        # create the joystick input text zone
        self.textJoystick = QTextEdit()
        self.textJoystick.setReadOnly(True)
        
        # create the inputbox for the arduino port
        portTitle = QLabel('Arduino port')
        self.connectPushButton = QPushButton('Connect')
        self.arduinoPort = QLineEdit()
        self.arduinoPort.setPlaceholderText(f"Example on Linux: \"ttyACM0\". Example on Windows: \"COM10\". Port founds : {[i for i in self.list_of_ports]}")
        self.connectPushButton.pressed.connect(self.portDefine)
        

        # create LED sliders
        # hue
        initialHueValue = 0
        self.hueWheel = 360
        self.basicSliderHueText = 'HUE: '
        self.labelValueHue = QLabel(self.basicSliderHueText + '%.2f' % initialHueValue)
        self.labelValueHue.setStyleSheet('font-size: 12px;')
        sliderHue = QSlider(Qt.Orientation.Horizontal)
        sliderHue.setMinimum(0)
        sliderHue.setMaximum(self.hueWheel) # correspond to the HUE color circle
        sliderHue.setTickInterval(45)
        sliderHue.setTickPosition(QSlider.TickPosition.TicksAbove)
        sliderHue.valueChanged.connect(self.hueChangeValue)
        sliderHue.setValue(initialHueValue)
        # intensity
        initialIntensityValue = 0
        self.hueIntensity = 100
        self.basicSliderIntensityText = 'Intensity: '
        self.labelValueIntensity = QLabel(self.basicSliderIntensityText + '%.2f' % initialIntensityValue)
        self.labelValueIntensity.setStyleSheet('font-size: 12px;')
        sliderIntensity = QSlider(Qt.Orientation.Horizontal)
        sliderIntensity.setMinimum(0)
        sliderIntensity.setMaximum(self.hueIntensity)
        sliderIntensity.setTickInterval(10)
        sliderIntensity.setTickPosition(QSlider.TickPosition.TicksLeft)
        sliderIntensity.valueChanged.connect(self.hueChangeIntensity)
        sliderIntensity.setValue(initialIntensityValue)
        
        # create LED button
        btnToggleLED = QPushButton()
        btnToggleLED.setCheckable(True)
        btnToggleLED.clicked.connect(partial(self.toggleLed, btnToggleLED))
        self.basicToggleLedText = 'LED is : '
        initialBtnState = kwargs.pop('btnState', False)
        self.toggleLed(btnToggleLED, initialBtnState)
        
        # add widgets to layout
        layout = QVBoxLayout(self)
        
        # joystick title
        layout.addWidget(JoystickTitle)
        
        # text joystick
        layout.addWidget(self.textJoystick)
        
        # led title
        layout.addWidget(LEDTitle)
        
        # sliders
        layoutSliders = QGridLayout()
        layoutSliders.addWidget(self.labelValueHue, 0, 0)
        layoutSliders.addWidget(sliderHue, 0, 1)
        layoutSliders.addWidget(self.labelValueIntensity, 1, 0)
        layoutSliders.addWidget(sliderIntensity, 1, 1)
        layoutSliders.addWidget(portTitle, 2, 0)
        layoutSliders.addWidget(self.arduinoPort, 2, 1)
        layoutSliders.addWidget(self.connectPushButton, 2, 2)
        
        layout.addLayout(layoutSliders)
        # # hue
        # layoutHUE = QHBoxLayout()
        # layoutHUE.addWidget(self.labelValueHue)
        # layoutHUE.addWidget(sliderHue)
        # layout.addLayout(layoutHUE)

        # # intensity
        # layoutIntensity = QHBoxLayout()
        # layoutIntensity.addWidget(self.labelValueIntensity)
        # layoutIntensity.addWidget(sliderIntensity)
        # layout.addLayout(layoutIntensity)

        # turn on/off button
        layout.addWidget(btnToggleLED)
    
    def hueChangeValue(self):
        value = self.sender().value() ## / self.hueWheel
        self.labelValueHue.setText(self.basicSliderHueText + '%.2f' % value)
        self.hue = value
        script.send_input(self.serial, f"{self.on_off} {self.hue} {self.sat}")

        
        
    def hueChangeIntensity(self):
        value = self.sender().value() / self.hueIntensity
        self.labelValueIntensity.setText(self.basicSliderIntensityText + '%.2f' % value)
        self.sat = value
        script.send_input(self.serial, f"{self.on_off} {self.hue} {self.sat}")
        
    def portDefine(self):
        value = self.arduinoPort.text()
        try:
            if sys.platform == 'win32':
                self.serial = serial.Serial(f'{value}', 9600) # Establish the connection on a specific port
            elif sys.platform == 'linux':
                self.serial = serial.Serial(f'/dev/{value}', 9600) # Establish the connection on a specific port
            self.arduinoPort.clear()
            self.connectPushButton.setDisabled(True)
            QMessageBox.information(self, 'Connection', f'Connection established to port {value}')
        except:
            QMessageBox.warning(self, 'Error', f'Port n° "{value}" not found')

        
    def toggleLed(self, sender, checked):
        mode = 'ON' if checked else 'OFF'
        sender.setText(self.basicToggleLedText + mode)
        project_events.ledEvent(checked)
        self.on_off = 1 if checked else 0
        script.send_input(self.serial, f"{self.on_off} {self.hue} {self.sat}")


    def joystickEventThing(self, s):
        oldText = self.textJoystick.toPlainText()
        if oldText != '':
            s += '\n'
        self.textJoystick.setText(s + oldText)

def main():
    
    app = QApplication(sys.argv)
    
    mainWindow = MainWindow()
    mainWindow.show()
    
    sys.exit(app.exec()) # this is the main event loop

if __name__ == '__main__':
    main()
