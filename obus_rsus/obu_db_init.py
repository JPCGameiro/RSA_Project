import sqlite3 as sql
import sys

db = sql.connect('obu.db')

db.execute('''create table obu(lat real,
                                long real,
                                ip text primary key);''')

db.execute('insert into obu values(null, null, "192.168.98.30")')
db.execute('insert into obu values(null, null, "192.168.98.40")')
db.execute('insert into obu values(null, null, "192.168.98.50")')

db.commit()
db.close()