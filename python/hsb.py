from PyQt6.QtWidgets import QApplication, QWidget, QSlider, QGridLayout, QLabel, QCheckBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import sys
from functools import partial
from math import sqrt, atan, pi

# def debug(tab):
#     for dic in tab:
#         s = ''
#         for k, v in dic.items():
#             s += f'{k}:{v} '
#         print(s)
#     print('\n')


MAX = 1023
def getHSV(x, y):
    #center is P(511; 511);
    x = x - int(MAX / 2) -1
    y = y - int(MAX / 2) -1
    # now center is P(0; 0), min-max is (-512, 511)

    # // saturation = norme(P, joy.pos)

    saturation = sqrt(x**2 + y**2) / ((MAX / 2) + 1)
    if saturation > 1:
        saturation = 1
    # Hue is the angle between 0 and 360 between our position and the xAxis)
    # simple math, use pythagore and tan the y on x
    # if x == 0 => either 90° or 270°
    
    if x == 0:
        if y == 0:
            hue = 0
        else:
            hue = 90 if y > 0 else 270
    else:
        ratio = y/x
        alpha = atan(ratio)
        # now in degrees
        alpha = alpha * 180 / pi

        # first and third quarter
        if alpha >= 0:
            # first quarter
            if x > 0:
                hue = alpha
            # third quarter
            else:
                hue = alpha + 180
        # second and fourth quarter
        else:
            # second quarter
            if y > 0:
                hue = alpha + 180
            # fourth quarter
            else:
                hue = alpha + 360
        
        
    value = 1
    return hue, saturation, value

def HSVtoRGB(x, y):
    h,s,v = getHSV(x, y)
    
    c = v * s
    un = h/60
    deux = un % 2 - 1
    trois = 1 - abs(deux)
    x = c * trois
    # x = c * (1-abs((h / 60) % 2 - 1))
    m = v - c
    # debug([
    #     {'h': h, 's': s, 'v': v},
    #     {'un': un, 'deux': deux, 'trois': trois},
    #     {'c': c, 'x': x, 'm': m},
    #     ])

    if 0 <= h and h < 60:
        # rgb = [c, x, 0];
        r, g, b = c, x, 0
    if 60 <= h and h < 120:
        # rgb = [x, c, 0];
        r, g, b = x, c, 0
    if 120 <= h and h < 180:
        # rgb = [0, c, x];
        r, g, b = 0, c, x
    if 180 <= h and h < 240:
        # rgb = [0, x, c];
        r, g, b = 0, x, c
    if 240 <= h and h < 300:
        # rgb = [x, 0, c];
        r, g, b = x, 0, c
    if 300 <= h and h < 360:
        # rgb = [c, 0, x];
        r, g, b = c, 0, x
    
    r = (r+m) * 255
    g = (g+m) * 255
    b = (b+m) * 255
    if r > 255 or r < 0:
        print('r:',r,h, s, v)
    if g > 255 or g < 0:
        print('g:',g,h, s, v)
    if b > 255 or b < 0:
        print('b:',b,h, s, v)
    return r, g, b

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_gui()
        
    def init_gui(self):
        self.sliderX = QSlider(Qt.Orientation.Horizontal)
        self.sliderY = QSlider(Qt.Orientation.Vertical)
        
        self.sliderX.setFixedSize(300, 20)
        self.sliderY.setFixedSize(20, 300)
        self.sliderX.setRange(0, MAX)
        self.sliderY.setRange(0, MAX)
        self.x = int(MAX / 2)
        self.y = int(MAX / 2)
        self.sliderX.setValue(self.x)
        self.sliderY.setValue(self.y)
        
        self.sliderX.valueChanged.connect(partial(self.sliderChanged, 'x'))
        self.sliderY.valueChanged.connect(partial(self.sliderChanged, 'y'))
        
        self.w = QWidget()
        self.changeColor()

        self.lbValue = QLabel(self.strLbValue())
        self.lbValue.setStyleSheet('background-color: transparent;')
        self.lbValue.setFont(QFont('Arial', 20))

        self.followBorder = True
        cbx1 = QCheckBox('hit border')
        cbx1.setChecked(self.followBorder)
        cbx1.clicked.connect(self.cbxIsClicked)
        
        self.isXAxisMain = True
        cbx2 = QCheckBox('follow x axis')
        cbx2.setChecked(self.isXAxisMain)
        cbx2.clicked.connect(self.cbxXMain)
        
        self.isNegativeAxis = False
        cbx3 = QCheckBox('use negative axis')
        cbx3.setChecked(self.isNegativeAxis)
        cbx3.clicked.connect(self.bcxNegativeAxis)
        

        layout = QGridLayout(self)
        layout.addWidget(self.sliderX, 1, 1, 1, 1, Qt.AlignmentFlag.AlignBottom) 
        layout.addWidget(self.sliderY, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.w, 0, 1, 1, 1)
        layout.addWidget(self.lbValue, 0, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(cbx1, 1, 2, 1, 1)
        layout.addWidget(cbx2, 2, 2, 1, 1)
        layout.addWidget(cbx3, 3, 2, 1, 1)
     
    def sliderChanged(self, sender, value):
        if sender == 'x':
            if self.isXAxisMain and self.followBorder:
                otherValue = self.getOtherSliderValue(value)
                self.sliderY.setValue(otherValue)
                self.y = otherValue
            self.x = value
        elif sender == 'y':
            if not self.isXAxisMain and self.followBorder:
                otherValue = self.getOtherSliderValue(value)
                self.sliderX.setValue(otherValue)
                self.x = otherValue
            self.y = value
        self.lbValue.setText(self.strLbValue())
        self.changeColor()

    def getOtherSliderValue(self, value):
        # x, y = [0, MAX]
        # P (MAX/2, MAX/2)
        # x^2 + y^2 = (MAX/2)^2
        # we search y
        # y^2 = (MAX/2)^2 - x^2
        # y = sqrt(...)
        half_max = int(MAX/2)
        x = value - half_max -1 # [-512, 511]
        if x == -half_max-1:
            x += 1  # because crash when x = -512
        y = int(sqrt(half_max**2 - x**2))
        if not self.isNegativeAxis:
            y += half_max
        else:
            y = half_max - y
        return y

    def strLbValue(self):
        return f'({self.x};{self.y})'
    
    def changeColor(self):
        r, g, b = HSVtoRGB(self.x, self.y)
        styleSheet = f'background-color: rgb({r}, {g}, {b});'

        self.w.setStyleSheet(styleSheet)
        
    def cbxIsClicked(self, isClicked):
        self.followBorder = isClicked
        
    def cbxXMain(self, isClicked):
        self.isXAxisMain = isClicked
        
    def bcxNegativeAxis(self, isClicked):
        self.isNegativeAxis = isClicked

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWidget()
    w.show()
    sys.exit(app.exec())
