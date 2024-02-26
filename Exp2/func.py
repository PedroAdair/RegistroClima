import yaml
import requests
# import folium
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import yaml
from datetime import datetime
from pymongo import MongoClient
import logging


logging.basicConfig(filename='log.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)


import random


def coneccionDB(mongo_uri:str,database_name:str,collection_name:str):
    "coneccion a una colecccion en base de datos"
    try:
        client = MongoClient(mongo_uri)
        db = client[database_name]
        collection = db[collection_name]
        print(f'coneccion exitosa a la coleccion: {database_name}.{collection_name}')
        return collection 
    except Exception as e:
        logging.warning(e)

def GetWeather(coord:list):
    """Coordinates coord= [lat, lon], where lat, lon is latitude and longitude in type float. \n
    Example: [19.29586, -97.768889]. \n
    Invalid formats: 18°55'22.8\" N 98°23'44.3\"W"""
    lat= coord[0]
    lon = coord[1]
    API_key=config['API_key']
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric'
    response = requests.get(url)
    data_weather = response.json()
    return data_weather   
def verification(diccionario, valor):

    for calidad, rango in diccionario.items():
        if 'min' in rango and 'max' in rango:
            if rango['min'] <= valor < rango['max']:
                return calidad
        elif 'min' in rango and valor >= rango['min']:
            return calidad

    return None

def check_wind_speed(diccionario:dict, valor:float):
    Index= {'Calmed down':1, 'Soft breeze':2, 'Moderate Breeze':3, 'Strong wind': 4, 'Storm':5, None: 0}
    ver_txt = verification(diccionario, valor)
    return {'element': 'wind speed','Qualitative name': ver_txt,'Index': Index[ver_txt], 'Value': valor, 'Unit': 'm/s'}

def check_temp(diccionario:dict, valor:float):
    Index= {'Frozen':1, 'Cold':2, 'Moderate':3, 'Warm': 4, 'Very warm':5, None: 0}
    ver_txt = verification(diccionario, valor)
    return {'element': 'temp', 'Qualitative name': ver_txt,'Index': Index[ver_txt], 'Value': valor, 'Unit': '°C'}

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## GetAirPollution

def GetAirPollution(coord:list):
    """Coordinates coord= [lat, lon], where lat, lon is latitude and longitude in type float. \n
    Example: [19.29586, -97.768889]. \n
    Invalid formats: 18°55'22.8\" N 98°23'44.3\"W"""
    lat= coord[0]
    lon = coord[1]
    API_key=config['API_key']
    url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_key}&units=metric'
    response = requests.get(url)
    data_weather = response.json()
    return data_weather   

def check_so2(diccionario:dict, valor:float):
    Index = {'Good':1, 'Fair':2, 'Moderate':3, 'Poor': 4, 'Very Poor':5, None: 0}
    ver_txt = verification(diccionario, valor)
    return {'element': 'pm10','Qualitative name': ver_txt,'Index': Index[ver_txt], 'Value': valor, 'Unit': 'µg/m^3' }

def check_no2(diccionario:dict, valor:float):
    Index = {'Good':1, 'Fair':2, 'Moderate':3, 'Poor': 4, 'Very Poor':5, None: 0}
    ver_txt = verification(diccionario, valor)
    return {'element': 'no2','Qualitative name': ver_txt,'Index': Index[ver_txt], 'Value': valor, 'Unit': 'µg/m^3' }

def check_pm10(diccionario:dict, valor:float):
    Index = {'Good':1, 'Fair':2, 'Moderate':3, 'Poor': 4, 'Very Poor':5, None: 0}
    ver_txt = verification(diccionario, valor)
    return {'element': 'pm10','Qualitative name': ver_txt,'Index': Index[ver_txt], 'Value': valor, 'Unit': 'µg/m^3' }

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
## Warnings and notifications

