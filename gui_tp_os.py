import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QSlider
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
    def __init__(self):
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
        
        self.create_ui()
        
        self.show()
        
    def create_ui(self):
        
        sliderHue = QSlider(Qt.Orientation.Horizontal)
        sliderIntensity = QSlider(Qt.Orientation.Horizontal)
        
        button = QPushButton()
        button.setText("Click me")
        button.clicked.connect(self.bonjour)
        
        # add widgets to layout
        layout = QGridLayout(parent=self)
        layout.addWidget(sliderHue, 0, 0)
        layout.addWidget(sliderIntensity, 1, 0)
        layout.addWidget(button, 2, 0)
        
    def bonjour(self):
        print('bonjour')

def main():
    
    app = QApplication(sys.argv)

    mainWindow = MainWindow()
    
    sys.exit(app.exec()) # this is the main event loop

if __name__ == '__main__':
    main()