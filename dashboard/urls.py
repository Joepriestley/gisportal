from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('main-dashboard/', views.main_dashboard, name='main-dashboard'),
    path('add-data/', views.addData, name='add-data')
]
