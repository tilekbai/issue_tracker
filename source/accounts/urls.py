from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static
from .views import RegisterView, UserDetailView, UserChangeView, UserPasswordChangeView
from django.contrib.auth.views import LoginView, LogoutView
app_name = 'accounts'


urlpatterns = [
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/create/', RegisterView.as_view(), name='create'),
    path('<int:pk>/user', UserDetailView.as_view(), name='detail'),
    path('change/', UserChangeView.as_view(), name='change'),
    path('password_change/', UserPasswordChangeView.as_view(), name='password_change'),
]
