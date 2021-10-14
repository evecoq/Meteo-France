import requests
import json
import datetime
import pandas as pd

def flattenJson(json):
    out = {}
    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x
    flatten(json)
    return out

def mergeDict(dictOne, dictTwo):
    keys = ['coord_lon', 'coord_lat', 'main_temp', 'main_feels_like', 'main_pressure', 'main_humidity', 'wind_speed', 'name']
    meteoSmall = {x:dictOne[x] for x in keys}  
    keys = ['records_0_fields_code_postal']
    zipcodeSmall = {x:dictTwo[x] for x in keys} 
    alldata = {**meteoSmall, **zipcodeSmall}
    return alldata

def getTime(df, now):
    timestamp = pd.to_datetime(df['date'])
    delta = now - timestamp            
    delta = delta.to_frame()        
    delta['seconds'] = delta['date'].dt.seconds
    return delta

def getData(url):
    response = requests.get(url).content
    data = json.loads(response)    
    flatten = flattenJson(data) 
    return flatten