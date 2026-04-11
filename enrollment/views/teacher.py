from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from enrollment.models import *
from enrollment.forms import TeacherForm
from django.contrib import messages

@login_required(login_url='login') 
def teacher_view(request):
    teacher = Instructor.objects.all().order_by('-last_name')
    if request.method == "POST":
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Teacher Successfully Added")
            return redirect('teacher_view')
        else:
            messages.error(request, "Please correct the errors below")
    else:
        form = TeacherForm()
    return render(request, "enrollment/instructor/teacher.html", {'form': form,'ins': teacher})