def CreateReport(code_name:str):
    """
    Get a report about weather, air pollution from a specific area. 

    {
        'code name': code_name,
        'time': 'dd-mm-yyyy hh:mm',
        'temp_report'        :      {'element': 'temp', 'Qualitative name': str,'Index': int, 'Value': float, 'Unit': str},
        'wind_speed_report'  :      {'element': 'temp', 'Qualitative name': str,'Index': int, 'Value': float, 'Unit': str},
        'so2_lvl_report'     :      {'element': 'temp', 'Qualitative name': str,'Index': int, 'Value': float, 'Unit': str},
        'no2_lvl_report'     :      {'element': 'temp', 'Qualitative name': str,'Index': int, 'Value': float, 'Unit': str},
        'pm10_lvl_report'    :      {'element': 'temp', 'Qualitative name': str,'Index': int, 'Value': float, 'Unit': str}
    }

    
    """
    coord =config['cities'][code_name]
    #date info
    date_now = datetime.now()
    date_str = date_now.strftime("%d-%m-%Y %H:%M")

    #weather
    data_weather = GetWeather(coord)
    wind_speed   = data_weather['wind']['speed']
    temp         = data_weather['main']['temp']

    weatherStandars =  config['notifications']['weather']['temp']
    #air pollution
    data_pollution = GetAirPollution(coord=coord)
    so2_lvl        = data_pollution['list'][0]['components']['so2']
    no2_lvl        = data_pollution['list'][0]['components']['no2']
    pm10_lvl       = data_pollution['list'][0]['components']['pm10']

    AirPollutionStandars =  config['notifications']['AirPollution']
    windStandars =  config['notifications']['weather']['wind']
    #
    temp_report       = check_temp(weatherStandars,temp)
    wind_speed_report = check_wind_speed(windStandars,wind_speed)
    # 
    so2_lvl_report  = check_so2(AirPollutionStandars['so2'],so2_lvl)
    no2_lvl_report  = check_no2(AirPollutionStandars['so2'],no2_lvl)
    pm10_lvl_report = check_pm10(AirPollutionStandars['pm10'],pm10_lvl)

    return {
        'code name': code_name,
        'time':date_str,
        'temp_report':temp_report,
        'wind_speed_report':wind_speed_report,
        'so2_lvl_report':so2_lvl_report,
        'no2_lvl_report': no2_lvl_report,
        'pm10_lvl_report': pm10_lvl_report
    }

def NotificationsAndWarmings(code_name:str, insert=True):
    alerts_collection = coneccionDB(config['connection_url'], config['db_ecoterra'], config['alerts_collection'])

    report = CreateReport(code_name=code_name)

    notifications = {clave: valor for clave, valor in report.items() if isinstance(valor, dict) and valor.get('Index', 0) == config['notifications']['indexNotification']}
    if bool(notifications):
        
        notifications['code name']= report['code name']
        notifications['time']= report['time']
        notifications['type']= 'Notification'
        alerts_collection.insert_one(notifications)

    warming  = {clave: valor for clave, valor in report.items() if isinstance(valor, dict) and valor.get('Index', 0) == config['notifications']['indexAlert']}
    if bool(warming):
        warming['code name']= report['code name']
        warming['time']= report['time']
        warming['type']= 'Warming'
        alerts_collection.insert_one(warming)
    
    if insert:
        report_collection = coneccionDB(config['connection_url'], config['db_ecoterra'], config['weather_collection'])
        report_collection.insert_one(report)
    
    if bool(notifications):
        if bool(warming):
            return notifications, warming
        else: 
            return notifications
    else: 
        if bool(warming):
            return warming
        else:
            return None
        

###
        
def message_email():
    alerts = []
    i = 0
    for city in config['cities']:
        report = NotificationsAndWarmings(city, True)
        if report is not None:
            alerts.append(report)
            i +=1
    user = 'Constanza'
    asunto = 'Mensaje clima'
    destinatarios = ['ferphoenix1@gmail.com']

    mensaje = str(alerts)

    msg = MIMEMultipart()
    msg['From']= user
    msg['Subject']= asunto
    msg['To']=  ', '.join(destinatarios)
    msg.attach(MIMEText(mensaje))

    print(len(mensaje))
    if len(mensaje) >2:
        with smtplib.SMTP('smtp.gmail.com') as server:
            server.starttls()
            server.login(config['USER_MAIL'], config['pw'])
            server.sendmail(config['USER_MAIL'],destinatarios, msg.as_string())

        text = f"hubo {i} incidentes"
        logging.info(text)
