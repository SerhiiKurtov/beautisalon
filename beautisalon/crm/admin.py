import calendar
from datetime import datetime
from django.db import models
from django.forms import TextInput

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
from .forms import ScheduleGenerationForm
from django.shortcuts import render, HttpResponseRedirect

admin.site.register(Service)
admin.site.register(Client)
admin.site.register(MasterService)
admin.site.register(Booking)
admin.site.register(Advantage)
admin.site.register(ContactDetail)
admin.site.register(Gallery)

class ScheduleAdmin(admin.ModelAdmin) :
    change_list_template = 'admin/crm/schedule/change_list.html'
    list_display = ('master', 'date', 'time', 'display_client', 'is_available')
    list_filter = ('master', 'date', 'is_available')
    search_fields = ('master__name',)

    def display_client(self, obj) :
        booking = obj.booking_set.first()
        if booking :
            client = booking.client.name
            service = booking.service.service.title
            return f"{client} ({service})"
        else :
            return "-"
        
    display_client.short_description = 'Клієнт'

admin.site.register(Schedule, ScheduleAdmin)

def generate_schedule(modeladmin, request, queryset) :
    if 'apply' in request.POST :
        form = ScheduleGenerationForm(request.POST)
        if form.is_valid() :
            year = form.cleaned_data['year']
            month = form.cleaned_data['month']
            num_day = calendar.monthrange(year, month)[1]
            weekends_list = form.cleaned_data['weekends'].split()
            hours_list = form.cleaned_data['hours'].split()

            for master in queryset :
                for day in range(1, num_day + 1) :
                    if str(day) in weekends_list:
                        continue

                    current_date = f"{year}-{month:02}-{day:02}"

                    for h in hours_list :
                        Schedule.objects.get_or_create(master=master, date=current_date, time=h)

            modeladmin.message_user(request, "Графік створено")
            return HttpResponseRedirect(request.get_full_path())
    else :
        form = ScheduleGenerationForm()
    
    return render(request, 'admin/generate_schedule.html', {
        'queryset': queryset,
        'form': form
    })

generate_schedule.short_description = "Згенерувати графік на місяць"

class MasterAdmin(admin.ModelAdmin) :
    actions = [generate_schedule]

admin.site.register(Master, MasterAdmin)

class Settings(admin.ModelAdmin) :
    def formfield_for_dbfield(self, db_field, **kwargs) :
        if db_field.name in ['bg_color', 'container_color'] :
            kwargs['widget'] = TextInput(attrs={'type': 'color'})

        return super().formfield_for_dbfield(db_field, **kwargs)

admin.site.register(SiteSettings, Settings)