from flask import Flask, render_template, jsonify, request
from park_db_init import create_park_db
from obu_db_init import create_obu_db
import sqlite3


app = Flask(__name__)

@app.route('/')
def index():
    conn_rsu = sqlite3.connect('park.db')
    rsu = conn_rsu.execute('select id, lat, long from rsu;')

    
    if request.is_json:
        conn_obu = sqlite3.connect('obu.db')
        crs = conn_obu.execute('select ip, lat, long from obu;')
        obus = {}
        for c in crs:
            obus.update({c[0] : {"lat":c[1], "long":c[2]}})
            
        return jsonify(obus)
    
    return render_template('map.html', rsu = rsu)


if __name__ == '__main__':
    create_park_db()
    create_obu_db()
    app.run(port=3000, debug = True)
   


