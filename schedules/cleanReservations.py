from datetime import date, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from books.models import Reservation
from django.conf import settings

def clean():
    old_reservations = Reservation.objects.filter(time__lte=date.today()-timedelta(days=int(settings.RESERVATIONS_DAYS_MAX)))
    old_reservations.delete()

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(clean, 'cron', hour='1', minute='19')
    scheduler.start()