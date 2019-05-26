#!/usr/bin/env python
# coding: utf-8

# Aparaithta imports
import mysql.connector as sql

# Enarksh syndeshs me thn topikh bash dedomenon pou exo hdh egatastisi- mysql
db = sql.connect(
host = 'localhost',
user= 'root',
passwd = 'password')
print(db)

#Deikths gia thn ektelesh query erothmatwn sthn bash dedomenon
cursor = db.cursor(buffered=True)

# Diagrafh ths bashs dedomenon
cursor.execute("DROP DATABASE  track_popularity")

# Elegxos gia energa database sthn bash dedomenwn me to onoma track_popularity
cursor.execute("select schema_name from information_schema.schemata where schema_name = 'track_popularity'")

# Katagrafh ton apotelesmaton pou mas epestrepse o deikths
databases = cursor.fetchall()

# Elegxos an o deikths epestrepse kapoio apotelesma
if not databases:
 print('database droped') 
else:
 print("database not droped")
print('databases active -', databases)


# Telos syndesis
db.commit()
cursor.close()
db.close()

