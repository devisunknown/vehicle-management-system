from django.contrib import admin
from .models import patrickprofile,registedvehicle

class patrickprofileAdmin(admin.ModelAdmin):
    list_filter = ('username',)
    search_fields = ('username',)
    
admin.site.register(patrickprofile, patrickprofileAdmin)
admin.site.register(registedvehicle)

# Register your models here.
