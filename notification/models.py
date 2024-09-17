from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from task.models import Task
# Notification model
class Notification(models.Model):
    STATUS_CHOICES = [
        ('seen', 'Seen'),
        ('unseen', 'Unseen')
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    created_on = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=30)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='unseen')
    message = models.CharField(max_length=100)
    url=models.CharField(max_length=50,blank=True,null=True)
    des_id=models.IntegerField(blank=True,null=True)

    def __str__(self):
        return f"Notification for {self.owner.username}: {self.message}"
