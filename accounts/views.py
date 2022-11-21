from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
# from django.core.exceptions import ObjectDoesNotExist

from .forms import (
    UserCreationForm,
    UserUpdateForm,
    ConfirmPasswordForm,
)
from .utils.token import account_activation_token


User = get_user_model()


@login_required()
def home(request):
    return render(request, 'accounts/dashboard/home.html', {})


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)

            if form.is_valid():
                user = form.save(commit=False)
                user.save()

                current_site = get_current_site(request)
                mail_subject = 'Activation link has been sent to your email address.'
                message = render_to_string('accounts/email_template/account_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user)
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()

                messages.success(
                    request, 'Account created! Email has been sent, please verify your account.')
                return redirect('login')
        else:
            form = UserCreationForm()

        return render(request, 'accounts/signup.html', {'form': form})


@login_required
def settings(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        pass_form = PasswordChangeForm(user=request.user, data=request.POST)

        # Other fields
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been updated.')
            return redirect('home')

        # Password fields
        if pass_form.is_valid():
            user = pass_form.save(commit=True)
            # Logs out user from all session
            update_session_auth_hash(request, user)
            messages.success(request, 'Password updated successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')

    else:
        form = UserUpdateForm(instance=request.user)
        pass_form = PasswordChangeForm(request.user)

    return render(request, 'accounts/settings.html', {'form': form, 'pass_form': pass_form})


@login_required
def delete_account(request):
    if request.method == 'POST':
        form = ConfirmPasswordForm(request.POST, request=request)

        if form.is_valid():
            try:
                _user = get_object_or_404(
                    get_user_model(), username=request.user.username)
                _user.delete()
                messages.success(request, 'User successfully deleted!')
                return redirect('login')
            except:
                messages.error(request, 'Something went wrong!')
                return redirect('settings')

    else:
        form = ConfirmPasswordForm(request=request)
    return render(request, 'accounts/delete_account_confirm.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, 'Account has been verified! Now you can login.')
    else:
        messages.error(request, 'Activation link is invalid.')

    return redirect('login')
