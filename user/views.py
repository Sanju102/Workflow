from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def login_user(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('homepage')
        else:
            return redirect('homepage')

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'You have successfully logged out.')
        return redirect('homepage')
    else:
        return redirect('homepage')
    
def register_user(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    else:
        if request.method=='POST':
            username = request.POST["username"]
            password = request.POST["password"]
            email=request.POST["email"]
            first_name=request.POST["first_name"]
            last_name=request.POST["last_name"]
            if User.objects.filter(username=username).exists():
                messages.warning(request, 'Username already exists')
                render(request,'register.html')
            elif User.objects.filter(email=email).exists():
                messages.warning(request, 'Email already exists')
                render(request,'register.html')
            else:
                user = User.objects.create_user(username, email, password)
                user.first_name = first_name
                user.last_name = last_name
                user = authenticate(request, username=username, password=password)
                login(request,user)
                messages.success(request, 'You have successfully logged in.')
                return redirect('homepage')
        return render(request,'register.html')

        