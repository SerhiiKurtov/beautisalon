from django.shortcuts import render

from django.http import JsonResponse

from django.utils import timezone
from datetime import timedelta

from crm.models import Schedule
from crm.models import Service
from crm.models import MasterService
from crm.models import SiteSettings
from crm.models import Advantage
from crm.models import ContactDetail
from crm.models import Gallery
from crm.models import Master

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
    today = timezone.now().date()
    end_date = today + timedelta(days=5)
    settings = SiteSettings.objects.first()
    advantages = Advantage.objects.all().order_by('order')
    contacts = ContactDetail.objects.all().order_by('order')
    gallery = Gallery.objects.all().order_by('-date')
    services = Service.objects.all()
    schedule = Schedule.objects.filter(date__range=[today, end_date], is_available=True).order_by('date', 'time')
    master_list = []
    master = Master.objects.all()
    for m in master :
        m_schedule = Schedule.objects.filter(
            master=m,
            date__range=[today, end_date],
            is_available=True
        ).order_by('date', 'time')
        master_list.append({
            'master' : m,
            'slots' : m_schedule
        })
    return render(request, 'crm/index.html', {
        'settings' : settings,
        'advantages' : advantages,
        'contacts' : contacts,
        'gallery' : gallery,
        'services' : services,
        'master_list' : master_list 
    })

def load_schedule(request, master_id) :
    events = []
    schedule = Schedule.objects.filter(master_id=master_id, is_available=True).order_by('date', 'time')
    for s in schedule :
        event_data = {
            'id' : s.id,
            'title' : f"Вільний час ({s.master.name})",
            'start': f"{s.date}T{s.time}",
        }
        events.append(event_data)
    return JsonResponse(events, safe=False)