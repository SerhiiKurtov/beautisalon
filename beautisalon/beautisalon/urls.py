"""
URL configuration for beautisalon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from crm.views import schedule_list, service_list, masterservice_list, home
from django.conf import settings
from django.conf.urls.static import static
from crm import views

urlpatterns = [
    path('', home, name='home'),
    path('schedule/', schedule_list, name='schedule_list'),
    path('service/', service_list, name='service_list'),
    path('service/<int:service_id>/masters/', masterservice_list, name='masterservice_list'),
    path('schedule/<int:service_id>/<int:master_id>/', schedule_list, name='schedule_list'),
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('api/calendar-data/', views.schedule_date, name='schedule_data'),
    path('api/load_schedule/<int:master_id>/', views.load_schedule, name='load_schedule'),
    path('admin/', admin.site.urls),
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
