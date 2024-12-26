from django.urls import path
from . import views

app_name ='dashboard'

urlpatterns=[
    path('main-dashboard/',views.index, name="dashboard/main-dashboard"),
    path('add-data/',views.addData, name="dashboard/add-data"),
]