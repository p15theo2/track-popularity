#!/usr/bin/env python
# coding: utf-8

# Aparaithta imports
import mysql.connector as sql
import billboard
import matplotlib
from matplotlib import pyplot as plt
import matplotlib.dates
from pylab import MaxNLocator


# Enarksh syndeshs me thn topikh bash dedomenon pou exo hdh egatastisi - mysql
db = sql.connect(
    host = "localhost",
    user = "root",
    passwd = "password",
    database = "track_popularity"
)
cursor = db.cursor(buffered=True)


# Orismos diaforon query erothmaton pou tha xrhsimopoihsoume argotera
searchquerry = ("""SELECT id FROM track WHERE title LIKE""")
popularityquery = ("SELECT date,position from billboard_rating where track_id =")

# Eisagogh titlou gia anazhthsh apo to xrhsth
print("Type a title for search and then press enter \n")
title = input()
# Anazhtsh sto table 'track;
searchquerry = searchquerry+"\""+title+"\""
cursor.execute(searchquerry)
# Epistrofh apotelesmaton
records = cursor.fetchall()
# An den yparxoun apotelesmata
if not records:
 print("no results found") 
# An yparxoun apotelesmata
else:
 # Epistrofh tou protou apotelesmatos
 for row in records: 
  trackid = row[0]
  print("Track found !!! Track id on table - " , trackid)
  # Euresi tou kommatiou kai ston pinaka billboard_rating
  trackpopularity = popularityquery+str(trackid)
  i=0
  cursor.execute(trackpopularity)
  # Epistrofh ton diaforon theseon tou kommatiou sta charts kai ektyposh
  popularityrecords = cursor.fetchall()
  for row in popularityrecords:
   print(row)
   i+=1
  print("Rows found:",i)
  # Kodikas gia thn dhmiourgia tou diagrammatos me to matplotlib
  # Taksinomisi ton apotelesmaton apo ton pinaka billboard_rating se lista
  new_x1, new_y1 = list(zip(*popularityrecords))
  # Megethos diagramatos
  plt.rcParams["figure.figsize"] = (16,6)
  # Metablhtes pou tha mas boithisoun na allaksoume ta shmeia tou x aksona
  fig, ax = plt.subplots()
  #diagrama(xroma,typos grammhs klp)
  plt.plot(new_x1,new_y1,color='g',marker ='s',linestyle="--",markerfacecolor="r",markersize='8',label="track - position")
  plt.xticks(rotation=30)
  # Anastrofh tou y aksona etsi oste gia y=0 'thesi sto chart' = 100 . Dhladh oso 
  # pio psila toso pio dimofiles
  plt.gca().invert_yaxis()
  # Etiketes stro x,y aksona kai titlos
  plt.ylabel('Position on chart')
  plt.xlabel('DATE')
  plt.title("Track\npopularity")
  # Epeksigisi ton shmeivn
  plt.legend()
  # Steni topothetisi tou diagramatos pano sto parathiro pou emfanizetai
  plt.tight_layout()
  #orismos ton shmeivn pou tha emfanizontai ston x aksona
  ax.xaxis.set_major_locator(
  matplotlib.dates.WeekdayLocator(byweekday=matplotlib.dates.SA))
  ax.xaxis.set_major_formatter(
  matplotlib.dates.DateFormatter('%a %d\n%b %Y'))
  # Emfanisi tou diagramatos
  plt.show()

# Telos syndeshs
cursor.close()
db.close()



