from django.urls import path
from .views import login_user,logout_user,register_user

urlpatterns = [
    path('login/', login_user, name='login-user'),
    path('logout/', logout_user, name='logout-user'),
    path('register/', register_user, name='user-register'),
]