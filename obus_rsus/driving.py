from datetime import datetime
import sqlite3 as sql
import json
import time

def update_db(lat, long, id):
    db = sql.connect('../obu.db')
    obu_ip = ""
    if(id=='obu1'): obu_ip = "192.168.98.30"
    elif(id=='obu2'): obu_ip = "192.168.98.40"
    elif(id=='obu3'): obu_ip = "192.168.98.50"
    elif(id=='obu4'): obu_ip = "192.168.98.60"
    db.execute('update obu set lat = {la}, long = {lo} where ip = "{ip}";'.format(la = lat, lo=long, ip = obu_ip))
    db.commit()

#Go in square through all 4 points
def drive_in_square(data, point, obu, id):
    
    #0.1 seconds to dely for 10 Hz frequency in message generation
    while(data['longitude'] <= -8.655763):
        obu.subscribe("vanetza/out/denm")
        time.sleep(0.1)
        data['longitude'] += 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
        #update obu database
        update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
    while(data['latitude'] <= 40.633209):
        obu.subscribe("vanetza/out/denm")
        time.sleep(0.1)
        data['latitude'] += 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
        #update obu database
        update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
    print("OBU"+str(id)+": I am at point 1")
    if(point == 1):
        return None

    while(data['longitude'] <= -8.654387):
        time.sleep(0.1)
        data['longitude'] += 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
        #update obu database
        update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
    while(data['latitude'] <= 40.630577):
        time.sleep(0.1)
        data['latitude'] -= 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
        #update obu database
        update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
    print("OBU"+str(id)+": I am at point 2")
    if(point == 2):
        return None

    while(data['longitude'] >= -8.654894):
        time.sleep(0.1)
        data['longitude'] -= 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
        #update obu database
        update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
    while(data['latitude'] >= 40.630007):
        time.sleep(0.1)
        data['latitude'] -= 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
        #update obu database
        update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
    print("OBU"+str(id)+": I am at point 3")
    if(point == 3):
        return None

    while(data['longitude'] >= -8.657125):
        time.sleep(0.1)
        data['longitude'] -= 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
        #update obu database
        update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
    while(data['latitude'] >= 40.631786):
        time.sleep(0.1)
        data['latitude'] += 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
        #update obu database
        update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
    print("OBU"+str(id)+": I am at point 4")




#Go to the park entrance
def go_to_park(data, obu, id):
    
	#Go around the first three points
    drive_in_square(data, 3, obu, id)

    #Go from point 3 to entrance of the parking
    while(data['longitude'] >= -8.656567):
        obu.subscribe("vanetza/out/denm")
        time.sleep(0.1)
        data['longitude'] -= 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
        #update obu database
        update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
    while(data['latitude'] <= 40.631420):
        obu.subscribe("vanetza/out/denm")
        time.sleep(0.1)
        data['latitude'] += 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
        #update obu database
        update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
    print("OBU"+str(id)+": I'm At the parking 1 entrance")






#if a spot is not available go from the park entrance to the point 4
def go_straight(data, obu, id):
    
    #Go from point entrance of the park to point 4
    while(data['longitude'] >= -8.657125):
        obu.subscribe("vanetza/out/denm")
        time.sleep(0.1)
        data['longitude'] -= 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
        #update obu database
        update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
    while(data['latitude'] <= 40.631786):
        obu.subscribe("vanetza/out/denm")
        time.sleep(0.1)
        data['latitude'] += 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
        #update obu database
        update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
    print("OBU"+str(id)+": I'm At the point 4")






