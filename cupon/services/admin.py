from django.contrib import admin
from services.models import Service, EventList

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'coupon_id', 'status', 'qr_img', 'created_at')

class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'date', 'month', 'year')


# Register your models here.
admin.site.register(Service, ServiceAdmin)
admin.site.register(EventList, EventAdmin)

