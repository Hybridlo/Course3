from datetime import date, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from books.models import Reservation
from users.models import UserInfo
from django.conf import settings

def clean():
    old_reservations = Reservation.objects.filter(time__lte=date.today()-timedelta(days=int(settings.RESERVATIONS_DAYS_MAX)))
    old_reservations.delete()

    if (date.today().month == 9):        #don't clean users in september - give time to reactivate accounts
        return

    last_september = date(date.today().year, 9, 1)

    if date.today().month < 9:
        last_september = last_september.replace(year=last_september.year - 1)

    old_users = UserInfo.objects.filter(last_confirm__lte=last_september)
    for user in old_users:
        if not user.is_staff:
            user.user.is_active = False
            user.user.save()

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(clean, 'cron', hour='23', minute='59')
    scheduler.start()