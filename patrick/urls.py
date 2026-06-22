from django.urls import path
from . import views


urlpatterns = [
    path('', views.loginpg, name='loginpg'),
    path('login', views.login, name='login'),
    path('patrickprof', views.patrickprof, name='patrickprof'),
    path('register', views.register, name='register'),
   path('vehicle_list', views.vehicle_list, name='vehicle_list'),
   path('vehicleview', views.vehicleview, name='vehicleview'),
   path('dashboard', views.dashboard, name='dashboard'),
]
