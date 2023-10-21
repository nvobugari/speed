# %%
import tensorflow as tf
import tensorflow.keras as tfk
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from fun import prepro
from jinja2 import Template

import requests
api_key = '2a8be53043c3523cb8f9e00f4843aa8c'
lat = 13.351865197444729
lon = 74.79410422116098

# %%
import json
import csv

url2 = f'https://pro.openweathermap.org/data/2.5/forecast/hourly?lat={lat}4&lon={lon}&appid={api_key}'

#Let's now parse the JSON
req2 = requests.get(url2)
data2 = req2.json()

# %%
extracted_data = []
count = 0
for item in data2['list']:
    count = count+1
    dt = item['dt_txt']
    temp_min = item['main']['temp_min']
    temp_max = item['main']['temp_max']
    humidity = item['main']['humidity']
    precipitation = item.get('rain', {}).get('1h', 0)
    wind_speed = item['wind']['speed']

    avg_temp = (temp_min + temp_max)/2
    extracted_data.append({
        'timestamp': dt,
        'temperature': round(avg_temp-273,2),
        'humidity': round(humidity,2),
        'precipitation': round(precipitation,2),
        'wind_speed': round(wind_speed,2),
        'location' : 'Mangalore'
    })
    if count == 5: break

# Write the extracted data to a CSV file
csv_filename = 'weather_data_new.csv'
csv_headers = ['timestamp', 'location', 'temperature', 'humidity', 'wind_speed', 'precipitation']

with open(csv_filename, mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader()
    writer.writerows(extracted_data)

# %%


# %%


model = tfk.Sequential()
model.add(tfk.Input(shape = (4,4)))
model.add(tfk.layers.Bidirectional(tfk.layers.LSTM(128, return_sequences=True)))
model.add(tfk.layers.ReLU())
model.add(tfk.layers.Dropout(0.3))
model.add(tfk.layers.Bidirectional(tfk.layers.LSTM(256, return_sequences=True)))
model.add(tfk.layers.ReLU())
model.add(tfk.layers.Dropout(0.3))
model.add(tfk.layers.Bidirectional(tfk.layers.LSTM(256, return_sequences=True)))
model.add(tfk.layers.ReLU())
model.add(tfk.layers.Dropout(0.3))
model.add(tfk.layers.LSTM(128, return_sequences=False))
model.add(tfk.layers.ReLU())
model.add(tfk.layers.Dense(1))

# %%
model.load_weights(r'Pretrained Weights\po_hour').expect_partial()

# %%
data = pd.read_csv(r'weather_data_new.csv')
data.drop(columns=['location'], inplace=True)
data['timestamp'] = pd.to_datetime(data['timestamp'])
data.set_index('timestamp')

# %%

X = prepro(data)

# %%
gen = tfk.preprocessing.sequence.TimeseriesGenerator(np.asarray(X),np.asarray(X),length=4,sampling_rate=1,stride=1,batch_size=32)

d = data.to_html()
print(d,'<br>')
# %%
yhat = model.predict(gen)
print('<br><br>')

# %%
yhat = [1 if x > 0.5 else 0 for x in yhat]
yhat

# %%
if yhat[0] == 0:
    print('<br>NO DETECTABLE POWER OUTAGE IN THE COMING HOUR<br>')
else:
    print('<br>POSSIBILITY OF POWER OUTAGE IN THE COMING HOUR<br>')






