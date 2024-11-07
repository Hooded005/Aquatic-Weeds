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

def fetch_and_prepare_weather_data(start_size):
    """Fetch weather data and write it with updated start_size for each day."""
    token = get_access_token()
    if token:
        weather_data = fetch_weather_data(token)
        if weather_data:
            forecasts = extract_forecast_details(weather_data, start_size)
            return forecasts  # Extracted weather data for each day

def predict_next_size(start_size):
    """Predict the next day's end_size using the current start_size."""
    # Load the trained model
    model = pickle.load(open(filename, 'rb'))
    
    # Prepare the data row for prediction
    predict_data = pd.read_csv(weather_file_path, sep=';')
    predict_line = pd.DataFrame([predict_data[['temp', 'speed', 'direction']].iloc[-1].tolist() + [start_size]],
                                columns=['temp', 'speed', 'direction', 'start_size'])
    
    # Make the prediction
    predicted_end_size = model.predict(predict_line)[0]  # Get a single prediction
    return predicted_end_size

def sequential_prediction(start_size, days):
    results = []
    
    for day in range(days):
        # Fetch weather data for each day with the current start_size
        weather_data = fetch_and_prepare_weather_data(start_size)
        
        # Append to weather CSV file
        with open(weather_file_path, mode='a', newline='') as file:
            writer = csv.writer(file, delimiter=";")
            for row in weather_data:
                # Write temp, speed, direction, and start_size
                writer.writerow([row[0], row[1], row[2], start_size])
                
                # Prepare the output line
        result = f"Day {day + 1}: Temp {row[0]}, Speed {row[1]}, Direction {row[2]}, Start Size {start_size}, "
        results.append(result)
                
        # Predict end_size for the current day and update start_size for the next day
        predicted_end_size = predict_next_size(start_size)
        results[-1] += f"Predicted End Size: {predicted_end_size}"
        start_size = predicted_end_size  # Update start size for next day's prediction
    return results

# Example usage:
for i in range(days):
    print(f"{sequential_prediction(start_size, days)[i]}\n")

clear_weather()  # Clears the CSV file before starting