from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from enrollment.models import *
from enrollment.forms import SectionForm,EnrollmentForm
from django.contrib import messages
import uuid
from datetime import datetime

@login_required(login_url='login') 
def section_view(request):
    sec = Section.objects.all()
    if request.method == "POST":
        form = SectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student Successfully Added")
            return redirect('sectionview')
        else:
            messages.error(request, "Please correct the errors below")
    else:
        form = SectionForm()
    return render(request, "enrollment/student/section.html", {'form': form,'sec': sec})

@login_required(login_url='login') 
def section_student_list(request,sec_id):
    current_year = datetime.now().year
    sc =  f"{current_year}-{current_year+1}"
    students = Enrollment.objects.filter(section=sec_id,school_year=sc,status='enrolled').order_by('student__last_name')
    current_year = datetime.now().year
    
  
    return render(request, 'enrollment/student/section_student_list.html',{'students':students})


