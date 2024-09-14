from django.urls import path
from .views import task_create

urlpatterns = [
    path('create/', task_create, name='task-create'),
    # path('logout/', logout_user, name='logout-user'),
    # path('register/', register_user, name='user-register'),
]