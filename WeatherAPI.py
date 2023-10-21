# %%
import requests
api_key = '2a8be53043c3523cb8f9e00f4843aa8c'
city_name = "mangalore" #you can ask for user input instead

#Let's get the city's coordinates (lat and lon)
url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
print(url)

#Let's parse the Json
req = requests.get(url)
data = req.json()

#Let's get the name, the longitude and latitude
name = data['name']

lon = 74.794
lat = 13.35
# lon = data['coord']['lon']
# lat = data['coord']['lat']


print(name, lon, lat)

# %%
import json
import csv

url2 = f'https://pro.openweathermap.org/data/2.5/forecast/hourly?lat={lat}4&lon={lon}&appid={api_key}'
print(url2)

#Let's now parse the JSON
req2 = requests.get(url2)
data2 = req2.json()
temp = round(((data2['list'][0]['main']['temp_min'] + data2['list'][0]['main']['temp_max'])/2) - 273,2)
print(temp)
humid = data2['list'][0]['main']['humidity']
print(humid)
wind = round(data2['list'][0]['wind']['speed']*10,2)
print(wind)



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



