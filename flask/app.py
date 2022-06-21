from flask import Flask, render_template, jsonify, request

import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect('park.db')
    rsu = conn.execute('select id, lat, long from rsu;')

    
    if request.is_json:
        crs = conn.execute('select ip, lat, long from obu;')
        obus = {}
        for c in crs:
            obus.update({c[0] : {"lat":c[1], "long":c[2]}})
            
        return jsonify(obus)
    
    return render_template('map.html', rsu = rsu)


if __name__ == '__main__':
   app.run(port=3000, debug = True)
   


