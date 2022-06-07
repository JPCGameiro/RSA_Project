import paho.mqtt.client as mqtt
import time, json, sys, multiprocessing as mp
from datetime import datetime


def on_connect(client, userdata, flags, rc):
    if rc==0: print("connected")
    else: print("bad connection code=",rc)

def on_disconnect(client, userdata, flags, rc=0):
    print("disconnected")

def on_message(client, userdata, msg):
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    denm=json.loads(m_decode)
    
    '''
    #verificar free parks no demn
    if denm[''] > 0:
        #estacionar!!
        pass
    else:
        pass
    ''' 

def obu_process(broker):
    obu = mqtt.Client("obu")
    obu.on_connect = on_connect
    obu.on_disconnect = on_disconnect
    obu.on_message = on_message

    obu.loop_start()
    obu.connect(broker)
	
	#Open parked json format
    f = open('parked.json')    
    cam = json.load(f)
    
    #Parked car (in spot 3) sends every 0.5 second a CAM
    while(True):
        cam['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(cam))
        obu.subscribe("vanetza/out/denm")
        time.sleep(1)
    f.close()
    
    obu.loop_stop()
    obu.disconnect()



def main():
    #clients OBUs
    broker_obus = ["192.168.98.30"]

    proc_list = []
    for brk in broker_obus:
        obuProc = mp.Process(target=obu_process, args=[brk]) 
        obuProc.start()
        proc_list.append(obuProc)

    for obuProc in proc_list:   
        obuProc.join()   
    

if(__name__ == '__main__'):
    main()










class OBU:

    def __init__(self, broker):
        self.broker = broker
        self.obu = mqtt.Client("obu")
        self.obu.on_connect = on_connect
        self.obu.on_disconnect = on_disconnect
        self.obu.on_message = on_message

    def connect(self):
        self.obu.loop_start()
        self.obu.connect(self.broker)

    def send_cam(self):
        f = open('cam.json')    
        cam = json.load(f)
        self.obu.publish("vanetza/in/cam", json.dumps(cam))
        f.close()

    def disconnect(self):
        self.obu.loop_stop()
        self.obu.disconnect()

    def getBroker(self):
        return self.broker
