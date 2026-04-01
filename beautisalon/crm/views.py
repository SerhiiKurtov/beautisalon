from django.shortcuts import render

from crm.models import Schedule

# Create your views here.
def schedule_list(request) :
    schedules = Schedule.objects.filter(is_available=True)
    return render(request, 'crm/schedule.html', {'schedules' : schedules})