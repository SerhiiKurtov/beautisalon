from django.shortcuts import render

from crm.models import Schedule
from crm.models import Service
from crm.models import MasterService

# Create your views here.
def schedule_list(request, service_id, master_id) :
    schedules = Schedule.objects.filter(is_available=True, master_id=master_id)
    return render(request, 'crm/schedule.html', {
        'schedules' : schedules,
        'service_id': service_id
    })

def service_list(request) :
    services = Service.objects.all()
    return render(request, 'crm/service.html', {'services' : services})

def masterservice_list(request, service_id) :
    masters = MasterService.objects.filter(service_id=service_id)
    service = Service.objects.get(id=service_id)
    return render(request, 'crm/masterservice.html', {
        'masters' : masters,
        'service' : service
    })