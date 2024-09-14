from django.urls import path
from .views import task_create,mytask

urlpatterns = [
    path('create/', task_create, name='task-create'),
    path('mytask/', mytask, name='my-task'),
]