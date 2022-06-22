import sqlite3 as sql
import sys

def create_park_db():
    db = sql.connect('park.db')
    db.execute('''drop table if exists rsu''')
    db.execute('''create table rsu(id integer,
                                    lat real,
                                    long real,
                                ip text primary key);''')

    db.execute('''drop table if exists coordinate''')
    db.execute('''create table coordinate(lat real, 
                                        long real,
                                        point integer primary key autoincrement);''')


    db.execute('''drop table if exists park''')
    db.execute('''create table park(vtype integer not null, 
                                    vpriort text,
                                    point integer not null,
                                    ip text not null,
                                    state integer not null,
                                    num integer primary key autoincrement,
                                    foreign key(point) references coordinate(point),
                                    foreign key(ip) references rsu(ip));''')


    db.execute("insert into rsu values(1, 40.631491, -8.656481, '192.168.98.10')")
    db.execute("insert into rsu values(2, 40.631824, -8.657713, '192.168.98.20')")


    db.execute('insert into coordinate values(40.65899, -8.6583838, null)') #RSU1
    db.execute('insert into coordinate values(40.631637, -8.656507,  null)') #PARK1 SPOT1
    db.execute('insert into coordinate values(40.631648, -8.656529, null)') #PARK1 SPOT2
    db.execute('insert into coordinate values(40.631662, -8.656547,  null)') #PARK1 SPOT3
    db.execute('insert into coordinate values(40.631824, -8.657713, null)') #RSU2
    db.execute('insert into coordinate values(40.6318569, -8.657833,  null)') #PARK2 SPOT1
    db.execute('insert into coordinate values(40.631840, -8.657803, null)') #PARK2 SPOT2

    db.execute('insert into park values(5, null, 2, "192.168.98.10", -1, null)') #PARK1 SPOT1
    db.execute('insert into park values(5, null, 3, "192.168.98.10", -1, null)') #PARK1 SPOT2
    db.execute('insert into park values(5, null, 4, "192.168.98.10", 6, null)') #PARK1 SPOT3
    db.execute('insert into park values(5, null, 6, "192.168.98.20", -1, null)') #PARK2 SPOT1
    db.execute('insert into park values(5, null, 7, "192.168.98.20", 8, null)') #PARK2 SPOT2

    db.commit()
    db.close()
