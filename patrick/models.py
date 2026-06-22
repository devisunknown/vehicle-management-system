from django.db import models

class patrickprofile(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=100)
    last_login = models.DateTimeField(blank=True, null=True)
  
  
# class registerbd(models.Model,ForeignKey=patrickprofile,on_delete=models.CASCADE):
#     id = models.AutoField(primary_key=True)
#     username = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)    
    
    
#     def __repr__(self):
#         return self.id

# Create your models here.


class registedvehicle(models.Model):
    id = models.AutoField(primary_key=True)
    department = models.CharField(max_length=100)
    vehicle_model = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=20, unique=True)
    startdate = models.DateTimeField(auto_now_add=True)
    enddate = models.DateTimeField(blank=True, null=True)
    intialprogress= models.CharField(max_length=100, default='Not Started')
    issue= models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.license_plate