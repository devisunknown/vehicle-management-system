from django.urls import path
from . import views


urlpatterns = [
    path('', views.loginpg, name='loginpg'),
    path('login/', views.scancoatadmin, name='scancoatadmin'),
    path('patrickprof/', views.patrickprof, name='patrickprof'),
    path('register/', views.register, name='register'),
   path('vehicle_list/', views.vehicle_list, name='vehicle_list'),
   path('vehicleview/', views.vehicleview, name='vehicleview'),
   path('dashboard/', views.dashboard, name='dashboard'),
   path('delete_vehicle/<str:vehicle_order_number>/', views.delete_vehicle, name='delete_vehicle'),
   path('data/', views.data, name='data'),
   path('logout/', views.logooutus, name='logout'),
   path('complete/<str:vehicle_order_number>/', views.complete_vehicle, name='complete_vehicle'),
   path('vehicle/complete/<str:vehicle_order_number>/', views.complete_vehicle, name='complete_vehicle'),
   path('vehicle/upload-excel/', views.upload_excel, name='upload_excel'),
   path('vehicle/paid/<str:vehicle_order_number>/', views.paid, name='paid'),
]
