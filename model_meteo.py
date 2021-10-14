import requests, psycopg2
import pandas as pd
import json
import configuration

class ModelMeteo:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.connection()

    def connection(self):
        #Connection BDD
        self.conn = psycopg2.connect(database = configuration.database,
            user = configuration.user,
            password = configuration.password,
            host = configuration.host,
            port = configuration.port)
        self.cur = self.conn.cursor()

    def getCityByName(self, cityName):
        sql = f"""SELECT * FROM weather WHERE name LIKE '%{cityName}%';"""
        self.cur.execute(sql)
        res = self.cur.fetchone()
        dfraw = pd.read_sql(sql, self.conn, parse_dates=True)
        return dfraw

    def deleteCityByName(self, cityName):
        sql = f"""DELETE FROM weather WHERE name LIKE '%{cityName}%';"""
        self.cur.execute(sql)

    #insertion des valeurs dans la bdd
    def updateCity(self, dictMeteo):
        self.cur.execute(
            "INSERT INTO weather (coord_lon, coord_lat, main_temp, main_feels_like, main_pressure, main_humidity, wind_speed, name, date, zipcode) VALUES (%(coord_lon)s, %(coord_lat)s, %(main_temp)s, %(main_feels_like)s, %(main_pressure)s, %(main_humidity)s, %(wind_speed)s, %(name)s, NOW(), %(zipcode)s )", dictMeteo
        )
        self.conn.commit()
        
    def insertCity(self, dictMeteo):
        self.cur.execute(
            "INSERT INTO weather (coord_lon, coord_lat, main_temp, main_feels_like, main_pressure, main_humidity, wind_speed, name, date, zipcode) VALUES (%(coord_lon)s, %(coord_lat)s, %(main_temp)s, %(main_feels_like)s, %(main_pressure)s, %(main_humidity)s, %(wind_speed)s, %(name)s, NOW(), %(records_0_fields_code_postal)s )", dictMeteo
        )
        self.conn.commit()
    
    def getCityByCode(self, zipcode):
        sql = f"""SELECT * FROM weather WHERE zipcode = '{zipcode}';"""
        self.cur.execute(sql)
        res = self.cur.fetchone()
        dfraw = pd.read_sql(sql, self.conn, parse_dates=True)
        return dfraw
    
    def deleteCityByCode(self, zipcode):
        sql = f"""DELETE FROM weather WHERE zipcode = '{zipcode}';"""
        self.cur.execute(sql)
        
    def getZipcode(self, zipcode):
        sql = f"""SELECT * FROM weather WHERE zipcode = '{zipcode}';"""
        self.cur.execute(sql)
        return zipcode
    
