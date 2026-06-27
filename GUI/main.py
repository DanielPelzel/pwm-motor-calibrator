import queue

import PyQt5
import serial
from PyQt5.QtCore import Qt, QRunnable, QThreadPool, QThread
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QSlider, QComboBox, QVBoxLayout, QHBoxLayout, QLabel, \
    QSpinBox
import sys

try:
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
except serial.SerialException:
    ser = None


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Motor-Calibration")
        self.setMinimumSize(600, 200)

        #---Threding---
        self.worker = Worker(ser)
        self.worker.start()



        #--- Slider Widget---
        self.sliderWidget = QSlider(Qt.Horizontal)
        self.sliderWidget.setValue(0)
        self.sliderWidget.setMinimum(10)
        self.sliderWidget.setMaximum(100)
        self.sliderWidget.setSingleStep(1)
        self.sliderWidget.setRange(0, 4095)


        #---show Value Widget---
        self.valueWidget = QLabel(f"PWM: 0")
        self.sliderWidget.valueChanged.connect(self.showValue)

        #---RES-Dropdown-Widget---
        res_Widget = QComboBox()
        res_Widget.addItems(["8-bit", "10-bit", "12-bit", "13-bit"])
        res_Widget.setCurrentText("12-bit")
        res_Widget.currentTextChanged.connect(self.updateSlider)


        #---FREQ SpinBox Widget
        spinbxWidget = QSpinBox()
        spinbxWidget.setRange(50,20000)
        spinbxWidget.setSingleStep(10)
        spinbxWidget.valueChanged.connect(self.updateFreq)
        spinbxWidget.setValue(1000)


        # ---layout---
        layout1 = QVBoxLayout()  # Oben unten
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()

        layout1.addLayout(layout2)
        layout1.addLayout(layout3)
        layout3.addWidget(self.sliderWidget)
        layout3.addWidget(self.valueWidget)
        layout2.addWidget(res_Widget)
        layout2.addWidget(spinbxWidget)

        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)

        #TODO Funktion send_PWM() schreiben. Sendet akutellen PWM Wert per Serial



    def showValue(self, i):
        self.valueWidget.setText(f"PWM: {i}")
        self.worker.send(f"PWM:{i}\n")

    def updateSlider(self, i):
        if i == "8-bit":
            self.sliderWidget.setRange(0,255)
        elif i == "10-bit":
            self.sliderWidget.setRange(0,1023)
        elif i == "12-bit":
            self.sliderWidget.setRange(0,4095)
        elif i == "13-bit":
            self.sliderWidget.setRange(0,8191)

        res = i.replace("-bit", "")
        self.worker.send(f"RES:{res}\n")

    def updateFreq(self, i):
        self.worker.send(f"FREQ:{i}\n")

class Worker(QThread):
    def __init__(self, ser):
        super().__init__()
        self.ser = ser
        self.queue = queue.Queue()
        self.running = True

    def send(self, command):
        self.queue.put(command)

    def run(self):
        while self.running == True:
            try:
                cmd = self.queue.get(timeout=0.1)
                if self.ser:
                    self.ser.write(cmd.encode())
                else:
                    print(f"MOCK: {cmd}")
            except queue.Empty:
                pass




app = QApplication(sys.argv)
window  = MainWindow()
window.show()
app.exec_()