from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Service
from .models import Client
from .models import Master
from .models import MasterService
from .models import Schedule
from .models import Booking

admin.site.register(Service)
admin.site.register(Client)
admin.site.register(Master)
admin.site.register(MasterService)
admin.site.register(Booking)

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('master', 'date', 'time', 'is_available')
    list_filter = ('master', 'date', 'is_available')
    search_fields = ('master__name',)

admin.site.register(Schedule, ScheduleAdmin)