import sqlite3, time

conn = sqlite3.connect('park.db')

obu30 = [40.631894, -8.657776]
obu40 = [40.631810, -8.657700]
obu50 = [40.631864, -8.657742]

while(1):
    conn.execute('update obu set lat = {la}, long = {lo} where ip = "192.168.98.30"'.format(la = obu30[0], lo=obu30[1]))
    conn.execute('update obu set lat = {la}, long = {lo} where ip = "192.168.98.40"'.format(la = obu40[0], lo=obu40[1]))
    conn.execute('update obu set lat = {la}, long = {lo} where ip = "192.168.98.50"'.format(la = obu50[0], lo=obu50[1]))
    conn.commit()

    obu30[0] =0.000001 + obu30[0]
    obu30[1] =0.000001 + obu30[1]

    obu40[0]=0.000001 + obu40[0]
    obu50[1]=0.000001 + obu50[1]

    time.sleep(0.1)


