#!/usr/bin/env python
# coding: utf-8

# Aparaithta imports
import mysql.connector as sql
import billboard
import datetime
from datetime import date


# enarksh syndeshs me thn topikh bash dedomenon pou exo hdh egatastisi - mysql
db = sql.connect(
host = 'localhost',
user= 'root',
passwd = 'password')
print(db)


# deikths gia thn ektelesh query erothmatwn sthn bash dedomenon
cursor = db.cursor(buffered=True)

# dhmiourgia tou database track_popularity
cursor.execute("CREATE DATABASE IF NOT EXISTS `track_popularity` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;")

#elegxos an dhmiourghthike bash dedomenwn me to onoma 'track_popularity'
cursor.execute("select schema_name from information_schema.schemata where schema_name = 'track_popularity'")
#katagrafh ton apotelesmaton pou mas epestrepse o deikths
databases = cursor.fetchall()
# elegxos an o deikths epestrepse kapoio apotelesma kai ektyposi
if not databases:
 print("database not created") 
else:
 print("database created")
print(databases)


# enarksh syndeshs me thn database - 'track_popularity'
db = sql.connect(
    host = "localhost",
    user = "root",
    passwd = "password",
    database = "track_popularity"
)
# Deikths gia thn ektelesh query erothmatwn sthn bash dedomenon
cursor = db.cursor(buffered=True)

# Dhmiourgia pinaka 'billboard_rating'
cursor.execute("""CREATE TABLE IF NOT EXISTS `billboard_rating` (
  `id` int(11) NOT NULL,
  `date` DATE NOT NULL,
  `position` int(11) NOT NULL,
  `track_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ;""")
# Dhmiourgia pinaka 'track'
cursor.execute("""CREATE TABLE IF NOT EXISTS `track` (
  `id` int(11) NOT NULL,
  `title` varchar(1024) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ;""")

# Orismos kleidiwn
cursor.execute("""ALTER TABLE `billboard_rating`
 ADD PRIMARY KEY (`id`), ADD KEY `track_id` (`track_id`);""")
cursor.execute("""ALTER TABLE `track`
 ADD PRIMARY KEY (`id`);""")
# Orismos tou column 'id' os auto_increment kai sta dyo table
cursor.execute("""ALTER TABLE track MODIFY id int(11) NOT NULL AUTO_INCREMENT;""")
cursor.execute("""ALTER TABLE `billboard_rating`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;""")
#orismos anaforon sta kleidia
cursor.execute("""ALTER TABLE `billboard_rating`
ADD CONSTRAINT `billboard_rating_ibfk_1` FOREIGN KEY (`track_id`) REFERENCES `track` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;""")

# Elegxos gia ta tables pou dhmiourghthkan
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
print('tables created :')
for table in tables:
    print(table)

# Euresi shmerinhs hmeromhnias
todate = date.today()
print("date today yyyy-mm-dd:",todate)

# Orismos mias tyxaias hmeromhnias gia na arxisei h katagrafh ton dedomenon dhmothkothtas (mporoume na to alaksoume kai na to orisoume se opoiadhpote hmeromhnia theloume emeis - kata protimhsh na einai kapoio sabbato afou to billboard parexi ta charts ths ebdomadas ana sabbato.) 
startdate = datetime.date(2019,2,1)
print("chosen day to test yyyy-mm-dd:",startdate)

# Orismos diaforon query erothmaton pou tha xrhsimopoihsoume argotera
# Eisagogi tragoudiou ston pinaka 'track'
trackquery = ("INSERT INTO track(title) VALUES (%s)")
# Eisagogi thesis sto chart ston pinaka 'billboard_rating'
ratequery = ("INSERT INTO billboard_rating (date,position,track_id) VALUES (%s,%s,%s)")
# Elegxos gia to an kapoio kommati yparxi hdh ston pinaka 'track'
checkquery = ("SELECT id from track where title =")

#enarksi gemismatos ton pinakon to while stamataei otan ftasoyme sthn shmerinh hmera,to gemisma ton pinakon arxizei me tis pio palies prosthikes kai teleiwnei stis pio prosfates - diladi stis shmerines.
while startdate<todate:
   # Euresi tou amesos epomenou sabbatou sthn hmeromhnia pou orisame an h
   # hmeromhnia  einai hdh sabbato tote parameni ekei .
   saturday = startdate + datetime.timedelta( (5-startdate.weekday()) % 7 )
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
    cursor.execute(tempquery)
    #epistrofh apotelesmaton kai elegxos an eixame kapoio apotelesma
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
     values2 = (chartdate,int(songposition),trackid)
     cursor.execute(ratequery,values2)
     # An to kommati yparxei hdh ston pinaka track
    else:
     # Eisagogi tis thesis sto chart ston pinaka billboard_rating me to id pou 
     # vrikame prin to if
     values2 = (chartdate,songposition,trackid)
     cursor.execute(ratequery,values2)
    # Meiosh tou i etsi oste ta tragoudia na prostithonte stous pinakes me seira
    # apo to teleytaio sto prvto osos anafora thn thesi tous sto chart
    i=i-1
  # Euresi tou epomenou sabbatou
   startdate +=datetime.timedelta(7)


# Ektyposi 3 rows apo ton pinaka track gia paradigma
cursor.execute("SELECT * FROM track LIMIT 3")
print("3 rows from track table\n",cursor.fetchall())

# Ektyposi 3 rows apo ton pinaka billboard_rating gia paradigma
cursor.execute("SELECT * FROM billboard_rating LIMIT 3")
print("3 rows from billboard_rating\n",cursor.fetchall())



# An ola exoun paei kala to last row periexi thn proti thesi tou chart ths shmerinhs hmeras
cursor.execute("""select * from billboard_rating ORDER BY id DESC LIMIT 1;""")
tempvar = cursor.fetchall()
# ektyposi tou teleytaiou row tou pinaka billboard_rating
for row in tempvar:
 print("Newest date of charts(saturday) yyyy-mm-dd format : ",row[1])
print ('last row:\n',tempvar)

# An ola exoun paei kala to first row periexi thn teleutaia thesi tou chart ths  hmeras pou orisame os arxikh
cursor.execute("""select * from billboard_rating ORDER BY id ASC LIMIT 1;""")
tempvar = cursor.fetchall()
# ektyposi tou protou row tou pinaka billboard_rating
for row in tempvar:
 print("Oldest date of charts(saturday) yyyy-mm-dd format : ",row[1])
print ("First row:\n",tempvar)


#lhksh syndesis
db.commit()
cursor.close()
db.close()




