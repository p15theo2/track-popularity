# Track Popularity 

## Track popularity database from billboard.com , written in python and sql

Code is writen in python 3. For the code to run correctly you must have installed mysql server.Also you must have pre-installed all the necessary libraries python3 , matplotlib and billboard python api.


### Files explanation :

##### databasefillv2.py

Creates database and tables. Fills database for dates - 'stardate' till today . For startdate you can set any value you want(format - yyyy-mm-dd) which allows you to collect data from any time you want until today.
Every billboard chart date is a saturday so its advised to select a saturday as 'startdate' . Code collects all 100 songs from chart and stores them from 100 to 1 and from the oldest date to the newest . For example the first row of the billboard_ratings table contains the 100th position of the oldest chart while the last row contains the 1th row of the newest chart.
This allows us to add more charts on our database at the future.


##### databaseupdatev1.py

Finds the newest date on the tables and then updates the database until today .If there is no newer chart then it will just do nothing.  Works pretty much the same as databasefillv2.py.

##### databasedropv1.py

Deletes the entire database. If you run this and the database does not exist then it will throw an error.

##### databasesearchv2.py
 First it ask the user to input a track title . If the database contains this title then the program will print the track's chart position over the time. Then a new window will open , presenting a diagram based on those positions. The diagram is made using matplotlib plot.
 If the database does not contain this track title then the program will print "no results found" and then it will terminate.
 
 
 ### If you have any concerns/questions about the code please let me know ! . Thanks ! 
