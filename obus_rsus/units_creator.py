import yaml
import copy

def create_dockercompose(numrsus, numobus):
    if numrsus + numobus > 15:
        print("ERROR: Invalid number of units, the sum of rsus and obus cannot be greater than 15")
        return 1

    #Open docker-compose file
    f = open("../../../Desktop/vanetza/docker-compose.yml", 'r')
    docker_yml = yaml.load(f, Loader=yaml.FullLoader)
    
    #Extract rsu and obu objects from yml file
    rsu = (docker_yml['services']['rsu'])
    obu = (docker_yml['services']['obu'])
    #Delete rsu and obu objects so that new ones can be created
    del[docker_yml['services']['rsu']]
    del[docker_yml['services']['obu']]

    print("Adding RSUs to the docker-compose.yml file...")
    #Add rsus to the docker compose
    for i in range(numrsus): 
        #new hostname
        rsu['hostname'] = 'rsu' + str(i+1)
        #new VANETZA_STATION_IDs
        rsu['environment'][0] = rsu['environment'][0][:-1] + str(i+1)
        #new VANETZA_MAC_ADDRESSs
        rsu['environment'][2] = rsu['environment'][2][:-1] + str(i+1)
        #new ipv4_address
        rsu['networks']['vanetzalan0']['ipv4_address'] = '192.168.98.'+str(i+1)+'0'
        
        #Add new rsu to the docker yml file
        docker_yml['services'][rsu['hostname']] = copy.deepcopy(rsu)
        print("RSU"+ str(i+1) + " added successfully!")

    
    print("Adding OBUs to the docker-compose.yml file...")
    #Add obus to the docker compose
    for i in range(numrsus, numrsus+numobus): 
        #new hostname
        obu['hostname'] = 'obu' + str(numobus+numrsus - i)
        #new VANETZA_STATION_IDs
        obu['environment'][0] = obu['environment'][0][:-1] + str(i+1)
        #new VANETZA_MAC_ADDRESSs
        obu['environment'][2] = obu['environment'][2][:-1] + str(i+1)
        #new ipv4_address
        obu['networks']['vanetzalan0']['ipv4_address'] = '192.168.98.'+str(i+1)+'0'
        
        #Add new rsu to the docker yml file
        docker_yml['services'][obu['hostname']] = copy.deepcopy(obu)
        print("OBU"+ str(i+1) + " added successfully!")
    
    
    
    #Write in result file
    f = open("../../../Desktop/vanetza/docker-compose-result.yml", 'w')
    yaml.dump(docker_yml, f, sort_keys = False)
    print("New docker-compose.yml file created successfully!")


create_dockercompose(3, 2)