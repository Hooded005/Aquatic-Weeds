import requests
import csv
import pandas as pd
import os
from dotenv import load_dotenv
import json

# Coordinates and API credentials
latitude = -25.7381
longitude = 27.8569
days = 7

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
api_key = os.getenv("API_KEY")
token_url = 'https://auth.afrigis.services/oauth2/token'
weather_api_url = f'https://afrigis.services/weather-forecast/v1/getDailyByCoords?latitude={latitude}&longitude={longitude}&station_count=3&location_buffer=10000&day_count={days}&groups=basic'

# Load historical data for training# Get the absolute path to the root directory
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
file_path = os.path.join(base_dir, 'data/new/weather.csv')

# ==============================JSON FILE BACKUP===================================
# Define the path to the sample JSON file
json_file_path = os.path.join(base_dir, 'data/new/weather.json')

def extract_sample_forecast_details(predicted_size):
    """Extract forecast details from the sample JSON file."""
    weather_Data = []
    
    # Open and load the JSON file
    with open(json_file_path, 'r') as json_file:
        sample_data = json.load(json_file)
    
    # Process the data
    for day in sample_data:
        temp_avg = day['temperature']
        wind_speed = day['wind_speed']
        wind_direction = day['wind_direction']
        weather_Data.append([temp_avg, wind_speed, wind_direction, predicted_size])
    
    return weather_Data
# ==============================JSON FILE BACKUP===================================

def get_access_token():
    """Fetch the OAuth2 token."""
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(token_url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        print("Failed to retrieve access token:", response.status_code, response.text)
        return None

def fetch_weather_data(access_token):
    """Fetch weather data using the access token."""
    headers = {
        'Authorization': f'Bearer {access_token}',
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }
    response = requests.get(weather_api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch weather data:", response.status_code, response.text)
        return None

def extract_forecast_details(weather_data, predicted_size):
    """Extract forecast details and save them to a CSV file."""
    if 'result' in weather_data:
        forecasts = weather_data['result'][0]['forecasts']
        weather_Data = [];
        counter = 0
        
        with open(file_path, mode='a', newline='') as file:
            for day in forecasts:
                temp_avg = day['basic']['temperature_apparent']
                wind_speed = day['basic']['wind_speed']
                wind_direction = day['basic']['wind_direction_degrees']
                weather_Data.append([temp_avg, wind_speed, wind_direction, predicted_size])
                counter += 1
                """ print("Result: " + str(counter) + "\n")
                print(weather_Data)
                print("\n") """
    return weather_Data;
                
def clear_weather():
    # Load the CSV file to get headers
    data = pd.read_csv(file_path)        
    # Create a DataFrame with only the header
    cleared_data = pd.DataFrame(columns=data.columns)        
    # Save back to the CSV, overwriting existing data but keeping the header
    cleared_data.to_csv(file_path, index=False)