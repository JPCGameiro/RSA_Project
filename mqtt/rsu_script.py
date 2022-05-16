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
    cam=json.loads(m_decode)
    brk = client._client_id.decode("utf-8")
    
    park_occp = []
    #verificar carros na sua area
    if verflocal(40.631491, cam['latitude'], -8.656481, cam['longitude']):
        if cam['speed'] != 0:
            if cam['stationID'] in park_occp: 
                park_occp.pop(cam['stationID'])
            else:
                #verificar disponobilidade de lugares
                free_prks = verfFreePark(brk, cam['stationType'])
                #responder com denm msg
        else: 
            #verificar se esta num dos parques
            #add parks ocupados
            pass
    

def verflocal(lat, vlat, long, vlong):
    return 0.000005 >= (pow(vlat - lat, 2) - pow(vlong - long, 2))

def verfFreePark(broker, vtype):
    db = sql.connect('park.db')
    crs = db.cursor()
    crs.execute('select count(distinct point) from Park where ip = "{b}" and vtype = {v}'.format(b=broker, v=vtype))
    cnt = crs.fetchone()
    return cnt[0]


def rsu_process(broker):
    rsu = mqtt.Client(broker)
    rsu.on_connect = on_connect
    rsu.on_disconnect = on_disconnect
    rsu.on_message = on_message

    rsu.loop_start()
    rsu.connect(broker)

    print("dcnt flag value : {rsu.dcnt_flag}")
    while(rsu.dcnt_flag):
        rsu.subscribe('vanetza/out/cam')
        time.sleep(2)
    
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








#rsu1: 40.631491, -8.656481
class RSU:
    db = sql.connect('park.db')

    def __init__(self, parkingLot, lat, long, broker):
        self.parkingLot = parkingLot
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
    def verifyLocal(self, vlat, vlong):
        return 100 >= pow(vlat - self.lat, 2) - pow(vlong - self.long, 2)

    #verifies if the parking lot has space for the vehicle
    def verifyFreeParks(self, vtype, vprio):
        self.db.execute('select point form Park where park = %s and vehicle = %s and priority = %s limit 1', self.parkingLot, vtype, vprio)
        

    #disconnect RSU
    def disconnect(self):
        self.rsu.loop_stop()
        self.rsu.disconnect()

    #getter broker
    def getBroker(self):
        return self.broker