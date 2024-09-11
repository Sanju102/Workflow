from django.shortcuts import render

def homepage(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return render(request, 'index.html')
