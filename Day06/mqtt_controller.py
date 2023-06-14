# MQTT 패키지 설치 - paho-mqtt
# sudo pip install paho-mqtt
# 동시에 publish / subscribe
from threading import Thread,Timer
import time # time.sleep()
import paho.mqtt.client as mqtt
import json
import datetime as dt
import Adafruit_DHT as dht

sensor=dht.DHT11
rcv_pin=10


class publisher(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.host='210.119.12.69' # ipconfig / ipv4 주소
        self.port=1883
        self.clientId='IOT69' 
        print('publisher 스레드 시작')
        self.client=mqtt.Client(client_id=self.clientId)

    def run(self):
        self.client.connect(self.host, self.port)
        self.publish_data_auto()
    
    def publish_data_auto(self):
        humid,temp=dht.read_retry(sensor, rcv_pin)
        curr=dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        origin_data = {'DEV_ID':self.clientId,
                       'CURR_DT':curr,
                       'TYPE':'TEMP&HUMID',
                       'STAT': f'{temp}|{humid}'} # sample data
        pub_data = json.dumps(origin_data) # MQTT로 전송할 json 데이터로 변환
        self.client.publish(topic='pknu/rpi/control/',payload=pub_data)
        print('Data Published')
        Timer(2.0,self.publish_data_auto).start()

class subscriber(Thread):
    pass

if __name__=='__main__':
    thPub=publisher() # publisher 객체 생성
    thPub.start() # run() 자동실행