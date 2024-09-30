from django.urls import path 
from .  import views

#urlconfig definition
urlpatterns =[
    path('gisportal/', views.cesium_view)
]