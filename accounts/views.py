from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import UserCreationForm, UserUpdateForm


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


def settings(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been updated.')
            return redirect('home')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'accounts/settings.html', {'form': form})
