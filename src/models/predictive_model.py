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

# Initial user input
start_size = float(input("What is the initial start size: "))
days = int(days)

# File paths
filename = "size_Predictor.pkl"
weather_file_path = "data/new/weather.csv"

# Load historical data for training
data = pd.read_csv('data/historical/CompleteData.csv', sep=';')
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
                print(f"Day {day + 1}: Temp {temp}, Speed {speed}, Direction {direction}, Start Size {initial_size:.2f}, Predicted End Size: {start_size:.2f}")

clear_weather()

# Run daily predictions
daily_predictions(start_size, days)