import sqlite3 as sql
import sys

db = sql.connect('park.db')

db.execute('''create table rsu(id integer,
                                ip text primary key);''')

db.execute('''create table coordinate( lat integer, 
                                        long integer,
                                        point integer primary key autoincrement);''')

db.execute('''create table park( vtype integer not null, 
                                vpriort text,
                                point integer not null,
                                ip text not null,
                                num integer primary key autoincrement,
                                foreign key(point) references coordinate(point),
                                foreign key(ip) references rsu(ip));''')








db.execute("insert into rsu values(1, '192.168.98.10')")
db.execute("insert into rsu values(2, '192.168.98.20')")

db.execute('insert into coordinate values(30, 120, null)')
db.execute('insert into coordinate values(30, 90,  null)')
db.execute('insert into coordinate values(35, 105, null)')
db.execute('insert into coordinate values(35, 75,  null)')
db.execute('insert into coordinate values(40, 90,  null)')
db.execute('insert into coordinate values(40, 60,  null)')


db.execute('insert into park values(15, null,      1, "192.168.98.20", null)')
db.execute('insert into park values(15, null,      2, "192.168.98.20", null)')
db.execute('insert into park values(15, "def",     3, "192.168.98.20", null)')
db.execute('insert into park values(15, null,      4, "192.168.98.10", null)')
db.execute('insert into park values(15, null,      5, "192.168.98.10", null)')
db.execute('insert into park values(15, "gravida", 6, "192.168.98.10", null)')

db.commit()
db.close()