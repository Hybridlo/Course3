from django.contrib.auth.forms import AuthenticationForm
from datetime import date, timedelta

def auth_form(request):
    warning = None

    curr_user = None
    if request.user.is_authenticated:
        curr_user = request.user

    last_september = date(date.today().year, 9, 1)

    if date.today().month < 9:
        last_september = last_september.replace(year=last_september.year - 1)

    if curr_user and not curr_user.info.is_staff and curr_user.info.last_confirm <= last_september:
        warning = 'Будь ласка, підтвердіть що ваша студентська пошта активна цього року, інакше цей акаунт стане неактивним в жовтні'
    return { 'curr_user' : curr_user, 'warning' : warning }