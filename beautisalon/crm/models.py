from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Service(models.Model) :
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Послуги"
        verbose_name_plural = "Послуги"

    def __str__(self) :
        return f"{self.title} ({self.price})"

class Client(models.Model) :
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)

    class Meta:
        verbose_name = "Клієнти"
        verbose_name_plural = "Клієнти"

    def __str__(self) :
        return self.name
    
class Master(models.Model) :
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Майстри"
        verbose_name_plural = "Майстри"

    def __str__(self) :
        return f"{self.name} ({self.specialization})"
    
class MasterService(models.Model) :
    master = models.ForeignKey(Master, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Майстер-послуги"
        verbose_name_plural = "Майстер-послуги"

    def __str__(self) :
        return f"{self.master} ({self.service} - {self.price})"

class Schedule(models.Model) :
    date = models.DateField()
    time = models.TimeField()
    is_available = models.BooleanField(default=True)
    master = models.ForeignKey(Master, on_delete=models.CASCADE)

    class Meta :
        unique_together = ('date', 'time', 'master')
        verbose_name = "Розклад"
        verbose_name_plural = "Розклад"

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
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Бронювання"
        verbose_name_plural = "Бронювання"

    def save(self, *args, **kwargs) :
        if not self.total_price :
            self.total_price = self.service.price
        if self.status in ['pending', 'confirmed'] :
            self.schedule.is_available = False
            self.schedule.save()
        elif self.status == 'canceled' :
            self.schedule.is_available = True
            self.schedule.save()
        super().save(*args, **kwargs)

    def __str__(self) :
        return f"{self.client} - {self.schedule}"
    
class SiteSettings(models.Model) :
    site_name = models.CharField(max_length=100, default='Irenka Nails')
    bg_color = models.CharField(max_length=7, default='#E6E6FA')
    container_color = models.CharField(max_length=7, default='#FFFFFF')
    hero_title = models.CharField(max_length=300, default='Твій ідеальний манікюр')
    hero_subtitle = models.TextField(blank=True)
    emblem = models.ImageField(upload_to='logos', null=True, blank=True)

    class Meta:
        verbose_name = "Налаштування сайту"
        verbose_name_plural = "Налаштування сайту"
    
    def __str__(self):
        return "Налаштування сайту"
    
class Advantage(models.Model) :
    title = models.CharField(max_length=100, unique=True, default='Якість')
    description = models.TextField(max_length=500, default='Працюємо на найкращих та перевірених матеріалах')
    order = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Переваги"
        verbose_name_plural = "Переваги"

    def __str__(self) :
        return self.title
    
class ContactDetail(models.Model) :
    name = models.CharField(max_length=50, blank=True)
    badge = models.CharField(max_length=100)
    contact = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Контактна інформація"
        verbose_name_plural = "Контактна інформація"

    def __str__(self):
        return self.name or self.contact
    
class Gallery(models.Model) :
    image = models.ImageField(upload_to='gallery', null=True, blank=True)
    name = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Галерея"
        verbose_name_plural = "Галерея"

    def __str__(self):
        return self.name or "Фото роботи"