from django.db import models
from django.utils import timezone

class Service(models.Model):
    name = models.CharField(max_length = 20)
    event = models.CharField(max_length = 20)
    coupon_id = models.CharField(primary_key=True, max_length = 20)
    qr_img = models.FileField(upload_to = 'QR/', max_length = 300, null=True, default = None)
    status = models.BooleanField(default = False)
    created_at = models.DateTimeField(default=timezone.now)

class EventList (models.Model):
    event_name = models.CharField(max_length=20)
    date = models.CharField(max_length=2)
    month = models.CharField(max_length=10, default='May')
    year = models.CharField(max_length=4, default='2024')

class ScannedData(models.Model):
    username = models.CharField(max_length=20)
    scanned_otp = models.CharField(max_length = 20)    
    scanned_time = models.DateTimeField(default=timezone.now)
    otp_status = models.CharField(max_length=20)

class GenScanStatus(models.Model):
    name = models.CharField(max_length = 10)
    status = models.BooleanField(default = True)
    


# Create your models here.
