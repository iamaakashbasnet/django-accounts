from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views as accounts_views

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', accounts_views.signup, name='signup'),
    path('settings/', accounts_views.settings, name='settings'),
]
