import paho.mqtt.client as mqtt
import sqlite3 as sql
import time, json, sys, multiprocessing as mp





#callbacks
def on_connect(client, userdata, flags, rc):
    if rc==0: print("connected")
    else: print("bad connection code=",rc)

def on_disconnect(client, userdata, flags, rc=0):
    print("disconnected")
    client.dcnt_flag = False

def on_message(client, userdata, msg):
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    m_in=json.loads(m_decode)
    print(m_in)
    #verificar carros na sua area
    #a entrar: 
    #verificar disponobilidade de lugares
    #verificar se estacinou, contador especif para avaliar se estacionou!!
    #responder com denm msg
    #a sair:
    #libertar lugares


def rsu_process(broker):
    rsu = mqtt.Client("rsu")
    rsu.on_connect = on_connect
    rsu.on_disconnect = on_disconnect
    rsu.on_message = on_message

    rsu.loop_start()
    rsu.connect(broker)

    print("dcnt flag value : {rsu.dcnt_flag}")
    while(rsu.dcnt_flag):
        rsu.subscribe('vanetza/out/cam')
        time.sleep(3)
    
    rsu.loop_stop()
    rsu.disconnect()
    

def main():
    #client RSU
    broker_rsus = ["192.168.98.10", "192.168.98.20"]
    mqtt.Client.dcnt_flag = True

    proc_list = []
    for brk in broker_rsus:
        rsuProc = mp.Process(target=rsu_process, args=[brk]) 
        rsuProc.start()
        proc_list.append(rsuProc)

    for rsuProc in proc_list:   
        rsuProc.join()


    '''
    rsu_dict = {}
    #Connect RSUs clients
    for brk in broker_rsus:
        rsu_dict[brk] = RSU(brk)
        rsu_dict[brk].connect()
    
    #disconnect RSUs clients
    for brk in broker_rsus:
        rsu_dict[brk].disconnect()
    '''

if(__name__ == '__main__'):
    main()




class RSU:
    db = sql.connect('park.db')

    def __init__(self, lat, long, broker):
        self.lat = lat
        self.long = long
        self.broker = broker
        self.rsu = mqtt.Client("obu")
        self.rsu.on_connect = on_connect
        self.rsu.on_disconnect = on_disconnect
        self.rsu.on_message = on_message

    #connect RSU
    def connect(self):
        self.rsu.loop_start()
        self.rsu.connect(self.broker)

    #send cam message
    def sendCam(self):
        f = open('cam.json')    
        cam = json.load(f)
        self.rsu.publish("vanetza/in/cam", json.dumps(cam))
        f.close()

    #send denm message
    def sendDemn(self):
        f = open('denm.json')    
        denm = json.load(f)
        self.rsu.publish("vanetza/in/denm", json.dumps(denm))
        f.close()
    

    #verifies db if the vehicle is in the range of it's operation
    def verifyLocal(self):
        self.db.execute('')

    #verifies if the parking lot has space for the vehicle
    def verifyParks(self):
        self.db.execute('')

    #disconnect RSU
    def disconnect(self):
        self.rsu.loop_stop()
        self.rsu.disconnect()

    #getter broker
    def getBroker(self):
        return self.broker