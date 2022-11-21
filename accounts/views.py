from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .forms import (
    UserCreationForm,
    UserUpdateForm,
    ConfirmPasswordForm,
)


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
                form.save()
                messages.success(
                    request, 'Account created! Now you can login.')
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
