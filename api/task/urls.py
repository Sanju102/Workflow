from django.urls import path
from .views import task_summary

urlpatterns = [
    path('task_summary/', task_summary, name='task_summary'),
]   