from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login') 
def homie(request):
    w = "HELLO"
    return render(request, 'enrollment/dashboard.html')

