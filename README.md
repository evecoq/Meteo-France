Here is a back-end of an apllication for getting the weather in France by city or by a post-code.

How does it work?
You need to create a PostgrSQL database with one table that consists following columns: coord_lon, coord_lat, main_temp, main_feels_like, main_pressure, main_humidity, wind_speed, name, date, zipcode.
Each time we check the weather in any city, the data will be stock in the database. If you sent a request for a city that has been already inserted within an hour, you'll get the same information. 
However, if the city already exists but it's been more than 1 hours since it has been inserted, than the information will be updated. 

You need to create a profile on https://openweathermap.org/ in API part I've choosen the "Current Weather Data" which is free. Get the API key and insert it in meteo.py file.
It doesn't provide the postcodes, so I added it from another API (https://datanova.laposte.fr/api)

There are 4 files: 
 - meteo.py that consists the algorithmic part of the code
 - model_meteo.py that consists all the functions with SQL queries
 - tool.py where we have other kinds of functions as, for example, flatten json fonction
 - log.py where I put 2 functions that print the outputs with weather informations 
You need to create a profile on https://openweathermap.org/ in API part I've choosen the "Current Weather Data" which is free. Get the API key and insert it in meteo.py file.


Sourse of flatten_json function https://towardsdatascience.com/flattening-json-objects-in-python-f5343c794b10
