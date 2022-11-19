from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import UserCreationForm


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
