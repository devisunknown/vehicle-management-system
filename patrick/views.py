from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login 
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from patrick.models import registedvehicle
from django.contrib.auth.decorators import login_required
from django.db.models import Count
import json
from django.db import IntegrityError

def loginpg(request):
    return render(request, 'scancoat.html')

def scancoatadmin(request):
    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')
       
        
        user = authenticate(request, username=username_input, password=password_input)
        
   
        if user is not None:
            auth_login(request, user) 
            return redirect('dashboard')
        
        else:
            messages.error(request, 'Invalid username or password please try again.')
            return redirect('loginpg')
            
    return redirect('loginpg')
@login_required
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
    if request.method == 'POST':
        department = request.POST.get('department')
        vehicle_model = request.POST.get('vehicle_model')
        license_plate = request.POST.get('license_plate')
        intialprogress = request.POST.get('intialprogress')
        issue_description = request.POST.get('issue_description')
        order_number = request.POST.get('ordernumber')  
        
        reg = registedvehicle(
            department=department,
            vehicle_model=vehicle_model,
            license_plate=license_plate,
            intialprogress=intialprogress,
            issue=issue_description,
            order_number=order_number
        )
        
        try:
            reg.save()
            
            return redirect('vehicle_list')
        except IntegrityError:
            return render(request, 'vehicle_list.html', {
                'error_msg': f"The license plate '{license_plate}' is already in use.",
                'formData': request.POST,
                'vehicles': registedvehicle.objects.all()
            })

    query = request.GET.get('search', '').strip()
    if query:
        vehicles = registedvehicle.objects.filter(
            Q(department__icontains=query) | Q(license_plate__icontains=query) | Q(order_number__icontains=query)
        )
    else:
        vehicles = registedvehicle.objects.all()

    return render(request, 'vehicle_list.html', {
        'vehicles': vehicles,
        'query': query,
    })
            
    


@login_required
def vehicleview(request):
    query = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()
    department = request.GET.get('department', '').strip()
    date_from = request.GET.get('date_from', '').strip()
    date_to = request.GET.get('date_to', '').strip()

    vehicles = registedvehicle.objects.all()

    if query:
        vehicles = vehicles.filter(
            Q(department__icontains=query) | Q(license_plate__icontains=query) | Q(order_number__icontains=query)
        )

    if status:
        vehicles = vehicles.filter(intialprogress=status)

    if department:
        vehicles = vehicles.filter(department=department)

    if date_from:
        vehicles = vehicles.filter(startdate__gte=date_from)

    if date_to:
        vehicles = vehicles.filter(startdate__lte=date_to)
        

    departments = registedvehicle.objects.values_list('department', flat=True).distinct()

    return render(request, 'vehicle_list.html', {
        'vehicles': vehicles,
        'query': query,
        'status': status,
        'department': department,
        'date_from': date_from,
        'date_to': date_to,
        'departments': departments,
    })

@login_required  
def dashboard(request):
    return render(request, 'pat.html')

@login_required
def delete_vehicle(request, vehicle_order_number):
  
    try:
        vehicle = registedvehicle.objects.get(order_number=vehicle_order_number)
        vehicle.delete()
    except registedvehicle.DoesNotExist:
        pass 
        
    return redirect('vehicle_list')
@login_required
def data(request):
    total_fleet = registedvehicle.objects.count()
    
    pending_count = registedvehicle.objects.filter(intialprogress__icontains='progress').count()
    completed_count = registedvehicle.objects.filter(intialprogress__icontains='complete').count()
    
    recent_vehicles = registedvehicle.objects.all().order_by('-id')[:5]

    dept_counts = registedvehicle.objects.values('department').annotate(total=Count('id')).order_by('-total')
    

    if dept_counts.exists():
        bar_labels = [item['department'] if item['department'] else 'Unassigned' for item in dept_counts]
        bar_values = [item['total'] for item in dept_counts]
    else:
        bar_labels = ['No Data Available']
        bar_values = [0]

    status_counts = registedvehicle.objects.values('intialprogress').annotate(total=Count('id'))
    if status_counts.exists():
        pie_labels = [item['intialprogress'] if item['intialprogress'] else 'Unknown' for item in status_counts]
        pie_values = [item['total'] for item in status_counts]
    else:
        pie_labels = ['No Data Available']
        pie_values = [0]

    return render(request, 'dashboard.html', {
        'total_fleet': total_fleet,
        'pending_count': pending_count,
        'completed_count': completed_count,
        'recent_vehicles': recent_vehicles,
        
        'bar_labels_json': json.dumps(bar_labels),
        'bar_values_json': json.dumps(bar_values),
        'pie_labels_json': json.dumps(pie_labels),
        'pie_values_json': json.dumps(pie_values),
    })



def dash(request):
    return render(request, 'dashboard.html' )


def logooutus(request):
    logout(request)
    return redirect('loginpg')