from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse

# Create your views here.
def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect to the main dashboard using the namespace and name
            return redirect(reverse('dashboard:main-dashboard'))
        else:
            messages.error(request, "There was an error logging in, try again.")
            return render(request, 'authenticate/login.html', {})  # Render the login page with an error
    else:
        return render(request, 'authenticate/login.html', {})  # Render the login page
