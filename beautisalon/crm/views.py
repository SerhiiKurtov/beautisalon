from django.shortcuts import render
import calendar

from django.http import JsonResponse

from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from datetime import date

from crm.models import Schedule
from crm.models import Service
from crm.models import MasterService
from crm.models import SiteSettings
from crm.models import Advantage
from crm.models import ContactDetail
from crm.models import Gallery
from crm.models import Master
from crm.models import Booking
from crm.models import Client

from crm.forms import BookingEditForm

# Create your views here.
def schedule_list(request, service_id, master_id) :
    schedules = Schedule.objects.filter(is_available=True, master_id=master_id)
    return render(request, 'crm/schedule.html', {
        'schedules' : schedules,
        'service_id': service_id
    })

def service_list(request) :
    services = Service.objects.all()
    return render(request, 'crm/includes/services.html', {'services' : services})

def masterservice_list(request, service_id) :
    masters = MasterService.objects.filter(service_id=service_id)
    service = Service.objects.get(id=service_id)
    return render(request, 'crm/includes/masterservice.html', {
        'masters' : masters,
        'service' : service
    })

def home(request) :
    try:
        month_param = request.GET.get('month')
        year_param = request.GET.get('year')
        
        if month_param and year_param:
            month = int(month_param)
            year = int(year_param)
        else:
            now = timezone.now()
            month = now.month
            year = now.year
    except ValueError:
        now = timezone.now()
        month = now.month
        year = now.year

    first_day_weekday, num_days = calendar.monthrange(year, month)
    range_offset = range(first_day_weekday)
    
    start_date = date(year, month, 1)
    end_date = date(year, month, num_days)

    settings = SiteSettings.objects.first()
    advantages = Advantage.objects.all().order_by('order')
    contacts = ContactDetail.objects.all().order_by('order')
    gallery = Gallery.objects.all().order_by('-date')
    services = Service.objects.all()
    
    all_schedule = Schedule.objects.filter(
        date__range=[start_date, end_date]
    ).order_by('date', 'time')

    if month == 1:
        prev_month, prev_year = 12, year - 1
    else:
        prev_month, prev_year = month - 1, year

    if month == 12:
        next_month, next_year = 1, year + 1
    else:
        next_month, next_year = month + 1, year

    final_calendar_data = []
    for day in range(1, num_days + 1):
        day_slots = [s for s in all_schedule if s.date.day == day]
        final_calendar_data.append({
            'number': day,
            'slots': day_slots
        })

    months_ua = {
        1: "Січень", 2: "Лютий", 3: "Березень", 4: "Квітень",
        5: "Травень", 6: "Червень", 7: "Липень", 8: "Серпень",
        9: "Вересень", 10: "Жовтень", 11: "Листопад", 12: "Грудень"
    }

    current_month_name = months_ua.get(month)

    return render(request, 'crm/index.html', {
        'settings': settings,
        'advantages': advantages,
        'calendar_days': final_calendar_data,
        'range_offset': range_offset,
        'prev_month': prev_month, 
        'prev_year': prev_year,
        'next_month': next_month, 
        'next_year': next_year,
        'current_month': month, 
        'current_year': year,
        'current_month_name': current_month_name,
        'contacts': contacts,
        'gallery': gallery,
        'services': services
    })

def my_calendar(request, year, month) :
    num_day = calendar.monthrange(year, month)[1]
    new = []
    start_date = date(year, month, 1) 
    end_date = date(year, month, num_day)
    records = Schedule.objects.filter(date__range=[start_date, end_date]).order_by('date', 'time')
    for day in range(1, num_day + 1) :
        current_data = f"{year}-{month:02}-{day:02}"
        day_slots = []
        for x in records :
            if x.date.day == day :
                day_slots.append(x)

        new_slots = {'number': day, 'slots': day_slots}
        new.append(new_slots)
    return render(request, 'crm/calendar.html', {'calendar_days': new})