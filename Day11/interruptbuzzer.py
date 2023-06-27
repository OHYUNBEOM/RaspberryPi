import RPi.GPIO as GPIO
import time

swPin=24
ledPin=6
buzzerPin=13
melody=[500,300]

GPIO.setmode(GPIO.BCM)
GPIO.setup(swPin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ledPin,GPIO.OUT)
GPIO.setup(buzzerPin,GPIO.OUT) 

buzz=GPIO.PWM(buzzerPin,440)

ledState=False
buzzerState=False

def callbackfunc(channel):
	global ledState
	ledState = not ledState
	global buzzerState
	buzzerState = not buzzerState
	print("LED State:",ledState)
	print("buzzer State:",buzzerState)

GPIO.add_event_detect(swPin,GPIO.RISING,callback=callbackfunc)

try:
	while True:
		GPIO.output(ledPin,ledState)
		if buzzerState==True:
			buzz.start(50)
			for i in range(0,len(melody)):
				buzz.ChangeFrequency(melody[i])
				time.sleep(0.3)
		else:
			buzz.stop()
except KeyboardInterrupt:
	GPIO.cleanup()
