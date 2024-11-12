from django.shortcuts import render
import pandas as pd
import os
from datetime import datetime, timedelta  # Ensure the necessary imports

# Function to convert degrees to cardinal direction
def degrees_to_cardinal(degrees):
    directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    idx = int((degrees + 11.25) / 22.5) % 16
    return directions[idx]

# Create your views here
def home(request):
    # Path to the CSV file
    csv_path = os.path.join(os.path.dirname(__file__), 'weather.csv')

    # Reading CSV file with pandas
    df = pd.read_csv(csv_path, delimiter=';')  # Ensure the correct delimiter

    # Rename the columns to match the specified headings
    df.columns = ["Temperature", "Wind_Speed", "Wind_Direction", "Patch_Size"]

    # Convert wind direction from degrees to cardinal directions
    df['Wind_Direction'] = df['Wind_Direction'].apply(degrees_to_cardinal)

    # Convert the DataFrame to a list of dictionaries for rendering
    data = df.to_dict(orient='records')

    # Generate ascending dates starting from tomorrow
    start_date = datetime.now() + timedelta(days=1)
    dates = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(len(data))]

    # Combine the dates with the data and calculate days from today
    for i, row in enumerate(data):
        row['Date'] = dates[i]
        row['Days_From_Today'] = i + 1

    #first_record = data[0]

    return render(request, "index.html", {'data': data})
