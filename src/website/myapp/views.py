# website/views.py
import sys
import os

from pandas import array

# Add the root project directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from django.shortcuts import render
from src.models.predictive_model import *  # Import your model function

my_predictions = []
array_pos = int(0)
def prediction_view(request):
    global my_predictions
    data = []  # Default empty data in case the user hasn't submitted the form
    alert_message = None  # Initialize alert message
    if request.method == 'POST':
        start_size = float(request.POST.get('start_size_input', 0))
        days = int(request.POST.get('days_input', 0))

        #Prints Old prediction values
        print("OLD: ")
        for row in my_predictions:
            print(*row, sep="\t")

        my_predictions.clear()
        # Call your prediction model function
        my_predictions, avg_size = daily_predictions_json(start_size, days)

        #Prints new predicted values
        print("New: ")
        for row in my_predictions:
            print(*row, sep="\t")

        # Generate alert message
        alert_message = send_Alert(avg_size)
        
        # Format the predictions data to match the table structure
        data = [
            {
                'Date': pred[0], 
                'Temperature': pred[1],
                'Wind_Speed': pred[2],
                'Wind_Direction': pred[3],
                'Start_Size': str(pred[4])+'%',
                'Predicted_End_Size': str(pred[5])+'%'
            } 
            for pred in my_predictions
        ]
    my_context = {'data': data, 'alert_message': alert_message}
    my_context.update(redo_map(0))

    return render(request, 'index.html', my_context)

def redo_predictions():
    global my_predictions, array_pos
    array_pos = 0

def redo_map(pos):
    global my_predictions, array_pos

    coverage_percentage = my_predictions[pos][5]

    context = {'coverage_percentage': str(coverage_percentage)+'%', 'coverage_description': coverage_description(coverage_percentage), 'image_path': coverage_image(coverage_percentage), 'coverage_date': my_predictions[pos][0]}
    print(context)
    return context

def coverage_description(size):
    if size <= 10:
        return "Low Coverage"
    elif size <= 25:
        return "Medium Coverage"
    elif size <= 50:
        return "High Coverage"

def coverage_image(size):
    if size <= 10:
        return "low.png"
    elif size <= 25:
        return "medium.png"
    elif size <= 50:
        return "high.png"