from django.urls import path
from . import views

urlpatterns = [
    path('', views.prediction_view, name='prediction_view'),
    path('prediction_view/', views.prediction_view, name='prediction_view'),
    path('cycle/<str:direction>/', views.cycle_data_view, name='cycle_data'),
]
