from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignupForm, LoginForm, UserSettings, UserAddInfo, ForgotPassword, ResetPassword, StaffSignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import User
from .models import UserInfo, StaffToken
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

            return render(request, 'message.html', {'message': 'На студентську пошту надісланий лист з посланням на підтвердження реєстрації'})
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
        return render(request, 'message.html', {'message': 'Пошта підтверджена'})
    else:
        return render(request, 'message.html', {'message': 'Посилання не дійсне'})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'message.html', {'message': 'Під час входу сталася помилка'})
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
                    user.info.hide_email2 = form.cleaned_data['hide_email2']
                    if form.cleaned_data['password2']:
                        user.set_password(form.cleaned_data['password2'])
                    success = True

                    user.save()
                    user.info.save()
            
                form = UserSettings(initial={
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email2': user.info.email2,
                    'hide_email2': user.info.hide_email2,
                })
            return render(request, 'users/useredit.html', {'form' : form, 'user': user, 'success': success})

        form = UserSettings(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email2': user.info.email2,
            'hide_email2': user.info.hide_email2,
        })
        return render(request, 'users/useredit.html', {'form': form, 'user': user})

    if request.user.is_authenticated and request.user.info.is_staff:      #for library staff
        if request.method == 'POST':
            success = False

            reserv_id = request.POST.get('reserv_id', None)
            taken_id = request.POST.get('taken_id', None)
            form = UserAddInfo(initial={
                'info': user.info.misc_info,
                'is_active': user.is_active,
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
                    if not user.is_active and form.cleaned_data['is_active']:
                        user.is_active = True
                        user.save()
                    success = True
            return render(request, 'users/user.html', {'form': form, 'user': user, 'success': success})
        else:
            form = UserAddInfo(initial={
                'info': user.info.misc_info,
                'is_active': user.is_active,
            })
            return render(request, 'users/user.html', {'form': form, 'user': user})

    return render(request, 'users/user.html', {'user': user})

def reactivation(request):
    last_september = date(date.today().year, 9, 1)

    if date.today().month < 9:
        last_september = last_september.replace(year=last_september.year - 1)

    if not request.user.is_authenticated or request.user.info.is_staff or not request.user.info.last_confirm <= last_september:
        return render(request, 'message.html', {'message': 'Ця дія недоступна'})

    current_site = get_current_site(request)
    mail_subject = 'Підтвердіть активність пошти.'
    message = render_to_string('users/acc_active_email.html', {
        'user': request.user,
        'domain': current_site.domain,
        'uid':urlsafe_base64_encode(force_bytes(request.user.pk)),
        'token':account_activation_token.make_token(request.user),
    })
    to_email = request.user.email
    email = EmailMessage(
                mail_subject, message, to=[to_email]
    )
    email.send()

    return render(request, 'message.html', {'message': 'Лист надісланий на студентську пошту'})

def forgot_password(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = ForgotPassword(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            found = User.objects.filter(email=email)
            success = False

            if not found.exists():
                found = UserInfo.objects.filter(email2=email)

                if not found.exists():
                    found = None

                else:
                    user = found[0].user

            else:
                user = found[0]

            if found != None:
                success = True
                current_site = get_current_site(request)
                mail_subject = 'Відновлення пароля.'
                message = render_to_string('users/pass_reset_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':PasswordResetTokenGenerator().make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                email.send()

        return render(request, 'users/forgot.html', {'form': form, 'success': success})
    else:
        form = ForgotPassword()
        return render(request, 'users/forgot.html', {'form': form})

def pass_reset(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if not request.user.is_authenticated and user and user.is_active is not None and PasswordResetTokenGenerator().check_token(user, token):
        form = ResetPassword()
        if request.method == 'POST':
            form = ResetPassword(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data['password2'])
                user.save()

        return render(request, 'users/reset_pass.html', {'form': form})
    else:
        return render(request, 'message.html', {'message': 'Посилання не дійсне'})

def staff_signup(request):
    if request.method == 'POST':
        form = StaffSignupForm(request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data.get("email"),
                email=form.cleaned_data.get("email"),
                password=form.cleaned_data.get("password2"),
                first_name=form.cleaned_data.get("first_name"),
                last_name=form.cleaned_data.get("last_name"),
                is_active=True,
            )
            user.save()

            user_info = UserInfo(
                user=user,
                is_staff=True
            )
            user_info.save()

            return render(request, 'message.html', {'message': 'Успішно'})
    else:
        form = StaffSignupForm()
    return render(request, 'users/signup.html', {'form': form})

def create_staff_token(request):
    if not request.user.info.is_staff:
        return redirect('index')

    token = StaffToken()
    token.generate()
    return render(request, 'message.html', {'message': 'Токен:' + token.token})