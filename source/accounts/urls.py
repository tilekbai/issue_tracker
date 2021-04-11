from django.urls import path, include 
# from .views import login_view, logout_view
from django.contrib.auth.views import LoginView, LogoutView
app_name = 'accounts'


urlpatterns = [
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),

]
