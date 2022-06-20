import paho.mqtt.client as mqtt
import sqlite3 as sql
import time, json, sys, multiprocessing as mp
from datetime import datetime


park_occp = []


#callbacks
def on_connect1(client, userdata, flags, rc):
    if rc==0: print("RSU1: connected")
    else: print("bad connection code=",rc)

def on_disconnect1(client, userdata, flags, rc=0):
    print("RSU1: disconnected")
    client.dcnt_flag = False

def on_connect2(client, userdata, flags, rc):
    if rc==0: print("RSU2: connected")
    else: print("bad connection code=",rc)

def on_disconnect2(client, userdata, flags, rc=0):
    print("RSU2: disconnected")
    client.dcnt_flag = False


#On message for RSU1
def on_message1(client, userdata, msg):
    #Process Message
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    cam=json.loads(m_decode)
    brk = client._client_id.decode("utf-8")

    #Check for cars in the area around
    if verflocal(40.631491, cam['latitude'], -8.656481, cam['longitude']):
        #If speed is 0 means car is driving
        if cam['speed'] != 0:
            print("RSU1: I detected a car driving with id "+str(cam['stationID']))
            #driving out of the park
            if cam['stationID'] in park_occp: 
                park_occp.pop(cam['stationID'])
                parkout(cam['latitude'], cam['longitude'])
            #driving in the road
            else:
                #Check park availability and aswer with denm
                free_prks = verfFreePark(brk, cam['stationType'])
                sendDenm(client, free_prks)
		#Car is stopped
        else: 
            #Check if car is stopped in a parking spot 
            print("RSU1: I detected a car parked")
            if not cam['stationID'] in park_occp:
                #add occupied parking spot
                park_occp.append(cam['stationID'])
                parkin(cam['latitude'], cam['longitude'], cam['stationID'])
                free_prks = verfFreePark(brk, cam['stationType'])
                print("RSU1: Parking was registered, now there are only "+str(free_prks)+" free spots")
                sendDenm(client, free_prks)



#On message for RSU2
def on_message2(client, userdata, msg):
    #Process Message
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    cam=json.loads(m_decode)
    brk = client._client_id.decode("utf-8")

    #Check for cars in the area around
    if verflocal(40.631824, cam['latitude'], -8.657713, cam['longitude']):
        #If speed is 0 means car is driving
        if cam['speed'] != 0:
            print("RSU2: I detected a car driving with id "+str(cam['stationID']))
            #driving out of the park
            if cam['stationID'] in park_occp: 
                park_occp.pop(cam['stationID'])
                parkout(cam['latitude'], cam['longitude'])
            #driving in the road
            else:
                #Check park availability and aswer with denm
                free_prks = verfFreePark(brk, cam['stationType'])
                sendDenm(client, free_prks)
		#Car is stopped
        else: 
            #Check if car is stopped in a parking spot 
            print("RSU2: I detected a car parked")
            if not cam['stationID'] in park_occp:
                #add occupied parking spot
                print("RSU2: at "+brk+" is registering parked car at "+str(cam['latitude'])+" "+str(cam['longitude']))
                park_occp.append(cam['stationID'])
                parkin(cam['latitude'], cam['longitude'], cam['stationID'])
                free_prks = verfFreePark(brk, cam['stationType'])
                print("RSU2: Parking was registered, now there are only "+str(free_prks)+" free spots")
                sendDenm(client, free_prks)
        
    

def verflocal(lat, vlat, log, vlong):
    return 0.0000001 >= (pow(vlat - lat, 2) + pow(vlong - log, 2))

def verfFreePark(broker, vtype):
    db = sql.connect('park.db')
    crs = db.cursor()
    crs.execute('select count(*) from park where state = -1 and ip = "{b}" and vtype = {v}'.format(b=broker, v=vtype))
    cnt = crs.fetchone()
    return cnt[0]

def parkin(lat, long, stationId):
    db = sql.connect('park.db')
    crs = db.cursor()
    crs.execute('select point from coordinate where lat = "{lat}" and long = {long}'.format(lat=lat, long=long))
    crs.execute('update park set state = {stationId} where point = {pnt}'.format(stationId=stationId, pnt=crs.fetchone()[0]))
    db.commit()

def parkout(lat, long):
    db = sql.connect('park.db')
    crs = db.cursor()
    crs.execute('select point from coordinate where lat = "{lat}" and long = {long}'.format(lat=lat, long=long))
    crs.execute('update park set state = 0 where point = {pnt}'.format(crs.fetchone()[0]))
    db.commit()

def sendDenm(rsu, prks):
    f = open('denm.json')    
    denm = json.load(f)
    denm['management']['actionID']['sequenceNumber'] += 1
    denm['situation']['eventType']['subCauseCode'] = prks
    denm['detectionTime'] = datetime.timestamp(datetime.now())
    denm['referenceTime'] = datetime.timestamp(datetime.now())
    rsu.publish("vanetza/in/denm", json.dumps(denm))
    f.close()
    



def rsu_process(broker, id):
    rsu = mqtt.Client(broker)
    if id == 1:
        rsu.on_connect = on_connect1
        rsu.on_disconnect = on_disconnect1
        rsu.on_message = on_message1
    else: 
        rsu.on_connect = on_connect2
        rsu.on_disconnect = on_disconnect2
        rsu.on_message = on_message2
    
    rsu.loop_start()
    rsu.connect(broker)

    while(True):
        rsu.subscribe('vanetza/out/cam')
        time.sleep(1)  
    print("RSU"+str(id)+": Simulation finished")
    rsu.loop_stop()
    rsu.disconnect()
    

def rsu_init_simul(broker_rsus):
    mqtt.Client.dcnt_flag = True
	
    proc_list = []
    #Add station 6 as parked for the moment
    park_occp.append(6)
    for brk in broker_rsus:
        rsuProc = mp.Process(target=rsu_process, args=[brk[0], brk[1]])
        rsuProc.start()
        proc_list.append(rsuProc)


    for rsuProc in proc_list:   
        rsuProc.join()


if(__name__ == '__main__'):
    rsu_init_simul([("192.168.98.10", 1), ("192.168.98.20",2)])

