from django.shortcuts import render

# Create your views here.
def main_dashboard(request):
    return render(request, 'dashboard/main-dashboard.html')  # Specify the full path to the template

def addData(request):
    return render(request, 'dashboard/add-data.html')  # Specify the full path to the template
