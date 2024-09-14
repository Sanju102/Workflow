from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    creator=models.ForeignKey(User,on_delete=models.CASCADE,related_name='task')
    assign_to=models.JSONField()
    created_on=models.DateTimeField(auto_now_add=True)
    completed_on=models.DateTimeField(blank=True,null=True)
    updated_on=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=50)
    priority=models.CharField(max_length=100)
    title=models.CharField(max_length=200)
    description=models.CharField(max_length=1000)
    exp_end_date=models.DateTimeField()
