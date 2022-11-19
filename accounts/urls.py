from django.urls import path
from django.contrib.auth.views import LoginView

from . import views as accounts_views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('signup/', accounts_views.signup, name='signup')
]
