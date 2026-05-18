from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from enrollment.forms import TeacherForm
from django.db import transaction

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in!")
            return redirect("/")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "sign-in.html")

from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect

def registration(request):
    if request.method == "POST":
        form = TeacherForm(request.POST)

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('registration')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already used")
            return redirect('registration')

        if form.is_valid():
            try:
                with transaction.atomic():

                    # 1. create user
                    user = User.objects.create_user(username=username,email=email,password=password)
                    instructor = form.save(commit=False)
                    instructor.user = user
                    instructor.save()

                    messages.success(request, "Teacher successfully registered")
                    return redirect('/login')

            except Exception as e:
                messages.error(request, f"Error: {str(e)}")

        else:
            messages.error(request, "Please correct the errors below")

    else:
        form = TeacherForm()

    return render(request, 'sign-up.html', {'form': form})

def sign_out(request):

    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect("/login") 