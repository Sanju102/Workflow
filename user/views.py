from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages

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

        