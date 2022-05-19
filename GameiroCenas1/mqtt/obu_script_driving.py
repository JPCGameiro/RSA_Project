import paho.mqtt.client as mqtt
import time, json, sys, multiprocessing as mp
from driving import drive_in_square, go_to_park, park
import sqlite3 as sql

canPark = True 

def on_connect(client, userdata, flags, rc):
    if rc==0: print("connected")
    else: print("bad connection code=",rc)

def on_disconnect(client, userdata, flags, rc=0):
    print("disconnected")

def on_message(client, userdata, msg):
    print("\ni received a DENM\n")
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    denm=json.loads(m_decode)
    
    #verificar free parks in the demn
    if denm['fields']['denm']['situation']['eventType']['subCauseCode'] > 0:
        canPark = True
    else:
        canPark = False


def get_spot_free_spotnum(broker, vtype):
    db = sql.connect('park.db')
    crs = db.cursor()
    crs.execute('select point from Park where state = -1 and ip = "{b}" and vtype = {v}'.format(b=broker, v=vtype))
    pnt = crs.fetchone()[0]
    crs.execute('select lat, long from coordinate where point = {v}'.format(v=pnt))
    cdrs = crs.fetchone()
    print("You can park at"+str(cdrs[0])+" , "+str(cdrs[1]))
    if (cdrs[0] == 40.631637):
        return 1
    elif(cdrs[0] == 40.631648):
        return 2
    elif (cdrs[0] == 40.631662):
        return 3	


def obu_process(broker):
    obu = mqtt.Client("obu")
    obu.on_connect = on_connect
    obu.on_disconnect = on_disconnect
    obu.on_message = on_message

    obu.loop_start()
    obu.connect(broker)

    f = open('driving.json')    
    cam = json.load(f)
    
    #obu.subscribe("vanetza/out/cam")
    while(True):
        drive_in_square(cam, 4, obu)
        #go_to_park()
        time.sleep(4)
        if(canPark):
            i = get_spot_free_spotnum("192.168.98.10", 5)
            print("You park at spot"+str(i))
            park(i, cam, obu)
        print("Circuit Finished")
        break
    f.close()
    
    obu.loop_stop()
    obu.disconnect()


def main():
    #clients OBUs
    broker_obus = ["192.168.98.40"]

    proc_list = []
    for brk in broker_obus:
        obuProc = mp.Process(target=obu_process, args=[brk]) 
        obuProc.start()
        proc_list.append(obuProc)

    for obuProc in proc_list:   
        obuProc.join()   
    

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
