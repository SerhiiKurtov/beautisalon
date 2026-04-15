from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Service
from .models import Client
from .models import Master
from .models import MasterService
from .models import Schedule
from .models import Booking
from .models import SiteSettings
from .models import Advantage
from .models import ContactDetail
from .models import Gallery

admin.site.register(Service)
admin.site.register(Client)
admin.site.register(Master)
admin.site.register(MasterService)
admin.site.register(Booking)
admin.site.register(SiteSettings)
admin.site.register(Advantage)
admin.site.register(ContactDetail)
admin.site.register(Gallery)

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('master', 'date', 'time', 'is_available')
    list_filter = ('master', 'date', 'is_available')
    search_fields = ('master__name',)

admin.site.register(Schedule, ScheduleAdmin)