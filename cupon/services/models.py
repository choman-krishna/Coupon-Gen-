from django.db import models
from django.utils import timezone

class Service(models.Model):
    name = models.CharField(max_length = 20)
    event = models.CharField(max_length = 20)
    coupon_id = models.CharField(primary_key=True, max_length = 20)
    qr_img = models.FileField(upload_to = 'QR/', max_length = 300, null=True, default = None)
    status = models.BooleanField(default = False)
    created_at = models.DateTimeField(default=timezone.now)

# Create your models here.
