from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Task
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone

@csrf_protect
def mytask(request):
    if request.user.is_authenticated:
        creator = User.objects.get(username=request.user.username)
        tasks = Task.objects.filter(creator=creator)

        # Get the current timezone-aware datetime
        now = timezone.now()

        for task in tasks:
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
        return render(request, 'mytask.html', {'tasks': tasks})

    return redirect('login')

@csrf_protect
def task_create(request):
    if request.user.is_authenticated:
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
        return render(request, 'create_task.html', {'users': users})
