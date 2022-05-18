from datetime import datetime
import json
import time

#Go in square through all 4 points
def drive_in_square(data, point, obu):
    #0.1 seconds to dely for 10 Hz frequency in message generation
    while(data['longitude'] <= -8.655763):
        time.sleep(0.1)
        data['longitude'] += 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
    while(data['latitude'] <= 40.633209):
        time.sleep(0.1)
        data['latitude'] += 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
    if(point == 1):
        return None


    while(data['longitude'] <= -8.654387):
        time.sleep(0.1)
        data['longitude'] += 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
    while(data['latitude'] <= 40.630577):
        time.sleep(0.1)
        data['latitude'] -= 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
    if(point == 2):
        return None


    while(data['longitude'] >= -8.654894):
        time.sleep(0.1)
        data['longitude'] -= 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
    while(data['latitude'] >= 40.630007):
        time.sleep(0.1)
        data['latitude'] -= 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
    if(point == 3):
        return None


    while(data['longitude'] >= -8.657125):
        time.sleep(0.1)
        data['longitude'] -= 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))
        print("CAM")
        print(data)
    while(data['latitude'] >= 40.631786):
        time.sleep(0.1)
        data['latitude'] += 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
        obu.publish("vanetza/in/cam", json.dumps(data))





#Go to the park entrance
def go_to_park():
    drive_in_square(3)

    #Go from point 3 to entrance of the parking
    while(data['longitude'] >= -8.656567):
        time.sleep(0.1)
        data['longitude'] -= 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
    while(data['latitude'] <= 40.631420):
        time.sleep(0.1)
        data['latitude'] += 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
    print("I'm At the parking entrance")


#Go to a spot in the parking lot
def park(spot):
    #Go from entrance of the parking to cancelas of the park
    while(data['longitude'] <= -8.656521):
        time.sleep(0.1)
        data['longitude'] += 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
    while(data['latitude'] <= 40.631503):
        time.sleep(0.1)
        data['latitude'] += 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
    print("I'm at the cancela")
    
    if(spot == 1):
        while(data['longitude'] <= -8.656507):
            time.sleep(0.1)
            data['longitude'] += 0.00001
            data['timestamp'] = datetime.timestamp(datetime.now())
        while(data['latitude'] <= 40.631637):
            time.sleep(0.1)
            data['latitude'] += 0.00001
            data['timestamp'] = datetime.timestamp(datetime.now())
        print("Parked at SPOT1")
    elif(spot == 2):
        while(data['longitude'] >= -8.656529):
            time.sleep(0.1)
            data['longitude'] -= 0.00001
            data['timestamp'] = datetime.timestamp(datetime.now())
        while(data['latitude'] <= 40.631648):
            time.sleep(0.1)
            data['latitude'] += 0.00001
            data['timestamp'] = datetime.timestamp(datetime.now())
        print("Parked at SPOT2")
    elif(spot == 3):
        while(data['longitude'] >= -8.656547):
            time.sleep(0.1)
            data['longitude'] -= 0.00001
            data['timestamp'] = datetime.timestamp(datetime.now())
        while(data['latitude'] <= 40.631662):
            time.sleep(0.1)
            data['latitude'] += 0.00001
            data['timestamp'] = datetime.timestamp(datetime.now())
        print("Parked at SPOT3")

#Leave the parking lot and go to point 4
def leave_park(spot):
    #go to the park cancela
    if(spot == 1):
        while(data['longitude'] >= -8.656521):
            time.sleep(0.1)
            data['longitude'] -= 0.00001
            data['timestamp'] = datetime.timestamp(datetime.now())
    else:
        while(data['longitude'] <= -8.656521):
            time.sleep(0.1)
            data['longitude'] += 0.00001
            data['timestamp'] = datetime.timestamp(datetime.now())     
    while(data['latitude'] >= 40.631503):
        time.sleep(0.1)
        data['latitude'] -= 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
    print("I'm na cancela")

    #Got to the starting point of the circuit
    while(data['longitude'] >= -8.657125):
        time.sleep(0.1)
        data['longitude'] -= 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
    while(data['latitude'] <= 40.631786):
        time.sleep(0.1)
        data['latitude'] += 0.00001
        data['timestamp'] = datetime.timestamp(datetime.now())
    print("I Left my spot sucessfully")

'''#Read json data
with open("./driving.json") as json_file:
    data = json.load(json_file)
    print(data)


while(True):
    #drive_in_square(4)
    print("Circuit Done")

    go_to_park()
    park(1)
    leave_park(1)
    break
'''


#40.633209, -8.655763       40.630577, -8.654387
#                       40.630007, -8.654894
#40.631786, -8.657125    

#Parking entrance: 40.631420, -8.656567
#Park cancela: 40.631503, -8.656521
#spot 1 = 40.631637, -8.656507
#spot 2 = 40.631648, -8.656529
#spot 3 = 40.631662, -8.656547 
