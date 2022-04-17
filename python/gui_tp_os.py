import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QSlider, QLabel, QTextEdit, QTextEdit, QLineEdit, QMessageBox, QVBoxLayout, QGridLayout
from screeninfo import get_monitors
from functools import partial
import project_events
import script_for_arduino_linux as script
import serial
from  serial.tools import list_ports


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
        
        self.switch_button.setDisabled(True)
        self.is_GUI_mode()
        
        
    def create_ui(self, **kwargs):
        
        # create the title labels
        LEDTitle = QLabel('LED')
        JoystickTitle = QLabel('Joystick')
        LEDTitle.setStyleSheet('font-weight: bold; font-size: 16px;')
        JoystickTitle.setStyleSheet('font-weight: bold; font-size: 16px;')
        
        ##Objects values for the LED
        self.hue = 0
        self.sat = 0
        self.on_off = 0
        self.mode_GUI = False ## for UI mode, else False for joystick mode
            
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
        initialHueValue = 0
        self.hueWheel = 360
        self.basicSliderHueText = 'HUE: '
        self.labelValueHue = QLabel(self.basicSliderHueText + '%.2f' % initialHueValue)
        self.labelValueHue.setStyleSheet('font-size: 12px;')
        self.sliderHue = QSlider(Qt.Orientation.Horizontal)
        self.sliderHue.setMinimum(0)
        self.sliderHue.setMaximum(self.hueWheel) # correspond to the HUE color circle
        self.sliderHue.setTickInterval(45)
        self.sliderHue.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.sliderHue.valueChanged.connect(self.hueChangeValue)
        self.sliderHue.setValue(initialHueValue)
        
        # intensity
        initialIntensityValue = 0
        self.hueIntensity = 100
        self.basicSliderIntensityText = 'Intensity: '
        self.labelValueIntensity = QLabel(self.basicSliderIntensityText + '%.2f' % initialIntensityValue)
        self.labelValueIntensity.setStyleSheet('font-size: 12px;')
        self.sliderIntensity = QSlider(Qt.Orientation.Horizontal)
        self.sliderIntensity.setMinimum(0)
        self.sliderIntensity.setMaximum(self.hueIntensity)
        self.sliderIntensity.setTickInterval(10)
        self.sliderIntensity.setTickPosition(QSlider.TickPosition.TicksLeft)
        self.sliderIntensity.valueChanged.connect(self.hueChangeIntensity)
        self.sliderIntensity.setValue(initialIntensityValue)
        
        # create LED button
        self.btnToggleLED = QPushButton()
        self.btnToggleLED.setCheckable(True)
        self.btnToggleLED.clicked.connect(partial(self.toggleLed, self.btnToggleLED))
        self.basicToggleLedText = 'LED is : '
        initialBtnState = kwargs.pop('btnState', False)
        self.toggleLed(self.btnToggleLED, initialBtnState)
        
        # create switch mode button
        self.switch_button = QPushButton("Mode : Joystick")
        self.switch_button.clicked.connect(self.switch_mode)
        
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
        layoutSliders.addWidget(self.sliderHue, 0, 1)
        layoutSliders.addWidget(self.labelValueIntensity, 1, 0)
        layoutSliders.addWidget(self.sliderIntensity, 1, 1)
        layoutSliders.addWidget(portTitle, 2, 0)
        layoutSliders.addWidget(self.arduinoPort, 2, 1)
        layoutSliders.addWidget(self.connectPushButton, 2, 2)
        
        layout.addLayout(layoutSliders)

        # turn on/off button
        layout.addWidget(self.btnToggleLED)
        
        # switch mode button
        layout.addWidget(self.switch_button)
    
    ##• Changes the color of the LED
    def hueChangeValue(self):
        value = self.sender().value() ## / self.hueWheel
        self.labelValueHue.setText(self.basicSliderHueText + '%.2f' % value)
        self.hue = value
        mode = get_mode_value(self.mode_GUI)
        script.send_input(self.serial, f"{self.on_off} {self.hue} {self.sat} {mode} \n")

    ## Changes the intensity of the LED
    def hueChangeIntensity(self):
        value = self.sender().value() / self.hueIntensity
        self.labelValueIntensity.setText(self.basicSliderIntensityText + '%.2f' % value)
        self.sat = value
        mode = get_mode_value(self.mode_GUI)
        script.send_input(self.serial, f"{self.on_off} {self.hue} {self.sat} {mode} \n")
        
    ## Defines the port of the arduino
    def portDefine(self):
        value = self.arduinoPort.text()
        try:
            if sys.platform == 'win32':
                self.serial = serial.Serial(f'{value}', 9600) # Establish the connection on a specific port
            elif sys.platform == 'linux':
                self.serial = serial.Serial(f'/dev/{value}', 9600) # Establish the connection on a specific port
            self.arduinoPort.clear()
            self.connectPushButton.setDisabled(True)
            self.switch_button.setEnabled(True)
            QMessageBox.information(self, 'Connection', f'Connection established to port {value}')
        except:
            QMessageBox.warning(self, 'Error', f'Port n° "{value}" not found')

    ## Switches the LED on/off    
    def toggleLed(self, sender, checked):
        mode = 'ON' if checked else 'OFF'
        sender.setText(self.basicToggleLedText + mode)
        project_events.ledEvent(checked)
        self.on_off = 1 if checked else 0
        mode = get_mode_value(self.mode_GUI)
        script.send_input(self.serial, f"{self.on_off} {self.hue} {self.sat} {mode} \n")

    ## Was used to get the values from the joystick (not used anymore)
    def joystickEventThing(self, s):
        oldText = self.textJoystick.toPlainText()
        if oldText != '':
            s += '\n'
        self.textJoystick.setText(s + oldText)
        
    ## Switches the mode between joystick and keyboard
    def switch_mode(self):
        self.mode_GUI = not self.mode_GUI
        mode = get_mode_value(self.mode_GUI)
        text = "UI" if self.mode_GUI == True else "Joystick"
        self.switch_button.setText(f'Mode : {text}')
        self.is_GUI_mode()
        script.send_input(self.serial, f"{self.on_off} {self.hue} {self.sat} {mode} \n")
        ## if mode == 2: ## Petit hack pour éviter que le joystick ne se déclenche en mode UI
           ## script.send_input(self.serial, f"{self.on_off} {self.hue} {self.sat} {mode} \n")
     
    ## Checks if the mode is joystick or UI   
    def is_GUI_mode(self):
        self.btnToggleLED.setEnabled(self.mode_GUI)
        self.sliderIntensity.setEnabled(self.mode_GUI)
        self.sliderHue.setEnabled(self.mode_GUI)
        
        
def get_mode_value(val):
    mode = 2 if val == True else 1
    return mode    
        

def main():
    
    app = QApplication(sys.argv)
    
    mainWindow = MainWindow()
    mainWindow.show()
    
    sys.exit(app.exec()) # this is the main event loop

if __name__ == '__main__':
    main()
