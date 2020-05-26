from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignupForm, LoginForm, UserSettings, UserAddInfo
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from .models import UserInfo
from django.core.mail import EmailMessage
from datetime import date
from books.models import Reservation, Taking

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data.get("email"),
                email=form.cleaned_data.get("email"),
                password=form.cleaned_data.get("password2"),
                first_name=form.cleaned_data.get("first_name"),
                last_name=form.cleaned_data.get("last_name"),
                is_active=False,
            )
            user.save()

            user_info = UserInfo(
                user=user,
                email2=form.cleaned_data.get("email2"),
            )
            user_info.save()

            current_site = get_current_site(request)
            mail_subject = 'Завершіть реєстрацію на сайті бібліотеки факультету.'
            message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()

            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'users/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        user.info.last_confirm = date.today()
        user.info.save()

        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return HttpResponse('Login fail')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

def user_view(request, id):
    user = User.objects.get(pk=id)

    if user == request.user:            #users' own account info
        if request.method == 'POST':
            success = False
            form = UserSettings(request.POST)
            if form.is_valid():
                check_user = authenticate(username=user.username, password=form.cleaned_data['curr_password'])
                if check_user != None and check_user == user:
                    user.first_name = form.cleaned_data['first_name']
                    user.last_name = form.cleaned_data['last_name']
                    user.info.email2 = form.cleaned_data['email2']
                    if form.cleaned_data['password2']:
                        user.set_password(form.cleaned_data['password2'])
                    success = True

                    user.save()
            
                form = UserSettings(initial={
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email2': user.info.email2
                })
            return render(request, 'users/useredit.html', {'form' : form, 'user': user, 'success': success})

        form = UserSettings(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email2': user.info.email2
        })
        return render(request, 'users/useredit.html', {'form': form, 'user': user})

    if request.user.is_authenticated and request.user.info.is_staff:      #for library staff
        if request.method == 'POST':
            success = False

            reserv_id = request.POST.get('reserv_id', None)
            taken_id = request.POST.get('taken_id', None)
            form = UserAddInfo(initial={
                'info': user.info.misc_info
            })
            if reserv_id != None:
                reservation = Reservation.objects.get(pk=reserv_id)
                taking = Taking()
                taking.taken_by = reservation.reserved_by
                taking.book = reservation.book
                taking.save()
                reservation.delete()
                success = True
            
            elif taken_id != None:
                taking = Taking.objects.get(pk=taken_id)
                taking.book.copies_available += 1
                taking.book.save()
                taking.delete()
                success = True

            else:
                form = UserAddInfo(request.POST)
                if form.is_valid():
                    user.info.misc_info = form.cleaned_data['info']
                    user.info.save()
                    success = True
            return render(request, 'users/user.html', {'form': form, 'user': user, 'success': success})
        else:
            form = UserAddInfo(initial={
                'info': user.info.misc_info
            })
            return render(request, 'users/user.html', {'form': form, 'user': user})

    return render(request, 'users/user.html', {'user': user})