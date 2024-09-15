from django.urls import path
from .views import task_create,mytask,taskdetails,delete_task

urlpatterns = [
    path('create/', task_create, name='task-create'),
    path('mytask/', mytask, name='my-task'),
    path('<int:pk>/', taskdetails, name='task-detail'),
    path('<int:pk>/delete/', delete_task, name='delete-task'),
]