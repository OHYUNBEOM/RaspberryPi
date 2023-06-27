import RPi.GPIO as GPIO
import time

swPin=24
ledPin=6

GPIO.setmode(GPIO.BCM)
GPIO.setup(swPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #스위치핀: 입력
GPIO.setup(ledPin,GPIO.OUT) #LED핀:출력

ledState=False  #LED상태변수, 초기상태 : False

def callbackfunc(channel):
	global ledState
	ledState = not ledState #함수 호출마다 ledState를 반전
	GPIO.output(ledPin,ledState) #함수 호출마다 ledPin을 True와 False로 출력
	print("LED State : ",ledState)

GPIO.add_event_detect(swPin, GPIO.RISING, callback=callbackfunc)
# 스위치 핀의 상승(RISING)을 감지, 감지되면 callbackfunc() 함수를 호출
try:
	while True:
		pass
except KeyboardInterrupt:
	GPIO.cleanup()
