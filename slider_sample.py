import sys
from PyQt5 import QtCore, QtSerialPort
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

servo_1_id = (201).to_bytes(1, 'big')
servo_2_id = (202).to_bytes(1, 'big')
servo_3_id = (203).to_bytes(1, 'big')
servo_4_id = (204).to_bytes(1, 'big')

class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

        self.serial = QtSerialPort.QSerialPort(
            'COM6', baudRate=QtSerialPort.QSerialPort.Baud9600, 
            readyRead = self.receive)
        self.serial.open(QtCore.QIODevice.ReadWrite)
    
    def initUI(self):
        
        self.angle_label = [QLabel() for x in range(4)]

        for each_label in self.angle_label:
            each_label.setText(str(90))

        self.angle_slider = [QSlider(Qt.Orientation.Horizontal) for x in range(4)]
        
        for each_slider in self.angle_slider:
            each_slider.setMaximum(170)
            each_slider.setMinimum(10)
            each_slider.setValue(90)
            each_slider.valueChanged.connect(self.value_change)
        
        servo_frame = [QFrame() for x in range(4)]
        servo_layout = [QHBoxLayout() for x in range(4)]

        vbox = QVBoxLayout()

        for i in range(4):
            servo_layout[i].addWidget(self.angle_label[i])
            servo_layout[i].addWidget(self.angle_slider[i])

            servo_frame[i].setLayout(servo_layout[i])
            vbox.addWidget(servo_frame[i])  
            
        self.setLayout(vbox)
        self.setGeometry(300, 300, 450, 300)
        self.show()
    
    def value_change(self):
        for i in range(4):
            self.angle_label[i].setText(str(self.angle_slider[i].value()))
        
        servo_1_angle = (self.angle_slider[0].value()).to_bytes(1, 'big')
        servo_2_angle = (self.angle_slider[1].value()).to_bytes(1, 'big')
        servo_3_angle = (self.angle_slider[2].value()).to_bytes(1, 'big')
        servo_4_angle = (self.angle_slider[3].value()).to_bytes(1, 'big')

        self.serial.write(servo_1_id)
        self.serial.write(servo_1_angle)
        
        self.serial.write(servo_2_id)
        self.serial.write(servo_2_angle)

        self.serial.write(servo_3_id)
        self.serial.write(servo_3_angle)

        self.serial.write(servo_4_id)
        self.serial.write(servo_4_angle)

    def receive(self):
        dummy = self.serial.readAll()

app = QApplication(sys.argv)
ex =Window()

sys.exit(app.exec())