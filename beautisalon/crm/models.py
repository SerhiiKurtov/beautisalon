from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Service(models.Model) :
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) :
        return f"{self.title} ({self.price})"

class Client(models.Model) :
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)

    def __str__(self) :
        return self.name
    
class Master(models.Model) :
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) :
        return f"{self.name} ({self.specialization})"
    
class MasterService(models.Model) :
    master = models.ForeignKey(Master, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) :
        return f"{self.master} ({self.service} - {self.price})"

class Schedule(models.Model) :
    date = models.DateField()
    time = models.TimeField()
    is_available = models.BooleanField(default=True)
    master = models.ForeignKey(Master, on_delete=models.CASCADE)

    class Meta :
        unique_together = ('date', 'time', 'master')

    def __str__(self) :
        return f"{self.date} {self.time} - {self.master.name}"

class Booking(models.Model) :
    STATUS_CHOICES = [
        ('pending', 'Очікується'),
        ('confirmed', 'Підтверджено'),
        ('completed', 'Виконано'),
        ('canceled', 'Скасовано'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ForeignKey(MasterService, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)

    def __str__(self) :
        return f"{self.client} - {self.schedule}"