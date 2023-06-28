import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TRIG=20
ECHO=21
buzzerPin=13
print("후방 감지기")

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(buzzerPin,GPIO.OUT)

buzz=GPIO.PWM(buzzerPin,440)

GPIO.output(TRIG,False)
print("초음파 초기화")
time.sleep(2)

try:
	while True:
		GPIO.output(TRIG,True)
		time.sleep(0.00001)
		GPIO.output(TRIG,False)

		while GPIO.input(ECHO)==0:
			start=time.time()

		while GPIO.input(ECHO)==1:
			stop=time.time()

		check_time=stop-start
		distance = check_time * 34300/2
		print("Distance : %.1f cm" %distance)

		if distance<=20:
			buzz.start(50)
			if distance<=10:
				buzz.ChangeFrequency(1000)
				time.sleep(0.1)
				buzz.stop()
			elif distance<=15:
				buzz.ChangeFrequency(700)
				time.sleep(0.1)
				buzz.stop()
			else:
				buzz.ChangeFrequency(500)
				time.sleep(0.1)
				buzz.stop()
		else:
			buzz.stop()

		time.sleep(0.4)
		
except KeyboardInterrupt:
	print("거리 측정 완료")
	GPIO.cleanup()
