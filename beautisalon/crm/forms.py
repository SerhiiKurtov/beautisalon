from django import forms
from django.db import models
from .models import Booking

class ScheduleGenerationForm(forms.Form) :
    year = forms.IntegerField(label="Рік", initial=2026)
    month = forms.IntegerField(label="Місяць (1-12)", min_value=1, max_value=12)
    hours = forms.CharField(
        label="Введіть робочі години (через пробіл)",
        help_text="Наприклад: 09:00 12:00 15:00",
        widget=forms.TextInput(attrs={'placeholder': '09:00 12:00...'})
    )
    weekends = forms.CharField(
        label="Вихідні (числа місяця через пробіл)",
        required=False,
        help_text="Наприклад: 5 6 12 13"
    )

class BookingEditForm(forms.ModelForm) :
    new_client_name = forms.CharField(required=False, label="Ім'я нового клієнта", max_length=100)
    new_phone = forms.CharField(required=False, label="Номер телефону", max_length=13)  

    class Meta:
        model = Booking
        fields = ['status', 'client', 'schedule', 'service', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].required = False