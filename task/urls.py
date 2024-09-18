from django.urls import path
from .views import task_create, mytask, taskdetails, delete_task, update_task, save_notes

urlpatterns = [
    path('create/', task_create, name='task-create'),
    path('mytask/', mytask, name='my-task'),
    path('<int:pk>/', taskdetails, name='task-detail'),
    path('<int:pk>/delete/', delete_task, name='delete-task'),
    path('<int:pk>/update/', update_task, name='update-task'),
    path('save-notes/<int:task_id>/', save_notes, name='save-notes'),  # Add this line
]