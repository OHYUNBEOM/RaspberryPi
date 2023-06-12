# LED 깜빡이기
import RPi.GPIO as GPIO
import time

signal_pin=18

#GPIO.setmode(GPIO.BOARD) # GPIO 구조 빵판 1~40번
GPIO.setmode(GPIO.BCM) # GPIO 18, GROUND
GPIO.setup(signal_pin,GPIO.OUT) # GPIO 18번 pin에 출력 설정

while(True):
    GPIO.output(signal_pin,True) # GPIO 18번 pin에 전압 시그널 ON
    time.sleep(2) # 2초동안 불킴
    GPIO.output(signal_pin,False) # GPIO 18번 pin에 전압 시그널 OFF 
    time.sleep(1) # 1초동안 불 끈 상태로 대기