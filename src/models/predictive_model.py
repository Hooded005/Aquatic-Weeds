import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error
import pickle
from src.data_collection.weather import *

# Load the data from the CSV file
data = pd.read_csv('data\\historical\\CompleteData.csv', sep=';');
predictData = pd.read_csv('data\\new\\weather.csv', sep=';');
filename = "size_Predictor.pkl";

# Split data into features (X) and labels (y)
X = data[['temp', 'speed', 'direction', 'start_size']]
y_size = data['end_size']

predictor = predictData[['temp', 'speed', 'direction', 'start_size']]

def trainModel():
    accuracy = 0;
    while accuracy <= 85:
        # Split for end_size regression
        X_train_size, X_test_size, y_train_size, y_test_size = train_test_split(X, y_size, test_size=0.2, random_state=42)

        # Train a Random Forest Regressor for end_size prediction
        rf_regressor = RandomForestRegressor()
        rf_regressor.fit(X_train_size, y_train_size)

        pickle.dump(rf_regressor, open(filename, "wb"))

        # Predict and evaluate for end_size
        y_pred_size = rf_regressor.predict(X_test_size)
        accuracy = mean_squared_error(y_test_size, y_pred_size)
        print(f"Mean Squared Error (end_size): {accuracy}")

# Print actual vs predicted for end_size
trainModel();

""" extract_forecast_details() """

def predict():
    model = pickle.load(open(filename, 'rb'))
    y_pred = model.predict(predictor)
    return y_pred

print(f"", predictor,
      "\nPredicted size: ", predict());