from django import forms

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