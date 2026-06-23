from django.db import models

class patrickprofile(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    last_login = models.DateTimeField(blank=True, null=True)


class registedvehicle(models.Model):
    order_number = models.CharField(primary_key=True, max_length=10, default='0000000000', null=False, unique=True)
    department = models.CharField(max_length=100)
    vehicle_model = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=20, unique=True)
    startdate = models.DateTimeField(auto_now_add=True)
    enddate = models.DateTimeField(blank=True, null=True)
    intialprogress = models.CharField(max_length=100, default='Not Started')
    issue = models.TextField(blank=True, null=True)
    equip_number = models.PositiveIntegerField(blank=True, null=True)
    equip_id = models.CharField(max_length=100, blank=True, editable=False)
    enddate = models.DateTimeField(null=True, blank=True)

    DEPARTMENT_ACRONYMS = {
        'Security': 'SYD',
        'Maintenance': 'MNT',
        # 'Human Resources': 'HRD',
    }

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['department', 'equip_number'], name='unique_equip_per_department')
        ]

    def save(self, *args, **kwargs):
        if self.equip_number:
            acronym = self.DEPARTMENT_ACRONYMS.get(self.department.title(), self.department[:3].upper())
            self.equip_id = f"{acronym} {self.equip_number}"
        super().save(*args, **kwargs)

    @property
    def formatted_plate(self):
        plate = self.license_plate.upper().replace(' ', '').replace('-', '')
        if len(plate) >= 8:
            region = plate[:2]
            middle = plate[2:6]
            year = plate[6:8]
            return f"{region}-{middle}-{year}"
        return self.license_plate.upper()

    def __str__(self):
        return self.license_plate