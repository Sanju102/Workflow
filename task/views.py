from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Task
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect

# Create your views here.
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
