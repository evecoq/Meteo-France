#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests, psycopg2
import json
import datetime as dt
from datetime import timedelta
from datetime import datetime
import pandas as pd
import re

from model_meteo import ModelMeteo
from log import printFromDict, printMessage
from tool import flattenJson, mergeDict, getTime, getData

db = ModelMeteo()
cur = db.connection()
now = dt.datetime.now()

#Recherche méteo
printMessage("Recherche méteo dans votre ville")
search = input("Nom de ville ou code postal? (v/c)\n")
API_key = '0caed253ae533fff1bcbec7336e607e9'

#Par ville
if search == "v":
    city_name = input('Ville\n')
    dfraw = db.getCityByName(city_name)
    
    #Si la ville existe, verifier l'heure de dernier mis à jour
    if not dfraw.empty:        
            delta = getTime(dfraw, now)
            
            #Inserer les données tous frais
            if pd.Series(delta['seconds'] >= 3600).all():
                #Supprimer les données existantes
                db.deleteCityByName(city_name)
                
                url = ('http://api.openweathermap.org/data/2.5/weather?q='+city_name+'&appid='+API_key+'&units=metric')
                meteo_city = getData(url)
                #Recuperation de code postal dans dfraw                
                getZip = dfraw["zipcode"]                               
                meteo_city['zipcode'] = int(getZip)
                
                db.updateCity(meteo_city)
                printFromDict(meteo_city)     
            else:
                printFromDict(meteo_city)
                    
    #Si la ville n'existe pas encore, charger les données
    elif dfraw.empty:
        url = ('http://api.openweathermap.org/data/2.5/weather?q='+city_name+'&appid='+API_key+'&units=metric')
        meteo_city = getData(url)
        
        #Recuperation de code postal        
        city_name = city_name.upper()
        url = ('https://datanova.laposte.fr/api/records/1.0/search/?dataset=laposte_hexasmal&q=&rows=1&facet=nom_de_la_commune&facet=code_postal&refine.nom_de_la_commune='+city_name+'')
        zipcode_city = getData(url)
        
        if 'records_0_fields_code_postal' not in zipcode_city: 
            #adaptation de nom de ville pour la recherche de zipcode
            city_name = city_name.upper()
            
            #Recherche de code postal
            url = ('https://datanova.laposte.fr/api/records/1.0/search/?dataset=laposte_hexasmal&q=&rows=1&facet=nom_de_la_commune&facet=code_postal&refine.nom_de_la_commune='+city_name+'+01')
            zipcode_city = getData(url)
            #Extraction des lignes qui nous interesse, merge 2 dicts dans un 1
            alldata = db.mergeDict(meteo_city, zipcode_city)
    
            #Insertion dans la BDD
            db.insertCity(alldata)
            printFromDict(meteo_city)
        
        else:       
            #Extraction des lignes qui nous interesse, merge 2 dicts dans un 1
            alldata = mergeDict(meteo_city, zipcode_city)
    
            #Insertion dans la BDD
            db.insertCity(alldata)
            printFromDict(meteo_city)
            
#Recherche par le code postal
if search == "c":
    zipcode = input('Code postal\n')
    dfraw = db.getCityByCode(zipcode)
    
    #Si la ville existe, verifier l'heure de dernier mis à jour
    if not dfraw.empty:        
            delta = getTime(dfraw, now)
            
            #Inserer les données tous frais
            if pd.Series(delta['seconds'] >= 3600).all():
                #Supprimer les données existantes
                db.deleteCityByCode(zipcode)                
                #Recuperer le code postal dans la bdd
                db.getZipcode(zipcode)
                #Recuperer le meteo
                url = ('http://api.openweathermap.org/data/2.5/weather?zip='+zipcode+',FR&appid='+API_key+'&units=metric')
                meteo_zip = getData(url)
                meteo_zip['zipcode'] = zipcode                
                db.updateCity(meteo_zip) 
                printFromDict(meteo_zip)
                
            else:
                printFromDict(meteo_zip)
                
    #Si la ville n'existe pas encore, charger les données
    elif dfraw.empty:
        url = ('http://api.openweathermap.org/data/2.5/weather?zip='+zipcode+',FR&appid='+API_key+'&units=metric')
        meteo_zip = getData(url)
        meteo_zip['zipcode'] = zipcode
        db.updateCity(meteo_zip)       
        printFromDict(meteo_zip)

    
            
