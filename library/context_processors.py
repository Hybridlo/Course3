from django.contrib.auth.forms import AuthenticationForm

def auth_form(request):
    if request.user.is_authenticated:
        return { 'curr_user' : request.user }
    return { 'curr_user' : None }