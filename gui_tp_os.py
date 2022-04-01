import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QSlider, QLabel, QTextEdit
from screeninfo import get_monitors

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
        super().__init__()
        
        # set title
        self.setWindowTitle("ARDUINO I COMMAND THEE")
        
        # set size of the app
        monitor_width, monitor_height = get_main_monitor_info()
        self.app_width, self.app_height = compute_app_size(monitor_width, monitor_height)
        
        self.setFixedSize(self.app_width, self.app_height)
        
        # move the window
        c_with, c_height = get_center_app_position(monitor_width, monitor_height, self.app_width, self.app_height)
        self.move(c_with, c_height)
        
        del monitor_width, monitor_height, c_with, c_height
        
        self.create_ui(**kwargs)
        
        
    def create_ui(self, **kwargs):
        
        # create the title labels
        LEDTitle = QLabel("LED")
        JoystickTitle = QLabel("Joystick")
        
        # create the joystick input text zone
        textJoystick = QTextEdit()
        textJoystick.setReadOnly(True)
        
        # create LED sliders
        initialHueValue = 0
        self.hueWheel = 360
        labelHue = QLabel('Hue value of the led')
        self.labelValueHue = QLabel('value: %.2f' % initialHueValue)
        sliderHue = QSlider(Qt.Orientation.Horizontal)
        sliderHue.setMinimum(0)
        sliderHue.setMaximum(self.hueWheel) # correspond to the HUE color circle
        sliderHue.setTickInterval(45)
        sliderHue.setTickPosition(QSlider.TickPosition.TicksBothSides)
        sliderHue.valueChanged.connect(self.hueChangeValue)
        sliderHue.setValue(initialHueValue)
        
        initialIntensityValue = 0
        self.hueIntensity = 100
        labelIntensity = QLabel('Hue value of the led')
        self.labelValueIntensity = QLabel('value: %.2f' % initialIntensityValue)
        sliderIntensity = QSlider(Qt.Orientation.Horizontal)
        sliderIntensity.setMinimum(0)
        sliderIntensity.setMaximum(self.hueIntensity)
        sliderIntensity.setTickInterval(10)
        sliderIntensity.setTickPosition(QSlider.TickPosition.TicksBothSides)
        sliderIntensity.valueChanged.connect(self.hueChangeIntensity)
        sliderIntensity.setValue(initialIntensityValue)
        
        # create LED buttons
        btnTurnOn = QPushButton("ON")
        btnTurnOn.clicked.connect(self.turnOnLed)
        
        btnTurnOff = QPushButton("OFF")
        btnTurnOff.clicked.connect(self.turnOffLed)
        
        initialBtnState = kwargs.pop('btnState', False)
        self.labelBtnState = QLabel(f"LED is : {'ON' if initialBtnState else 'OFF'}")
        self.turnOnLed() if initialBtnState else self.turnOffLed()
        
        # add widgets to layout
        layout = QGridLayout(parent=self)
        row = 0
        
        # joystick title
        layout.addWidget(JoystickTitle, row, 0)
        row += 1
        # text joystick
        layout.addWidget(textJoystick, row, 0)
        row += 1
        
        # led title
        layout.addWidget(LEDTitle, row, 0)
        row += 1
        # hue
        layout.addWidget(labelHue, row, 0)
        layout.addWidget(self.labelValueHue, row, 1)
        row += 1
        layout.addWidget(sliderHue, row, 0)
        row += 1
        # intensity
        layout.addWidget(labelIntensity, row, 0)
        layout.addWidget(self.labelValueIntensity, row, 1)
        row += 1
        layout.addWidget(sliderIntensity, row, 0)
        row += 1
        layout.addWidget(self.labelBtnState, row, 0)
        row += 1
        layout.addWidget(btnTurnOn, row, 0)
        layout.addWidget(btnTurnOff, row, 1)
        row += 1
    
    def hueChangeValue(self):
        value = self.sender().value() / self.hueWheel
        self.labelValueHue.setText('value: %.2f' % value)
        
    def hueChangeIntensity(self):
        value = self.sender().value() / self.hueIntensity
        self.labelValueIntensity.setText('value: %.2f' % value)
        
    def turnOnLed(self):
        self.labelBtnState.setText(f'LED is : ON')
    
    def turnOffLed(self):
        self.labelBtnState.setText(f'LED is : OFF')

def main():
    
    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()
    
    sys.exit(app.exec()) # this is the main event loop

if __name__ == '__main__':
    main()