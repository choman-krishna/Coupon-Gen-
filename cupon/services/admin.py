from django.contrib import admin
from services.models import Service, EventList, ScannedData

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'coupon_id', 'status', 'qr_img', 'created_at')

class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'date', 'month', 'year')

class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'date', 'month', 'year')

class ScannedDataAdmin(admin.ModelAdmin):
    list_display = ('username', 'scanned_otp', 'scanned_time')

# Register your models here.
admin.site.register(Service, ServiceAdmin)
admin.site.register(EventList, EventAdmin)
admin.site.register(ScannedData, ScannedDataAdmin)
