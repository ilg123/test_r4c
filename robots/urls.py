from django.urls import path
from .views import create_robot, generate_excel_report

urlpatterns = [
    path('create_robot/', create_robot, name='create_robot'),
    path('create_report/', generate_excel_report, name='create_report'),
]
