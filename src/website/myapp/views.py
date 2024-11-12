# website/views.py
import sys
import os

# Add the root project directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from django.shortcuts import render
from src.models.predictive_model import *  # Import your model function

def prediction_view(request):
    data = []  # Default empty data in case the user hasn't submitted the form
    if request.method == 'POST':
        start_size = float(request.POST.get('start_size_input', 0))
        days = int(request.POST.get('days_input', 0))
        
        # Call your prediction model function
        predictions = daily_predictions(start_size, days)
        
        # Format the predictions data to match the table structure
        data = [
            {
                'Date': pred[0], 
                'Temperature': pred[1],
                'Wind_Speed': pred[2],
                'Wind_Direction': pred[3],
                'Start_Size': pred[4],
                'Predicted_End_Size': pred[5]
            } 
            for pred in predictions
        ]
    
    return render(request, 'index.html', {'data': data})
