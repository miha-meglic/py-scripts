# Retrieves current data from ARSO automatic weather stations and writes it to a CSV
# Units are: time [ISO 8601], temperature and dew_point [°C], humidity [%], pressure [hPa], wind_speed [m/s]
# 	some values may be null

import requests
import xml.etree.ElementTree as et
import pandas as pd
from datetime import datetime

# Get data
req = requests.get('https://meteo.arso.gov.si/uploads/probase/www/observ/surface/text/sl/observationAms_si_latest.xml')
# Parse data
root = et.fromstring(req.text)
# Get data as array of stations
stations = root.findall('metData')

# Initialize data dictionary
data = {
	'id': list(),
	'name': list(),
	'time': list(),
	'temperature': list(),
	'humidity': list(),
	'pressure': list(),
	'dew_point': list(),
	'wind_speed': list()
}

# Parse stations one by one
for station in stations:
	## Data formatting ##
	time = station.find('valid').text.replace('CEST', 'UTC+0200').replace('CET', 'UTC+0100')
	time = datetime.strptime(time, '%d.%m.%Y %H:%M %Z%z') # Parse time to datetime
	
	if station.find('msl').text is None: pressure = None
	else: pressure = float(station.find('msl').text)
	
	if station.find('ff_val').text is None: wind_speed = None
	else: wind_speed = float(station.find('ff_val').text)
	
	## Parsing data to object ##
	data['id'].append(station.find('domain_meteosiId').text)
	data['name'].append(station.find('domain_longTitle').text)
	data['time'].append(time.isoformat())
	data['temperature'].append(float(station.find('t').text) if station.find('t').text else None)
	data['humidity'].append(int(station.find('rh').text) if station.find('rh').text else None)
	data['pressure'].append(pressure)
	data['dew_point'].append(float(station.find('td').text) if station.find('td').text else None)
	data['wind_speed'].append(wind_speed)

# Initialize pandas dataframe
df = pd.DataFrame(data=data)

# Write data to CSV
df.to_csv('data.csv', index=False)