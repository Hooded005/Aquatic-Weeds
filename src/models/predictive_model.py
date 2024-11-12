import sys
import os

# Add the root project directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.data_collection.weather import *

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import pickle
import datetime as dt

dataArray = [];

# Load historical data for training# Get the absolute path to the root directory
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

# Construct the full path to the CSV file
csv_path = os.path.join(base_dir, 'data/historical/CompleteData.csv')
weather_file_path = os.path.join(base_dir, 'data/new/weather.csv')
filename = os.path.join(base_dir, 'size_Predictor.pkl')

# Load the CSV file
data = pd.read_csv(csv_path, sep=';')
X = data[["temp", "speed", "direction", "start_size"]]
y_size = data['end_size']

def train_model():
    """Train and save the model for predicting end_size."""
    accuracy = 0
    while accuracy <= 85:
        # Split data for training the model
        X_train, X_test, y_train, y_test = train_test_split(X, y_size, test_size=0.2, random_state=42)
        
        # Train the Random Forest model
        rf_regressor = RandomForestRegressor()
        rf_regressor.fit(X_train, y_train)
        
        # Save the model
        pickle.dump(rf_regressor, open(filename, "wb"))
        
        # Calculate Mean Squared Error to determine accuracy
        y_pred = rf_regressor.predict(X_test)
        accuracy = mean_squared_error(y_test, y_pred)
        print(f"Mean Squared Error (end_size): {accuracy}")

# Train the model before predictions
""" train_model() """

def predict_next_size(start_size, temp, speed, direction):
    model = pickle.load(open(filename, 'rb'))
    predict_line = pd.DataFrame([[temp, speed, direction, start_size]], columns=['temp', 'speed', 'direction', 'start_size'])
    return model.predict(predict_line)[0]



# Main function for sequential predictions
def daily_predictions(start_size, days):
    clear_weather()
    date = dt.date.today();
    
    for day in range(days):
        token = get_access_token()
        if token:
            weather_data = fetch_weather_data(token)
            if weather_data:
                # Get forecast for the current day
                forecasts = extract_forecast_details(weather_data, start_size)
                day_forecast = forecasts[day]  # Get forecast for the current day
                temp, speed, direction = day_forecast[0], day_forecast[1], day_forecast[2]
                
                # Write to CSV for reference
                with open(weather_file_path, mode='a', newline='') as file:
                    writer = csv.writer(file, delimiter=";")
                    start_size = round(start_size, 2)
                    writer.writerow([temp, speed, direction, start_size])
                
                initial_size = start_size    
                # Predict and set new start size for the next day
                start_size = predict_next_size(start_size, temp, speed, direction)
                # print(f"Day {day}: Temp {temp}, Speed {speed}, Direction {direction}, Start Size {initial_size:.2f}, Predicted End Size: {start_size:.2f}")
                dataArray.append([date, temp, speed, direction, round(float(initial_size),2), round(float(start_size),2)]);                
                date += dt.timedelta(days=1)
    return dataArray

daily_predictions(10, 5);