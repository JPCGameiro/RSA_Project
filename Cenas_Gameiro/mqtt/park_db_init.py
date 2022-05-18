import sqlite3 as sql
import sys

db = sql.connect('park.db')

db.execute('''create table rsu(id integer,
                                ip text primary key);''')

db.execute('''create table coordinate(lat real, 
                                      long real,
                                      point integer primary key autoincrement);''')

db.execute('''create table park(vtype integer not null, 
                                vpriort text,
                                point integer not null,
                                ip text not null,
                                state integer not null,
                                num integer primary key autoincrement,
                                foreign key(point) references coordinate(point),
                                foreign key(ip) references rsu(ip));''')






db.execute("insert into rsu values(1, '192.168.98.10')")

db.execute('insert into coordinate values(40.65899, -8.6583838, null)') #RSU
db.execute('insert into coordinate values(40.631637, -8.656507,  null)') #SPOT1
db.execute('insert into coordinate values(40.631648, -8.656529, null)') #SPOT2
db.execute('insert into coordinate values(40.631662, -8.656547,  null)') #SPOT3

db.execute('insert into park values(15, null,      3, "192.168.98.30", 0, null)')
db.execute('insert into park values(15, null,      2, "192.168.98.20", 0, null)')
db.execute('insert into park values(15, "def",     3, "192.168.98.20", 0, null)')

db.commit()
db.close()
