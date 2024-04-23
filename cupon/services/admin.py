from django.contrib import admin
from services.models import Service

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'coupon_id', 'status', 'qr_img', 'created_at')

# Register your models here.
admin.site.register(Service, ServiceAdmin)
