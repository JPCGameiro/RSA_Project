# RSA - Parking Lot Management
## Contents
1. obus_rsus folder contains scripts to generate the simulations and communicate with the vanetza system (mqtt brokers)
2. app.py, static and templates folders allow to run the flask server that presents the visual envirnoment on the browser
3. obu_db_init.py and park_db_init.py perform the initialization of the database
4. docker-compose.yml contains the configuration to launch the docker containers that represent the obus and rsus

## How to run
1. Open four terminals
2. Run in one the docker compose (in the vanetza repository source)
```bash
docker-compose up
``` 
3. Run in another the app.py
```bash
python3 app.py
```
4. Run in another rsu_script.py
 ```bash
python3 rsu_script.py
```
5. Run in the last one obu_script.py

```bash
python3 obu_script.py
```

## How to install requirements

1. Create a virtual environment (venv)
```bash
python3 -m venv venv
```

2. Activate the virtual environment (you need to repeat this step, and this step only, every time you start a new terminal/session):
```bash
source venv/bin/activate
```

3. Install the game requirements:
```bash
pip install -r requirements.txt
```
