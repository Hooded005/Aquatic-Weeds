import requests
import csv
import pandas as pd

# Coordinates and API credentials
latitude = -25.7381
longitude = 27.8569
days = input("Enter the amount of days between 1 and 7: ");

client_id = '5mtp9oonnmmvkucj7phr0q3lt6'
client_secret = 'ob81fml3cjjhhb4kvauhkrs7nc7qc09lapdca6b4besga7v4u0i'
api_key = 'BgGPhMfSQC8CzgqFci2ze7aKYpG9QcHD351i11Fo'
token_url = 'https://auth.afrigis.services/oauth2/token'
weather_api_url = f'https://afrigis.services/weather-forecast/v1/getDailyByCoords?latitude={latitude}&longitude={longitude}&station_count=3&location_buffer=10000&day_count={days}&groups=basic'

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
        file_path = "data/new/weather.csv"
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
    file_path = "data/new/weather.csv"
    # Load the CSV file to get headers
    data = pd.read_csv(file_path)        
    # Create a DataFrame with only the header
    cleared_data = pd.DataFrame(columns=data.columns)        
    # Save back to the CSV, overwriting existing data but keeping the header
    cleared_data.to_csv(file_path, index=False)