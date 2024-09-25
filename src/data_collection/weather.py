import requests
from requests.auth import HTTPBasicAuth

latitude = -25.7381
longitude = 27.8569

# Define the API credentials and URLs
client_id = '5mtp9oonnmmvkucj7phr0q3lt6'         # Replace with your client ID
client_secret = 'ob81fml3cjjhhb4kvauhkrs7nc7qc09lapdca6b4besga7v4u0i' # Replace with your client secret
token_url = 'https://auth.afrigis.services/oauth2/token'  # Afrigis token URL
weather_api_url = f'https://afrigis.services/weather-forecast/v1/getDailyByCoords?latitude={latitude}&longitude={longitude}&station_count=3&location_buffer=10000&day_count=7&groups=basic'

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
def fetch_weather_data(access_token, lat, lon):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    params = {
        'lat': lat,
        'lon': lon,
        'days': 7
    }

    response = requests.get(weather_api_url, headers=headers, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        print("Weather Data:", weather_data)
        return weather_data
    else:
        print("Failed to fetch weather data:", response.status_code, response.text)
        return None

# Main function to run the script
if __name__ == "__main__":
    token = get_access_token(client_id, client_secret)
    
    if token:
        # Example: Coordinates for Hartbeespoort Dam
               
        weather_data = fetch_weather_data(token, latitude, longitude)
        if weather_data:
            print("Successfully retrieved weather data!")