from django.urls import path
from .views import UserRegistrationView, login_view, UserProfileView

app_name = 'users'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
