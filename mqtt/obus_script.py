import paho.mqtt.client as mqtt
import time, json, sys, multiprocessing as mp


def on_connect(client, userdata, flags, rc):
    if rc==0: print("connected")
    else: print("bad connection code=",rc)

def on_disconnect(client, userdata, flags, rc=0):
    print("disconnected")

def on_message(client, userdata, msg):
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    m_in=json.loads(m_decode)
    #verificar demn


def obu_process(broker):
    obu = mqtt.Client("obu")
    obu.on_connect = on_connect
    obu.on_disconnect = on_disconnect
    obu.on_message = on_message

    obu.loop_start()
    obu.connect(broker)

    f = open('cam.json')    
    cam = json.load(f)
    for _ in range(10):
        obu.publish("vanetza/in/cam", json.dumps(cam))
        time.sleep(3)
    f.close()
    
    obu.loop_stop()
    obu.disconnect()



def main():
    #clients OBUs
    broker_obus = ["192.168.98.30", "192.168.98.40", "192.168.98.50"]

    proc_list = []
    for brk in broker_obus:
        obuProc = mp.Process(target=obu_process, args=[brk]) 
        obuProc.start()
        proc_list.append(obuProc)

    for obuProc in proc_list:   
        obuProc.join()


    '''
    obu_dict ={}
    run = True
    while(run):
        
        for brk in broker_obus:
            obu_dict[brk] = OBU(brk)
            obu_dict[brk].connect()

        for brk in broker_obus:
            obu_dict[brk].disconnect()
    '''    
    

if(__name__ == '__main__'):
    main()




#
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
