import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error

# Load the data from the CSV file
data = pd.read_csv('data\\historical\\CompleteData.csv', sep=';')

# Split data into features (X) and labels (y)
X = data[['temp', 'speed', 'direction', 'start_size']]
y_size = data['end_size']

# Split for end_size regression
X_train_size, X_test_size, y_train_size, y_test_size = train_test_split(X, y_size, test_size=0.2, random_state=42)

# Train a Random Forest Regressor for end_size prediction
rf_regressor = RandomForestRegressor()
rf_regressor.fit(X_train_size, y_train_size)

# Predict and evaluate for end_size
y_pred_size = rf_regressor.predict(X_test_size)
mse = mean_squared_error(y_test_size, y_pred_size)
print(f"Mean Squared Error (end_size): {mse}")

# Print actual vs predicted for end_size
print("\nPredicted vs Actual for end_size:")
for pred, actual in zip(y_pred_size, y_test_size):
    print(f"Predicted: {pred:.2f}, Actual: {actual}")
