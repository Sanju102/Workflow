from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Task
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from django.db.models import Q
from notification.models import Notification

@csrf_protect
def mytask(request):
    if request.user.is_authenticated:
        search_term = request.GET.get('search')
        status = request.GET.get('status')
        priority = request.GET.get('priority')
        only_delayed = request.GET.get('only_delayed')
        creator = User.objects.get(username=request.user.username)
        tasks = Task.objects.filter(creator=creator)
        not_tasks = Task.objects.exclude(status="Completed")
        for task in not_tasks:
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
        if search_term:
                tasks = tasks.filter(Q(title__icontains=search_term) |  Q(description__icontains=search_term))

        if only_delayed:
            # If 'Only Delayed' checkbox is checked, filter only delayed tasks
            tasks = tasks.filter(Q(exp_end_date__lt=timezone.now()))
        # Get the current timezone-aware datetime
        if status:
            tasks=tasks.filter(Q(status=status))
        if priority:
            tasks=tasks.filter(Q(priority=priority))
        now = timezone.now()

        for task in tasks:
            if task.status=="Completed":
                if task.exp_end_date and task.exp_end_date < task.completed_on:
                    task.task_status = 'Delayed'
                    task.task_status_tag="danger"
                else:
                    task.task_status = 'On Time'
                    task.task_status_tag="success"
            else:
                if task.exp_end_date and task.exp_end_date < now:
                    task.task_status = 'Delayed'
                    task.task_status_tag="danger"
                else:
                    task.task_status = 'On Time'
                    task.task_status_tag="success"
            
            # Task priority tag based on the priority level
            if task.priority == 'High':
                task.priority_tag = 'danger'  # Bootstrap danger (red)
            elif task.priority == 'Medium':
                task.priority_tag = 'warning'  # Bootstrap warning (yellow)
            else:
                task.priority_tag = 'primary'  # Bootstrap primary (blue)
        # Render the tasks with the calculated task_status in the template
        notifications=Notification.objects.filter(owner=creator).order_by('-created_on')
        unseen_notification=notifications.filter(Q(status='unseen')).count()
        return render(request, 'mytask.html', {'tasks': tasks,"notification":{"count":unseen_notification,"data":notifications}})

    return redirect('login')

def taskdetails(request, pk):
    if request.user.is_authenticated:
        # Use get_object_or_404 to fetch the task or return a 404 error if it doesn't exist
        task = get_object_or_404(Task, pk=pk)
        now = timezone.now()
        creator = User.objects.get(username=request.user.username)
        tasks = Task.objects.filter(creator=creator)
        notification_task = Task.objects.exclude(status="Completed")
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

        if task.status=="Completed":
            if task.exp_end_date and task.exp_end_date < task.completed_on:
                task.task_status = 'Delayed'
                task.task_status_tag="danger"
            else:
                task.task_status = 'On Time'
                task.task_status_tag="success"
        else:
            if task.exp_end_date and task.exp_end_date < now:
                task.task_status = 'Delayed'
                task.task_status_tag="danger"
            else:
                task.task_status = 'On Time'
                task.task_status_tag="success"
        
        # Task priority tag based on the priority level
        if task.priority == 'High':
            task.priority_tag = 'danger'  # Bootstrap danger (red)
        elif task.priority == 'Medium':
            task.priority_tag = 'warning'  # Bootstrap warning (yellow)
        else:
            task.priority_tag = 'primary'  # Bootstrap primary (blue)
        # Task priority tag based on the priority level
        if task.status == 'Droped':
            task.status_tag = 'danger'  # Bootstrap danger (red)
        elif task.status == 'Ongoing':
            task.status_tag = 'warning'  # Bootstrap warning (yellow)
        elif task.status == 'Completed':
            task.status_tag = 'success'  # Bootstrap warning (yellow)
        else:
            task.status_tag = 'primary'  # Bootstrap primary (blue)
        return render(request, 'taskview.html', {'task': task, "notification":{"count":unseen_notification,"data":notifications}})
    return redirect('login')

@csrf_protect
def task_create(request):
    if request.user.is_authenticated:
        creator = User.objects.get(username=request.user.username)
        tasks = Task.objects.filter(creator=creator)
        notification_task = Task.objects.exclude(status="Completed")
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
        if request.method=='POST':
            creator = User.objects.get(username=request.user.username)
            assign_to = [request.user.username]
            status = request.POST.get('status')  # POST should be uppercase
            priority = request.POST.get('priority')
            title = request.POST.get('title')
            description = request.POST.get('description')
            exp_end_date = request.POST.get('exp_end_date')
            task = Task(
            creator=creator,
            assign_to=assign_to,  # This assumes assign_to is a list field
            status=status,
            priority=priority,
            title=title,
            description=description,
            exp_end_date=exp_end_date
            )
            task.save()
            messages.success(request,"Task has been created !")
            return redirect('homepage')
        
        users = User.objects.all()  # Get all users
        return render(request, 'create_task.html', {'users': users, "notification":{"count":unseen_notification,"data":notifications}})

@csrf_protect   
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('my-task')

@csrf_protect   
def update_task(request, pk):
    if request.user.is_authenticated:
        creator = User.objects.get(username=request.user.username)
        tasks = Task.objects.filter(creator=creator)
        notification_task = Task.objects.exclude(status="Completed")
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
        task = Task.objects.get(pk=pk)
        if request.method=='POST':
            now = timezone.now()
            task.creator = User.objects.get(username=request.user.username)
            task.assign_to = [request.user.username]
            task.status = request.POST.get('status')
            if task.status=='Completed':
                task.completed_on=now
            task.priority = request.POST.get('priority')
            task.title = request.POST.get('title')
            task.description = request.POST.get('description')
            task.exp_end_date = request.POST.get('exp_end_date')
            task.save()
            messages.success(request,"Task updated succcesfully !")
            return redirect('my-task')
        
          # Get all users
        return render(request, 'update_task.html', {'task': task, "notification":{"count":unseen_notification,"data":notifications}})
