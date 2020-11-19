# Retrieves latest SARS-CoV-2 (COVID-19) data for Slovenia from gov.si and writes it to a JSON
# Data is described on lines 14->22
#	some data is in delta form (change from previous day) and some is absolute

import csv
import json
from datetime import datetime
import requests

# Retrieve data from gov.si
csv_data = requests.get('https://www.gov.si/teme/koronavirus-sars-cov-2/element/67900/izvoz.csv').text.splitlines()
data = list(csv.DictReader(csv_data))[0]

# Parse retrieved data
data = {
	'date': datetime.strptime(data['Datum'], '%Y-%m-%d %H:%M:%S').strftime('%a, %d %b %Y'),  # Date of data update
	'tested': int(data['Opravljeni testi']),  # People newly tested
	'positive': int(data['Pozitivne osebe']),  # People newly tested positive
	'hospitalized': int(data['Hospitalizirane osebe']),  # People currently hospitalized
	'icu': int(data['Osebe na intenzivni negi']),  # People currently on intensive care
	'released': int(data['Odpuščeni iz bolnišnice']),  # People newly released from hospital
	'died': int(data['Umrli'])  # New deaths
}

# Write data to json
with open('data.json', 'w') as file:
	json.dump(data, file, indent='\t')