#Go to a spot in the parking lot 1
def park(spot, data, obu, id):
    
    #Go from entrance of the parking to cancelas of the park
    while(data['longitude'] <= -8.656521):
        obu.subscribe("vanetza/out/denm")
        time.sleep(0.1)
        data['longitude'] += 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
        #update obu database
        update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
    while(data['latitude'] <= 40.631503):
        obu.subscribe("vanetza/out/denm")
        time.sleep(0.1)
        data['latitude'] += 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
        #update obu database
        update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
    print("OBU"+str(id)+": I'm at the cancela")
    
    if(spot == 1):
        while(data['longitude'] <= -8.656507):
            time.sleep(0.1)
            data['longitude'] += 0.00001
            data['timestamp'] = datetime.timestamp(datetime.now())
            obu.publish("vanetza/in/cam", json.dumps(data))
            #update obu database
            update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
        while(data['latitude'] <= 40.631637):
            time.sleep(0.1)
            data['latitude'] += 0.00001
            data['timestamp'] = datetime.timestamp(datetime.now())
            obu.publish("vanetza/in/cam", json.dumps(data))
            #update obu database
            update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
        data['longitude'] = -8.656507
        data['latitude'] = 40.631637
        data['speed'] = 0
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
        #update obu database
        update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
        print("OBU"+str(id)+": Parked at SPOT1 in PARK1")
    elif(spot == 2):
        while(data['longitude'] >= -8.656529):
            time.sleep(0.1)
            data['longitude'] -= 0.00001
            data['timestamp'] = datetime.timestamp(datetime.now())
            obu.publish("vanetza/in/cam", json.dumps(data))
            #update obu database
            update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
        while(data['latitude'] <= 40.631648):
            time.sleep(0.1)
            data['latitude'] += 0.00001
            data['timestamp'] = datetime.timestamp(datetime.now())
            obu.publish("vanetza/in/cam", json.dumps(data))
            #update obu database
            update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
        data['longitude'] = -8.656529
        data['latitude'] = 40.631648
        data['speed'] = 0
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
        #update obu database
        update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
        print("OBU"+str(id)+": Parked at SPOT2 in PARK1")
    elif(spot == 3):
        while(data['longitude'] >= -8.656547):
            time.sleep(0.1)
            data['longitude'] -= 0.00001
            data['timestamp'] = datetime.timestamp(datetime.now())
            obu.publish("vanetza/in/cam", json.dumps(data))
            #update obu database
            update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
        while(data['latitude'] <= 40.631662):
            time.sleep(0.1)
            data['latitude'] += 0.00001
            data['timestamp'] = datetime.timestamp(datetime.now())
            obu.publish("vanetza/in/cam", json.dumps(data))
            #update obu database
            update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
        data['longitude'] = -8.656547
        data['latitude'] = 40.631662
        data['speed'] = 0
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
        #update obu database
        update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
        print("OBU"+str(id)+": Parked at SPOT3 in PARK1")






#Leave the parking lot and go to point 4
def leave_park(spot, data, obu, id):
    print("OBU"+str(id)+": I am leaving spot "+str(spot))
    #go to the park cancela
    if(spot == 1):
        while(data['longitude'] >= -8.656521):
            time.sleep(0.1)
            data['longitude'] -= 0.00001
            data['timestamp'] = datetime.timestamp(datetime.now())
            obu.publish("vanetza/in/cam", json.dumps(data))
            #update obu database
            update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
    else:
        while(data['longitude'] <= -8.656521):
            time.sleep(0.1)
            data['longitude'] += 0.00001
            data['timestamp'] = datetime.timestamp(datetime.now())  
            obu.publish("vanetza/in/cam", json.dumps(data))   
            #update obu database
            update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
    while(data['latitude'] >= 40.631503):
        time.sleep(0.1)
        data['latitude'] -= 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
        #update obu database
        update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
    print("OBU"+str(id)+": I'm na cancela")

    #Got to the starting point of the circuit
    while(data['longitude'] >= -8.657125):
        time.sleep(0.1)
        data['longitude'] -= 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
    while(data['latitude'] <= 40.631786):
        time.sleep(0.1)
        data['latitude'] += 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
    print("OBU"+str(id)+": I Left the park1 sucessfully")


#From point 1 got to park2 entrance
def go_to_park2(data, obu, id):
    
    while(data['longitude'] >= -8.657328):
        obu.subscribe("vanetza/out/denm")
        time.sleep(0.1)
        data['longitude'] -= 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
        #update obu database
        update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
    while(data['latitude'] >= 40.631622):
        obu.subscribe("vanetza/out/denm")
        time.sleep(0.1)
        data['latitude'] -= 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
        #update obu database
        update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
    print("OBU"+str(id)+": I am at point 5")

    while(data['longitude'] >= -8.657763):
        obu.subscribe("vanetza/out/denm")
        time.sleep(0.1)
        data['longitude'] -= 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
        #update obu database
        update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
    while(data['latitude'] <= 40.631890):
        obu.subscribe("vanetza/out/denm")
        time.sleep(0.1)
        data['latitude'] += 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
        #update obu database
        update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
    print("OBU"+str(id)+": I am at parking 2 entrance")


