from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

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

def registration(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('registration')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already used")
            return redirect('registration')

        user = User.objects.create_user(username=username,email=email,password=password)
        user.save()

        messages.success(request, "Account created successfully!")
        return redirect('/login')

    return render(request, 'sign-up.html')

def sign_out(request):

    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect("/login") 