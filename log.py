def printMessage(msg):
    print(msg)

def printFromDict(meteo_city):
    print("Temperature:", meteo_city["main_temp"], "\nT.ressentie:", meteo_city["main_feels_like"], "\nPression:", meteo_city["main_pressure"], "\nHumidité:", meteo_city["main_humidity"], "\nKm/h:", meteo_city["wind_speed"])