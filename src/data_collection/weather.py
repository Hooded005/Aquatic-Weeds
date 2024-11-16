import requests
import json
import csv
import pandas as pd
import os
from dotenv import load_dotenv

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
json_path = os.path.join(base_dir, 'data/new/weather.json')

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
    
def json_to_csv():
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)

# Open the CSV file in write mode
    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        # Write the header (keys from the JSON objects)
        header = data[0].keys() if data else []
        writer.writerow(header)

        # Write the data (values from each JSON object)
        for row in data:
            writer.writerow(row.values())
    print("JSON data has been successfully converted to CSV.")

def extract_json():
    # Initialize an empty array to store the extracted data
    extracted_data = []

    # Load the JSON data from the file
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)

        # Extract specific fields from each entry in the JSON
        for entry in data:
            temp = entry.get('temp')
            speed = entry.get('speed')
            direction = entry.get('direction')
            start_size = entry.get('start_size')
            
            # Append the extracted data as a list to the array
            extracted_data.append([temp, speed, direction, start_size])
    return extracted_data