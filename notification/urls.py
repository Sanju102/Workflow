from django.urls import path
from .views import check_notification

urlpatterns = [
    path('check/<int:pk>/', check_notification, name='check-notification')
]