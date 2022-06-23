import sqlite3 as sql
import sys

def create_obu_db():
    db = sql.connect('obu.db')

    db.execute('''drop table if exists obu''')
    db.execute('''create table obu(lat real,
                                    long real,
                                    ip text primary key);''')

    db.execute('insert into obu values(null, null, "192.168.98.30")')
    db.execute('insert into obu values(null, null, "192.168.98.40")')
    db.execute('insert into obu values(null, null, "192.168.98.50")')
    db.execute('insert into obu values(null, null, "192.168.98.60")')
    db.execute('insert into obu values(40.631840, -8.657803, "192.168.98.80")')

    db.commit()
    db.close()