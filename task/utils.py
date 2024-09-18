import logging
from django.utils import timezone
from .models import Task
from notification.models import Notification
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

def check_overdue_tasks():
    logger.info("Starting check_overdue_tasks function")
    current_date = timezone.now()
    overdue_tasks = Task.objects.filter(exp_end_date__lt=current_date, status__in=['To do', 'Ongoing'])
    
    logger.info(f"Found {overdue_tasks.count()} overdue tasks")
    
    for task in overdue_tasks:
        if Notification.objects.filter(des_id=task.id, type='task_delayed').exists():
            pass
        else:
            Notification.objects.create(
            owner=task.creator,
            type="task_delayed",
            status="unseen",
            message="Task "+task.title+" has been delayed",
            des_id=task.id,
            url="task-detail"
        )
    
    logger.info("Finished check_overdue_tasks function")