#Go to a spot in the parking lot 2
def park2(spot, data, obu, id):
    
    if(spot == 1):
        while(data['longitude'] >= -8.657833):
            obu.subscribe("vanetza/out/denm")
            time.sleep(0.1)
            data['longitude'] -= 0.00001
            data['timestamp'] = datetime.timestamp(datetime.now())
            obu.publish("vanetza/in/cam", json.dumps(data))
            #update obu database
            update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
        while(data['latitude'] >= 40.631857):
            obu.subscribe("vanetza/out/denm")
            time.sleep(0.1)
            data['latitude'] -= 0.00001
            data['timestamp'] = datetime.timestamp(datetime.now())
            obu.publish("vanetza/in/cam", json.dumps(data))
            #update obu database
            update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
        data['longitude'] = -8.657833
        data['latitude'] = 40.631857
        data['speed'] = 0
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
        #update obu database
        update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
        print("OBU"+str(id)+": Parked at SPOT1 in PARK2")
    else:
        while(data['longitude'] >= -8.657803):
            obu.subscribe("vanetza/out/denm")
            time.sleep(0.1)
            data['longitude'] -= 0.00001
            data['timestamp'] = datetime.timestamp(datetime.now())
            obu.publish("vanetza/in/cam", json.dumps(data))
            #update obu database
            update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
        while(data['latitude'] >= 40.631840):
            obu.subscribe("vanetza/out/denm")
            time.sleep(0.1)
            data['latitude'] -= 0.00001
            data['timestamp'] = datetime.timestamp(datetime.now())
            obu.publish("vanetza/in/cam", json.dumps(data))
            #update obu database
            update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
        data['longitude'] = -8.657803
        data['latitude'] = 40.631840
        data['speed'] = 0
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
        #update obu database
        update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
        print("OBU"+str(id)+": Parked at SPOT2 in PARK2")        


#Go from parking 2 entrance back to point 1
def go_back_tostart(data, obu, id):
    
    while(data['longitude'] >= -8.658624):
        obu.subscribe("vanetza/out/denm")
        time.sleep(0.1)
        data['longitude'] -= 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
        #update obu database
        update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
    while(data['latitude'] <= 40.633545):
        obu.subscribe("vanetza/out/denm")
        time.sleep(0.1)
        data['latitude'] += 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))  
        #update obu database
        update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
    print("OBU"+str(id)+": I am at point 5")

    while(data['longitude'] >= -8.657125):
        obu.subscribe("vanetza/out/denm")
        time.sleep(0.1)
        data['longitude'] -= 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
        #update obu database
        update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
    while(data['latitude'] >= 40.631786):
        obu.subscribe("vanetza/out/denm")
        time.sleep(0.1)
        data['latitude'] -= 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))  
        #update obu database
        update_db(data["latitude"], data["longitude"], obu._client_id.decode("utf-8"))
    print("OBU"+str(id)+": I am at point 1")  


#   CIRCUIT 1
#40.633209, -8.655763       40.630577, -8.654387
#                       40.630007, -8.654894
#40.631786, -8.657125  

#   CIRCUIT 2           
#    40.633545, -8.658624               40.631786, -8.657125
#                    40.631622, -8.657328

#Parking1 entrance: 40.631420, -8.656567
#Park1 cancela: 40.631503, -8.656521
#Park1
#   spot 1 = 40.631637, -8.656507
#   spot 2 = 40.631648, -8.656529
#   spot 3 = 40.631662, -8.656547
#Park2 entrance: 40.631890, -8.657763
#Park2
#   spot 1 = 40.631857, -8.657833
#   spot 2 = 40.631840, -8.657803
#rsu1 = 40.631491, -8.656481
#rsu2 = 40.631824, -8.657713

