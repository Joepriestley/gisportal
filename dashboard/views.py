from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'dashboard/main-dashboard.html')

def addData(request):
    return render(request, 'dashboard/add-data.html')

    
