import sys
import RPi.GPIO as GPIO
import time
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# LED
ledPin=6
# 부저
buzzerPin = 13
# 초음파 감지 
TRIG=20
ECHO=21

GPIO.setmode(GPIO.BCM)
#LED
GPIO.setup(ledPin,GPIO.OUT)
#부저
GPIO.setup(buzzerPin,GPIO.OUT)
#초음파
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
#440HZ 부저 객체
buzz=GPIO.PWM(buzzerPin, 440)
# 초음파 초기 설정
GPIO.output(TRIG,False)



class qtApp(QWidget):
    # ON/OFF 판단을 위한 bool 변수
    is_buzzer_on=False
    is_sonic_on=False
    def __init__(self):
        super().__init__()
        uic.loadUi('LEDBuzzer.ui',self)
        # 버튼 슬롯 함수
        self.btn_ledOn.clicked.connect(self.btnLEDOnClicked)
        self.btn_ledOff.clicked.connect(self.btnLEDOffClicked)
        self.btn_buzzerOn.clicked.connect(self.btnBuzzerOnClicked)
        self.btn_buzzerOff.clicked.connect(self.btnBuzzerOffClicked)
        self.btn_sonicOn.clicked.connect(self.btnSonicOnClicked)
        self.btn_sonicOff.clicked.connect(self.btnSonicOffClicked)
        

    def btnLEDOnClicked(self):
        GPIO.output(ledPin,GPIO.HIGH)

    def btnLEDOffClicked(self):
        GPIO.output(ledPin,GPIO.LOW)
    
    def btnBuzzerOnClicked(self):
        buzz.start(50)

    def btnBuzzerOffClicked(self):
        buzz.stop()

    def btnSonicOnClicked(self):
        self.is_sonic_on=True
        while self.is_sonic_on:
            GPIO.output(TRIG,True)
            time.sleep(0.00001)
            GPIO.output(TRIG,False)

            while GPIO.input(ECHO)==0:
                start=time.time()

            while GPIO.input(ECHO)==1:
                stop=time.time()

            check_time=stop-start
            distance = check_time * 34300/2
            self.Lbl_sonic.setText('Distance : %.1f cm' %distance)
            QApplication.processEvents() #UI 업데이트 위해 필요함


    def btnSonicOffClicked(self):
        self.is_sonic_on=False
        self.Lbl_sonic.setText('')

if __name__=='__main__':
    app=QApplication(sys.argv)
    ex=qtApp()
    ex.show()
    sys.exit(app.exec_())