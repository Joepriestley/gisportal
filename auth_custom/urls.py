from django.urls import path
from . import views

app_name ='auth_custom'

urlpatterns=[
   
    path('', views.login_user, name="registration/login")
    ]