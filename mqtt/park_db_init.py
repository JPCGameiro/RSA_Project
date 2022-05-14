import sqlite3 as sql
import sys

db = sql.connect('park.db')

db.execute('create table ParkingLot(name text primary key);')

db.execute('''create table Coordinate( lat integer, 
                                        long integer,
                                        point integer primary key autoincrement);''')

db.execute('''create table Park( vehicle integer not null, 
                                priority text,
                                point1 integer not null,
                                point2 integer not null,
                                park text not null,
                                num integer primary key autoincrement,
                                foreign key(point1) references Coordinate(point),
                                foreign key(point2) references Coordinate(point),
                                foreign key(park) references ParkingLot(name));''')


db.execute("insert into ParkingLot values('deti')")
db.execute('insert into ParkingLot values("biblioteca")')

db.execute('insert into Coordinate values(30, 120, null)')
db.execute('insert into Coordinate values(30, 90, null)')
db.execute('insert into Coordinate values(35, 105, null)')
db.execute('insert into Coordinate values(35, 75, null)')
db.execute('insert into Coordinate values(40, 90, null)')
db.execute('insert into Coordinate values(40, 60, null)')
db.execute('insert into Coordinate values(55, 75, null)')
db.execute('insert into Coordinate values(35, 55, null)')
db.execute('insert into Coordinate values(75, 55, null)')
db.execute('insert into Coordinate values(70, 60, null)')
db.execute('insert into Coordinate values(70, 90, null)')
db.execute('insert into Coordinate values(85, 85, null)')
db.execute('insert into Coordinate values(65, 95, null)')
db.execute('insert into Coordinate values(90, 100, null)')
db.execute('insert into Coordinate values(70, 110, null)')

db.execute('insert into Park values(1, null, 1, 2, "deti", null)')
db.execute('insert into Park values(1, "gravida", 3, 4, "deti", null)')
db.execute('insert into Park values(1, "defeciente", 5, 6, "deti", null)')
db.execute('insert into Park values(2, null, 7, 8, "deti", null)')

db.execute('insert into Park values(1, null, 7, 9, "biblioteca", null)')
db.execute('insert into Park values(1, "gravida", 10, 11, "biblioteca", null)')
db.execute('insert into Park values(1, "defeciente", 12, 13, "biblioteca", null)')
db.execute('insert into Park values(2, null, 14, 15, "biblioteca", null)')

db.commit()
db.close()