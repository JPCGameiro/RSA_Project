import paho.mqtt.client as mqtt
import sqlite3 as sql
import time, json, sys, multiprocessing as mp
from datetime import datetime


park_occp = []
canPark = True


#callbacks
def on_connect(client, userdata, flags, rc):
    if rc==0: print("RSU: connected")
    else: print("bad connection code=",rc)

def on_disconnect(client, userdata, flags, rc=0):
    print("RSU: disconnected")
    client.dcnt_flag = False

def on_message(client, userdata, msg):
    #Process Message
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    cam=json.loads(m_decode)
    brk = client._client_id.decode("utf-8")

    #Check for cars in the area around
    if verflocal(40631491, cam['latitude'], -8656481, cam['longitude']):
        #If speed is 0 means car is driving
        if cam['speed'] != 0:
            print("RSU: I detected a car driving")
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
            print("RSU: I detected a car parked")
            if not cam['stationID'] in park_occp:
                #add occupied parking spot
                park_occp.append(cam['stationID'])
                parkin(cam['latitude'], cam['longitude'], cam['stationID'])
                free_prks = verfFreePark(brk, cam['stationType'])
                print("RSU: Parking was registered, now there are only "+str(free_prks)+" free spots")

        
    

def verflocal(lat, vlat, log, vlong):
    return 0.000005 >= (pow(vlat*0.000001 - 0.000001*lat, 2) - pow(vlong*0.000001 - 0.000001*log, 2))

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

def sendDenm(rsu, prks):
    f = open('denm.json')    
    denm = json.load(f)
    denm['management']['actionID']['sequenceNumber'] += 1
    denm['subCauseCode'] = prks
    denm['detectionTime'] = datetime.timestamp(datetime.now())
    denm['referenceTime'] = datetime.timestamp(datetime.now())
    rsu.publish("vanetza/in/denm", json.dumps(denm))
    f.close()
    



def rsu_process(broker):
    rsu = mqtt.Client(broker)
    rsu.on_connect = on_connect
    rsu.on_disconnect = on_disconnect
    rsu.on_message = on_message

    rsu.loop_start()
    rsu.connect(broker)

    while(True):
        rsu.subscribe('vanetza/out/cam')
        time.sleep(1)  
    print("RSU: Simulation finished")
    rsu.loop_stop()
    rsu.disconnect()
    

def rsu_init_simul(broker_rsus):
    #client RSU
    #broker_rsus = ["192.168.98.10"]
    mqtt.Client.dcnt_flag = True
	
    proc_list = []
    #Add station 2 as parked for the moment
    park_occp.append(2)
    for brk in broker_rsus:
        rsuProc = mp.Process(target=rsu_process, args=[brk])
        rsuProc.start()
        proc_list.append(rsuProc)


    for rsuProc in proc_list:   
        rsuProc.join()


if(__name__ == '__main__'):
    rsu_init_simul(["192.168.98.10"])

