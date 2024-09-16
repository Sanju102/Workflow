from django.shortcuts import render
from task.models import Task
from django.db.models import Q 
from django.utils import timezone
from django.contrib.auth.models import User

def homepage(request):
    if request.user.is_authenticated:
        creator = User.objects.get(username=request.user.username)
        tasks=Task.objects.filter(creator=creator)
        open_task=tasks.filter(Q(status="To do") | Q(status="Ongoing")).count()
        delayed_task=tasks.filter(Q(status="To do") | Q(status="Ongoing"))
        now = timezone.now()
        delayed_task=delayed_task.filter(Q(exp_end_date__lt=now)).count()
        data={"task_summary":{"open_task":open_task,"delayed_task":delayed_task}}
        print(data)
        return render(request, 'index.html',data)
    else:
        return render(request, 'index.html')
