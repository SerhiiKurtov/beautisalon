from django.core.management.base import BaseCommand
from crm.models import Master, Schedule
from datetime import datetime, date
import calendar

class Command(BaseCommand) :
    help = 'Генерує розклад для майстра'

    def add_arguments(self, parser) :
        parser.add_argument('--master_id', type=int, help='ID майстра')
        parser.add_argument('--month', type=int, help='Місяць (1-12)')
        parser.add_argument('--year', type=int, default=2026, help='Рік')
        parser.add_argument('--hour', type=str, nargs='+', help='Години')
        parser.add_argument('--off_day', type=int, nargs='+', help='Вихідні')

    def handle(self, *args, **options) :
        master_id = options['master_id']
        month = options['month']
        year = options['year']
        target_hour = options['hour']
        weekend = options['off_day']

        num_day = calendar.monthrange(year, month)[1]

        try :
            master = Master.objects.get(id=master_id)
        except Master.DoesNotExist :
            self.stdout.write(self.style.ERROR(f"Майстра з ID {master_id} не знайдено!"))
            return
        
        time_day = []
        for t in options['hour'] :
            try :
                valid_time = datetime.strptime(t, "%H:%M").time()
                if valid_time not in time_day :
                    time_day.append(valid_time)
                    self.stdout.write(self.style.SUCCESS(f"Час {valid_time} прийнято."))
            except ValueError :
                self.stdout.write(self.style.ERROR("Помилка! Введіть час у форматі HH:MM (наприклад, 09:00)."))
                return
            
        weekend = options.get('off_day') or []
        for day in range(1, num_day + 1) :
            current_date = date(year, month, day)
            if day in weekend :
                continue
            for h in time_day :
                try :
                    Schedule.objects.get_or_create(master=master, date=current_date, time=h)
                except Exception as e :
                    self.stdout.write(self.style.ERROR(f"Виникла помилка: {e}"))
        
        self.stdout.write(self.style.SUCCESS('Розклад успішно створено!'))