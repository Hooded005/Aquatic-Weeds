import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, accuracy_score

# Sample data: Replace with actual CSV file loading
data = pd.read_csv('data\\processed\\CompleteData.csv', sep=';')

# Encode categorical variables
label_encoder = LabelEncoder()
data['start_pos'] = label_encoder.fit_transform(data['start_pos'])
data['end_pos'] = label_encoder.fit_transform(data['end_pos'])  # Also for classification

# Split data into features (X) and labels (y)
X = data[['start_pos', 'temp', 'speed', 'direction', 'start_size', 'days']]
y_size = data['end_size']
y_pos = data['end_pos']

# Split for end_size regression
X_train_size, X_test_size, y_train_size, y_test_size = train_test_split(X, y_size, test_size=0.2, random_state=42)

# Train a Random Forest Regressor for end_size prediction
rf_regressor = RandomForestRegressor()
rf_regressor.fit(X_train_size, y_train_size)

# Predict and evaluate
y_pred_size = rf_regressor.predict(X_test_size)
mse = mean_squared_error(y_test_size, y_pred_size)
print(f"Mean Squared Error (end_size): {mse}")

# Split for end_pos classification
X_train_pos, X_test_pos, y_train_pos, y_test_pos = train_test_split(X, y_pos, test_size=0.2, random_state=42)

# Train a Random Forest Classifier for end_pos prediction
rf_classifier = RandomForestClassifier()
rf_classifier.fit(X_train_pos, y_train_pos)

# Predict and evaluate
y_pred_pos = rf_classifier.predict(X_test_pos)
accuracy = accuracy_score(y_test_pos, y_pred_pos)
print(f"Accuracy (end_pos): {accuracy}")
