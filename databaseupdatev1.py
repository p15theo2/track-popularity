#!/usr/bin/env python
# coding: utf-8

# Aparaithta imports
import mysql.connector as sql
import billboard
import datetime
from datetime import date


# Enarksh syndeshs me thn topikh bash dedomenon pou exo hdh egatastisi - mysql
db = sql.connect(
    host = "localhost",
    user = "root",
    passwd = "password",
    database = "track_popularity"
)
# Deikths gia thn ektelesh query erothmatwn sthn bash dedomenon
cursor = db.cursor(buffered=True)

# Euresi shmerinhs hmeromhnias
todate = date.today()
# Euresi teleutaias(pio prosfaths) hmeromhnias ston pinaka 'billboard_rating'
cursor.execute("""select date from billboard_rating ORDER BY date DESC LIMIT 1;""")
list = cursor.fetchall()
for row in list:
 lastdate = row[0]
# Ektyposh twn hmeromhnion pou brikame parapano
print("date today(yyyy-mm-dd)",todate)
print("last date on tables - saturday (yyyy-mm-dd)\n",lastdate)


# Orismos diaforon query erothmaton pou tha xrhsimopoihsoume argotera
# Eisagogi tragoudiou ston pinaka track
trackquery = ("INSERT INTO track(title) VALUES (%s)")
# Eisagogi thesis sto chart ston pinaka billboard_rating
ratequery = ("INSERT INTO billboard_rating (date,position,track_id) VALUES (%s,%s,%s)")
# Elegxos gia to an kapoio kommati yparxi hdh ston pinaka track
checkquery = ("SELECT id from track where title =")

# Proxorame mia mera mprosta apo thn pio prosfath hmeromhnia gia na mhn ksanagemisoume thn basi me hdh yparxonta dedomena
lastdate+=datetime.timedelta(1)

# Enarksi gemismatos ton pinakon to while stamataei otan ftasoyme sthn shmerinh hmera,to gemisma ton pinakon arxizei me tis pio palies prosthikes kai teleiwnei stis pio prosfates - diladi stis shmerines.
while lastdate<todate:
   # Euresi tou epomenou sabbatou apo thn hmeromhnia pou exi ekxorithi sto lastdate
   saturday = lastdate + datetime.timedelta( (5-lastdate.weekday()) % 7 )
   # Pernoume to chart tou billboard gia thn hmeromhnia pou brikame
   chart = billboard.ChartData('hot-100',saturday)
   # i=99 giati to chart exei 100 kommatia kai ta arithmi apo to 0
   i=99
   while i>=0:
    song = chart[i]
    # Titlos
    title = song.title
    # Thesi sto chart
    songposition = i+1
    # Hmeromhnia
    chartdate = chart.date
    # Dhmiourgia tou erothmatos gia na eleksoume an to kommati yparxi hdh ston
    # pinaka track
    tempquery = checkquery+"\""+title+"\""
    # Epistrofh apotelesmaton kai elegxos an eixame kapoio apotelesma
    cursor.execute(tempquery)
    records = cursor.fetchall()
    for row in records: 
     trackid = row[0]
    # An to kommati den yparxei hdh ston pinaka track
    if cursor.rowcount==0:
     # Eisagogh ston pinaka track
     values = (title)
     cursor.execute(trackquery,(values,))
     # Euresi tou id pou tou dothike apo ton pinaka track  
     tempquery = checkquery+"\""+title+"\""
     cursor.execute(tempquery)
     records = cursor.fetchall()
     for row in records: 
      trackid = row[0]
     # Eisagogi ston pinaka billboard_rating me to id pou vrikame pio pano
     values2 = (chartdate,songposition,trackid)
     cursor.execute(ratequery,values2)
     # An to kommati yparxei hdh ston pinaka track
    else:
     # Eisagogi ston pinaka billboard_rating me to id pou vrikame prin to if
     values2 = (chartdate,songposition,trackid)
     cursor.execute(ratequery,values2)
    # Meiosh tou i etsi oste ta tragoudia na prostithonte stous pinakes me seira 
    # apo to teleytaio sto prvto osos anafora thn thesi tous sto chart
    i=i-1
  # Euresi tou epomenou sabbatou
   lastdate +=datetime.timedelta(7)


# Euresi kai ektyposi ths teleuteas hmeromhnias
cursor.execute("""select * from billboard_rating ORDER BY date DESC LIMIT 1;""")
tempvar = cursor.fetchall()
print("Database updated until date (yyyy-mm-dd format)")
for row in tempvar:
 print(row[1])
# An ola exoun paei kala to last row periexi thn proti thesi tou chart ths shmerinhs hmeras
cursor.execute("""select * from billboard_rating ORDER BY id DESC LIMIT 1;""")
# Ektyposi tou teleytaiou row tou pinaka billboard_rating
print("Example last row on billboard rating:\n",cursor.fetchall())


# Telos syndeshs
db.commit()
cursor.close()
db.close()




