from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from api.views import logout
from api.user.views import get_username

urlpatterns = [
    path('username/', get_username, name='username'),
    path('login/', obtain_auth_token, name='login'),
    path('logout/', logout, name='logout'),
]
