from datetime import datetime
import json
import time

#Go in square through all 4 points
def drive_in_square(data, point, obu, obuid):
    #0.1 seconds to dely for 10 Hz frequency in message generation
    while(data['longitude'] <= -8655763):
        obu.subscribe("vanetza/out/denm")
        time.sleep(0.1)
        data['longitude'] += 30
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
    while(data['latitude'] <= 40633209):
        obu.subscribe("vanetza/out/denm")
        time.sleep(0.1)
        data['latitude'] += 30
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
    print("OBU"+str(obuid)+": I'm at point 1")
    if(point == 1):
        return None

    while(data['longitude'] <= -8654387):
        time.sleep(0.1)
        data['longitude'] += 30
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
    while(data['latitude'] >= 40630577):
        time.sleep(0.1)
        data['latitude'] -= 30
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
    print("OBU"+str(obuid)+": I'm at point 2")
    if(point == 2):
        return None

    while(data['longitude'] >= -8654894):
        time.sleep(0.1)
        data['longitude'] -= 30
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
    while(data['latitude'] >= 40630007):
        time.sleep(0.1)
        data['latitude'] -= 30
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
    print("OBU"+str(obuid)+": I'm at point 3")
    if(point == 3):
        return None

    while(data['longitude'] >= -8657125):
        time.sleep(0.1)
        data['longitude'] -= 30
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
    while(data['latitude'] <= 40631786):
        time.sleep(0.1)
        data['latitude'] += 30
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
    print("OBU"+str(obuid)+": I'm at point 4")




#Go to the park entrance
def go_to_park(data, obu, obuid):
	#Go around the first three points
    drive_in_square(data, 3, obu, obuid)
	
    data['speed'] = 20
    #Go from point 3 to entrance of the parking
    while(data['longitude'] >= -8656567):
        obu.subscribe("vanetza/out/denm")
        time.sleep(0.1)
        data['longitude'] -= 10
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
    while(data['latitude'] <= 40631420):
        obu.subscribe("vanetza/out/denm")
        time.sleep(0.1)
        data['latitude'] += 10
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
    print("OBU"+str(obuid)+": I'm At the parking entrance")






#if a spot is not available go from the park entrance to the point 4
def go_straight(data, obu, obuid):
    #Go from point entrance of the park to point 4
    while(data['longitude'] >= -8657125):
        obu.subscribe("vanetza/out/denm")
        time.sleep(0.1)
        data['longitude'] -= 10
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
    while(data['latitude'] <= 40631786):
        obu.subscribe("vanetza/out/denm")
        time.sleep(0.1)
        data['latitude'] += 10
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
    print("OBU"+str(obuid)+": I'm At the point 4")






#Go to a spot in thse parking lot
def park(spot, data, obu, obuid):
    #Go from entrance of the parking to cancelas of the park
    data['speed'] = 10
    while(data['longitude'] <= -8656521):
        obu.subscribe("vanetza/out/denm")
        time.sleep(0.1)
        data['longitude'] += 10
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
    while(data['latitude'] <= 40631503):
        obu.subscribe("vanetza/out/denm")
        time.sleep(0.1)
        data['latitude'] += 10
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
    print("OBU"+str(obuid)+": I'm at the cancela")
    
    if(spot == 1):
        while(data['longitude'] <= -8656507):
            time.sleep(0.1)
            data['longitude'] += 10
            data['timestamp'] = datetime.timestamp(datetime.now())
            obu.publish("vanetza/in/cam", json.dumps(data))
        while(data['latitude'] <= 40631637):
            time.sleep(0.1)
            data['latitude'] += 10
            data['timestamp'] = datetime.timestamp(datetime.now())
            obu.publish("vanetza/in/cam", json.dumps(data))
        data['longitude'] = -8656507
        data['latitude'] = 40631637
        data['timestamp'] = datetime.timestamp(datetime.now())
        data['speed'] = 0
        obu.publish("vanetza/in/cam", json.dumps(data))
        print("OBU"+str(obuid)+": I'm parked at SPOT1")
    elif(spot == 2):
        while(data['longitude'] >= -8656529):
            time.sleep(0.1)
            data['longitude'] -= 10
            data['timestamp'] = datetime.timestamp(datetime.now())
        while(data['latitude'] <= 40631648):
            time.sleep(0.1)
            data['latitude'] += 10
            data['timestamp'] = datetime.timestamp(datetime.now())
        data['longitude'] = -8656529
        data['latitude'] = 40631648
        data['timestamp'] = datetime.timestamp(datetime.now())
        data['speed'] = 0
        obu.publish("vanetza/in/cam", json.dumps(data))
        print("OBU"+str(obuid)+": I'm parked at SPOT2")
    elif(spot == 3):
        while(data['longitude'] >= -8656547):
            time.sleep(0.1)
            data['longitude'] -= 10
            data['timestamp'] = datetime.timestamp(datetime.now())
        while(data['latitude'] <= 40631662):
            time.sleep(0.1)
            data['latitude'] += 10
            data['timestamp'] = datetime.timestamp(datetime.now())
        data['longitude'] = -8656547
        data['latitude'] = 40631662
        data['timestamp'] = datetime.timestamp(datetime.now())
        data['speed'] = 0
        obu.publish("vanetza/in/cam", json.dumps(data))
        print("OBU"+str(obuid)+": I'm parked at SPOT3")






#Leave the parking lot and go to point 4
def leave_park(spot, data, obu, obuid):
    #go to the park cancela
    data['speed'] = 10
    if(spot == 1):
        while(data['longitude'] >= -8656521):
            time.sleep(0.1)
            data['longitude'] -= 10
            data['timestamp'] = datetime.timestamp(datetime.now())
            obu.publish("vanetza/in/cam", json.dumps(data))
    else:
        while(data['longitude'] <= -8656521):
            time.sleep(0.1)
            data['longitude'] += 10
            data['timestamp'] = datetime.timestamp(datetime.now())  
            obu.publish("vanetza/in/cam", json.dumps(data))   
    while(data['latitude'] >= 40631503):
        time.sleep(0.1)
        data['latitude'] -= 10
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
    print("OBU"+str(obuid)+": I'm na cancela")
    data['speed'] = 30
    
    #Got to the starting point of the circuit
    while(data['longitude'] >= -8657125):
        time.sleep(0.1)
        data['longitude'] -= 10
        data['timestamp'] = datetime.timestamp(datetime.now())
    while(data['latitude'] <= 40631786):
        time.sleep(0.1)
        data['latitude'] += 10
        data['timestamp'] = datetime.timestamp(datetime.now())
    print("OBU"+str(obuid)+": I Left my spot sucessfully")



#40.633209, -8.655763       40.630577, -8.654387
#                       40.630007, -8.654894
#40.631786, -8.657125    

#Parking entrance: 40.631420, -8.656567
#Park cancela: 40.631503, -8.656521
#spot 1 = 40.631637, -8.656507
#spot 2 = 40.631648, -8.656529
#spot 3 = 40.631662, -8.656547 