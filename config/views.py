from django.shortcuts import render
from task.models import Task
from django.db.models import Q 
from django.utils import timezone
from django.contrib.auth.models import User
from notification.models import Notification

def homepage(request):
    if request.user.is_authenticated:
        creator = User.objects.get(username=request.user.username)
        tasks=Task.objects.filter(creator=creator)
        notification_task=tasks.exclude(status='Completed')
        for task in notification_task:
            if Notification.objects.filter(des_id=task.id, type='task_delayed').exists():
                pass
            else:
                Notification.objects.create(
                    owner=task.creator,
                    type="task_delayed",
                    status="unseen",
                    message="Task "+task.title+" has been delayed.",
                    des_id=task.id,
                    url="task-detail"
                )
        notifications=Notification.objects.filter(owner=creator).order_by('-created_on')
        unseen_notification=notifications.filter(Q(status='unseen')).count()
        open_task=tasks.filter(Q(status="To do") | Q(status="Ongoing")).count()
        delayed_task=tasks.filter(Q(status="To do") | Q(status="Ongoing"))
        now = timezone.now()
        delayed_task=delayed_task.filter(Q(exp_end_date__lt=now)).count()
        data={"task_summary":{"open_task":open_task,"delayed_task":delayed_task},"notification":{"count":unseen_notification,"data":notifications}}
        return render(request, 'index.html',data)
    else:
        return render(request, 'index.html')
