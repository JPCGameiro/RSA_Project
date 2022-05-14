from datetime import datetime
import json
import time

json_result = []

#Read json data
with open("./parked.json") as json_file:
    data = json.load(json_file)
    print(data)

for i in range(0, 30):
    #0.1 seconds to dely for 10 Hz frequency in message generation
    time.sleep(0.1)
    dt = datetime.now()
    data['timestamp'] = datetime.timestamp(dt)
    json_result.append(data)

#Write result in output file
with open("parked_out.json", "w") as outfile:
    outfile.write(json.dumps(json_result))