from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import User
from .forms import UserCreationForm, UserLoginForm, PasswordResetForm, PasswordResetConfirm, PasswordChangeForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required


# Create your views here.

def signup(request):
    if request.method == "POST":
        user_creation_form = UserCreationForm(request.POST)
        if user_creation_form.is_valid():
            user = user_creation_form.save()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'signup.html', context={'form': user_creation_form})
    else:
        user_creation_form = UserCreationForm()
        return render(request, 'signup.html', context={'form': user_creation_form})


def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == "POST":
        user_login_form = UserLoginForm(request.POST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user and user.is_active:
            login(request, user)
            try:
                if request.GET['next']:
                    return redirect(request.GET['next'])
            except Exception as e:
                return redirect('home')
        else:
            messages.error(request, "Please Enter Correct Credential")
            return render(request, 'signin.html', context={'form': user_login_form})
    else:
        user_login_form = UserLoginForm()
        return render(request, 'signin.html', context={'form': user_login_form})


def password_reset_view(request):
    def get_users(mail):
        active_users = User.objects.filter(email__iexact=mail)
        return active_users

    def send_mail(subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()

    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            email = password_reset_form.cleaned_data['email']
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
            extra_email_context = {}
            use_https = False
            subject_template_name = "accounts/password_reset_subject.txt"
            email_template_name = "accounts/password_reset_email.html"
            from_email = "test@gmail.com"
            html_email_template_name = None
            for user in get_users(email):
                context = {
                    'email': email,
                    'domain': domain,
                    'site_name': site_name,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'user': user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'https' if use_https else 'http',
                    **(extra_email_context or {}),

                }
                send_mail(subject_template_name, email_template_name, context, from_email, user.email,
                          html_email_template_name=html_email_template_name,
                          )
            return redirect('password_reset_done')
        else:
            password_reset_form = PasswordResetForm(request.POST)
            # messages.error(request, "Email Field is Mandatory ")
            return render(request, 'password_reset.html', context={'form': password_reset_form})

    else:
        password_reset_form = PasswordResetForm()
        # messages.error(request, "Please Enter the Email ")
        return render(request, 'password_reset.html', context={'form': password_reset_form})


def password_reset_done(request):
    return render(request, 'password_reset_done.html')


def password_reset_confirm(request, uidb64, token):
    INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'
    reset_url_token = 'set-password'
    token_generator = default_token_generator

    def _get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            _user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            _user = None
        return _user

    user = _get_user(uidb64)
    if request.method == "POST":
        password_reset_confirm_form = PasswordResetConfirm(request.POST)
        if password_reset_confirm_form.is_valid():
            user.set_password(password_reset_confirm_form.cleaned_data['password1'])
            user.save()
            return redirect('password_reset_complete')
        else:
            validlink = True
            return render(request, 'password_reset_confirm.html',
                          context={'validlink': validlink, 'form': password_reset_confirm_form, 'user': user})


    else:
        if user:
            if token == reset_url_token:
                session_token = request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if token_generator.check_token(user, session_token):
                    # If the token is valid, display the password reset form.
                    validlink = True
                    password_reset_confirm_form = PasswordResetConfirm()
                    return render(request, 'password_reset_confirm.html',
                                  context={'validlink': validlink, 'form': password_reset_confirm_form, 'user': user})
            else:
                if token_generator.check_token(user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = request.path.replace(token, reset_url_token)
                    return redirect(redirect_url)

    return render(request, 'password_reset_failed.html')


def password_reset_complete(request):
    messages.success(request, "You have successfully changed your password! You may now proceed to log in.")
    return render(request, 'password_reset_complete.html')


@login_required
def change_password(request):
    if request.method == "POST":
        password_change_form = PasswordChangeForm(request.POST)
        if password_change_form.is_valid():
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            email = request.user.email
            user = authenticate(email=email, password=password1)
            if user:
                user.set_password(password2)
                user.save()
                messages.success(request, "Password changed Successfully")
                return redirect('password_change_done')
            else:
                messages.error(request, "Old password is Wrong ! Please Enter correct old password ")
                return render(request, 'password_change.html', context={'form': password_change_form})
        else:
            messages.error(request, "Password and Confirm Password are mandatory Fields")
            return render(request, 'password_change.html', context={'form': password_change_form})

    else:
        password_change_form = PasswordChangeForm()
        return render(request, 'password_change.html', context={'form': password_change_form})


def change_password_done(request):
    return render(request, 'password_change_done.html')
