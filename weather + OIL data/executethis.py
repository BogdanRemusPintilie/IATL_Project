import requests
import pandas as pd
import datetime as dt
import os

# Constants
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
API_KEY = "aef4e5249b8843ca1c567108af2766d7"
CITIES = ["Dubai", "Texas", "London"]
CSV_FILE = 'weather_data.csv'

# Function to convert Kelvin to Celsius
def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

# Function to fetch weather data
def fetch_weather_data(city):
    url = BASE_URL + "appid=" + API_KEY + "&q=" + city
    response = requests.get(url).json()
    data = {
        'city': city,
        'temperature_celsius': round(kelvin_to_celsius(response['main']['temp']), 2),
        "humidity": response['main']['humidity'],
        "wind speed": response['wind']['speed'],
        'datetime': dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    return data

# Fetch data for each city
weather_data = [fetch_weather_data(city) for city in CITIES]

# Convert to DataFrame
df = pd.DataFrame(weather_data)

# Check if CSV file exists
if not os.path.isfile(CSV_FILE):
    # If the file does not exist, create it and write headers
    df.to_csv(CSV_FILE, index=False, mode='w')
    print(f"Weather data has been created and named {CSV_FILE}")
else:
    # If the file exists, append data without writing headers
    df.to_csv(CSV_FILE, index=False, mode='a', header=False)
    print(f"Weather data has been appended to {CSV_FILE}")