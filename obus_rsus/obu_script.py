import paho.mqtt.client as mqtt
import time, json, sys, multiprocessing as mp
from driving import drive_in_square, go_to_park, park
from datetime import datetime
import sqlite3 as sql
import json

canPark = []
finished = False

def on_connect(client, userdata, flags, rc):
    if rc==0: print("OBU"+int(str(obu._client_id)[-2])+" connected")
    else: print("bad connection code=",rc)

def on_disconnect(client, userdata, flags, rc=0):
    print("OBU"+int(str(obu._client_id)[-2])+": disconnected")

def on_message(client, userdata, msg):
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    denm=json.loads(m_decode)
    
    #verificar free parks in the demn
    if denm['fields']['denm']['situation']['eventType']['subCauseCode'] > 0:
        canPark[ int(str(obu._client_id)[-2]) -1] = True
    else:
        canPark[ int(str(obu._client_id)[-2]) -1] = False


def get_spot_free_spotnum(broker, vtype, id):
    db = sql.connect('park.db')
    crs = db.cursor()
    crs.execute('select point from Park where state = -1 and ip = "{b}" and vtype = {v}'.format(b=broker, v=vtype))
    pnt = crs.fetchone()[0]
    crs.execute('select lat, long from coordinate where point = {v}'.format(v=pnt))
    cdrs = crs.fetchone()
    print("OBU"+id+": I am goin park at "+str(cdrs[0])+" , "+str(cdrs[1]))
    if (cdrs[0] == 40.631637):
        return 1
    elif(cdrs[0] == 40.631648):
        return 2
    elif (cdrs[0] == 40.631662):
        return 3	


def obu_process(broker, id):
    obu = mqtt.Client(client_id="obu"+str(id))
    obu.on_connect = on_connect
    obu.on_disconnect = on_disconnect
    obu.on_message = on_message
    
    #connect to the broker
    obu.loop_start()
    obu.connect(broker)

    #Load cam json tamplate
    f = open('driving.json')    
    cam = json.load(f)
    
    #drive_in_square(cam, 4, obu, 2)
    go_to_park(cam, obu, id)
    time.sleep(1)
    if(canPark[id-1] == True):
        i = get_spot_free_spotnum("192.168.98.10", 5, id)
        print("OBU"+str(id)+": I am parking at spot "+str(i))
        park(i, cam, obu, id)
        print("OBU"+str(id)+": I am parked")
    else:
        print("OBU"+str(id)+": I cannot park because it's full")

	
    for x in range(1, 20):
        cam['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(cam))
        time.sleep(0.5)
    print("OBU"+str(id)+": Simulation finished")

    obu.loop_stop()
    obu.disconnect()


def obu_init_simul(broker_obus):
    proc_list = []
    for brk in broker_obus:
        obuProc = mp.Process(target=obu_process, args=[brk[0], brk[1]]) 
        obuProc.start()
        proc_list.append(obuProc)

    for obuProc in proc_list:   
        obuProc.join()   
    

if(__name__ == '__main__'):
    canPark.append(False)
    canPark.append(False)
    obu_init_simul([("192.168.98.20", 1), ("192.168.98.30", 2)])

