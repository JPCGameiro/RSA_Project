import paho.mqtt.client as mqtt
import time, json, sys, multiprocessing as mp
from driving import drive_in_square, go_to_park, park, go_to_park2, park2, go_straight, go_back_tostart
from datetime import datetime
import sqlite3 as sql
import json, time
import random

canPark = []
finished = False

def on_connect(client, userdata, flags, rc):
    if rc==0: print("OBU"+str(client._client_id)[-2]+" connected")
    else: print("bad connection code=",rc)

def on_disconnect(client, userdata, flags, rc=0):
    print("OBU"+str(client._client_id)[-2]+": disconnected")

def on_message(client, userdata, msg):
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    denm=json.loads(m_decode)
    #verificar free parks in the demn
    if denm['fields']['denm']['situation']['eventType']['subCauseCode'] > 0:
        canPark[ int(str(client._client_id)[-2]) -1] = True
    else:
        canPark[ int(str(client._client_id)[-2]) -1] = False


def get_spot_free_spotnum(broker, vtype, id):
    db = sql.connect('../park.db')
    crs = db.cursor()
    crs.execute('select point from Park where state = -1 and ip = "{b}" and vtype = {v}'.format(b=broker, v=vtype))
    pnt = crs.fetchone()[0]
    crs.execute('select lat, long from coordinate where point = {v}'.format(v=pnt))
    cdrs = crs.fetchone()
    print("OBU"+str(id)+": I am goin park at "+str(cdrs[0])+" , "+str(cdrs[1]))
    if (cdrs[0] == 40.631637 or cdrs[0] == 40.6318569):
        return 1
    elif(cdrs[0] == 40.631648 or crds[0] == 40.631840):
        return 2
    elif (cdrs[0] == 40.631662):
        return 3

#Couse 1 -> try to park in parking 1
def course1(cam, obu, id):
    drive_in_square(cam, 4, obu, id)
    go_to_park(cam, obu, id)
    if(canPark[id-1] == True):
        i = get_spot_free_spotnum("192.168.98.10", 5, id)
        print("OBU"+str(id)+": I am parking at spot "+str(i))
        park(i, cam, obu, id)
        print("OBU"+str(id)+": I am parked")
        for x in range(1, 100):
            cam['timestamp'] = datetime.timestamp(datetime.now())
            cam['speed'] = 0
            obu.publish("vanetza/in/cam", json.dumps(cam))
            time.sleep(0.5)
        return True
    return False

#Couse 2 -> try to park in parking 2
def course2(cam, obu, id):
    go_to_park2(cam, obu, id) 
    if(canPark[id-1] == True):
        i = get_spot_free_spotnum("192.168.98.20", 5, id)
        park2(i, cam, obu, id)
        for x in range(1, 100):
            cam['timestamp'] = datetime.timestamp(datetime.now())
            cam['speed'] = 0
            obu.publish("vanetza/in/cam", json.dumps(cam))
            time.sleep(0.5)
        return True
    return False


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
    cam['stationID'] = id+1
    
    #Generate a random number to choose a randomly one of the paths to travel
    rand = random.randint(1, 3)
    print("OBU"+str(id)+": I am goint for course "+str(rand))
    #Generate random delay (1 or 2 or 3 seconds)
    time.sleep(random.randint(1, 10)*id)
    
    if( rand == 1 or rand == 2):
        if not course1(cam, obu, id):
            print("OBU"+str(id)+": I cannot park because it's full")
            go_straight(cam, obu, id)
            course2(cam, obu, id)
    elif( rand == 3):
        if not course2(cam, obu, id):
            print("OBU"+str(id)+": I cannot park because it's full")
            go_back_tostart(cam, obu, id)
            course1(cam, obu, id)


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
    canPark.append(False)
    obu_init_simul([("192.168.98.30", 1), ("192.168.98.40", 2), ("192.168.98.50", 3)])

