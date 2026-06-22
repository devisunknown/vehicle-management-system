from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login 
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse

from patrick.models import registedvehicle

def loginpg(request):
    return render(request, 'scancoat.html')

def login(request):
    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')
        
        
        user = authenticate(request, username=username_input, password=password_input)
        
   
        if user is not None:
            auth_login(request, user) 
            return render(request, 'pat.html')
        
        else:
            messages.error(request, 'Invalid username or password please try again.')
            return redirect('loginpg')
            
    return redirect('loginpg')

def patrickprof(request):
    return render(request, 'patrickp.html')

def register(request):
    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')
        
        if User.objects.filter(username=username_input).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')
        
        User.objects.create_user(username=username_input, password=password_input)
        
        messages.success(request, 'User registered successfully!')
        return redirect('loginpg')
        
    return render(request, 'patrickp.html')



def vehicle_list(request):
    from .models import registedvehicle
    if request.method == 'POST':
        department = request.POST.get('department')
        vehicle_model = request.POST.get('vehicle_model')
        license_plate = request.POST.get('license_plate')
        intialprogress = request.POST.get('intialprogress')
        startdate = request.POST.get('startdate')
        issue= request.POST.get('issue_description')
        reg=registedvehicle(department=department, vehicle_model=vehicle_model, license_plate=license_plate, intialprogress=intialprogress, startdate=startdate, issue=issue)
        reg.save()
    return HttpResponse("Vehicle registered successfully.")   


def vehicleview(request):
    vehicles=registedvehicle.objects.all()
    return render(request, 'vehicle_list.html', {'vehicles': vehicles})


def dashboard(request):
    return render(request, 'pat.html')