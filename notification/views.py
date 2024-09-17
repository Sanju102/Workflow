from django.shortcuts import render,redirect
from .models import Notification

# Create your views here.

def check_notification(request,pk):
    notification=Notification.objects.get(pk=pk)
    notpk=notification.des_id
    notification.status="seen"
    notification.save()
    return redirect('task-detail', pk=notpk)

