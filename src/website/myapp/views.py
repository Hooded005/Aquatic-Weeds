# website/views.py
import sys
import os

# Add the root project directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from django.shortcuts import render
from src.models.predictive_model import *  # Import your model function

def prediction_view(request):
    data = []  # Default empty data in case the user hasn't submitted the form
    alert_message = None  # Initialize alert message
    if request.method == 'POST':
        start_size = float(request.POST.get('start_size_input', 0))
        days = int(request.POST.get('days_input', 0))
        
        # Call your prediction model function
        predictions, avg_size = daily_predictions_json(start_size, days)
        
        # Generate alert message
        alert_message = send_Alert(avg_size)
        
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
        predictions.clear()
    
    return render(request, 'index.html', {'data': data, 'alert_message': alert_message})