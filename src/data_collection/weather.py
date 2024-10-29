import requests
from requests.auth import HTTPBasicAuth
import csv

latitude = -25.7381
longitude = 27.8569
days = 3

# Define the API credentials and URLs
client_id = '5mtp9oonnmmvkucj7phr0q3lt6'         # Replace with your client ID
client_secret = 'ob81fml3cjjhhb4kvauhkrs7nc7qc09lapdca6b4besga7v4u0i' # Replace with your client secret
api_key = 'BgGPhMfSQC8CzgqFci2ze7aKYpG9QcHD351i11Fo' # Replace with your API key
token_url = 'https://auth.afrigis.services/oauth2/token'  # Afrigis token URL
weather_api_url = f'https://afrigis.services/weather-forecast/v1/getDailyByCoords?latitude={latitude}&longitude={longitude}&station_count=3&location_buffer=10000&day_count={days}&groups=basic'

# Step 1: Get OAuth2 token
def get_access_token(client_id, client_secret):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    
    response = requests.post(token_url, headers=headers, data=data)
    
    if response.status_code == 200:
        token = response.json().get('access_token')
        print("Access Token:", token)
        return token
    else:
        print("Failed to retrieve access token:", response.status_code, response.text)
        return None

# Step 2: Fetch weather data from the API
def fetch_weather_data(access_token, lat, lon, api_key):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'x-api-key': api_key,  # Add the API key here
        'Content-Type': 'application/json'
    }
    params = {
        'lat': lat,
        'lon': lon,
        'days': days
    }

    response = requests.get(weather_api_url, headers=headers, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        # print("Weather Data:", weather_data)
        return weather_data
    else:
        print("Failed to fetch weather data:", response.status_code, response.text)
        return None

# Main function to run the script
if __name__ == "__main__":
    token = get_access_token(client_id, client_secret)
    
    if token:
        weather_data = fetch_weather_data(token, latitude, longitude, api_key)
        if weather_data:
            print("Successfully retrieved weather data!")

def extract_forecast_details(weather_data):
    if 'result' in weather_data:
        forecasts = weather_data['result'][0]['forecasts']  # Get the forecasts list
        
        for day in forecasts:
            date = day['date']
            description = day['basic']['description']
            temp_avg = day['basic']['temperature_apparent']
            wind_speed = day['basic']['wind_speed']
            wind_direction = day['basic']['wind_direction_degrees']
            
            # Print or store the information
            print("-" * 30)
            print(f"Date: {date}")
            print(f"Description: {description}")
            print(f"Temperature Average: {temp_avg}°C")
            print(f"Wind Speed: {wind_speed} km/h")
            print(f"Wind Direction: {wind_direction}°")
            
            file_path = "data\\new\\weather.csv";

            with open(file_path, mode='a', newline='') as file:
                writer = csv.writer(file, delimiter=";");
                writer.writerow([temp_avg, wind_speed, wind_direction]);

extract_forecast_details(weather_data)