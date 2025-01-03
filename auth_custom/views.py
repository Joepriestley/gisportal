from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def login_user(request):
    if request.method == 'POST':
        
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard/main-dashboard')
            # Redirect to a success page.
        else:
            messages.success(request, ("There was an error logging in , try again..."))
            return render(request, 'authenticate/login.html',{})
            # Return an 'invalid login' error message.
    else:
        return render(request,'authenticate/login.html',{})
