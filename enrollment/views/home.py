from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from enrollment.models import *
from enrollment.forms import StudentForm
from django.contrib import messages
from django.db import transaction
from datetime import datetime

@login_required(login_url='login') 
def homie(request):
    w = "HELLO"
    return render(request, 'enrollment/dashboard.html')

def enrollment_form(request):
    current_year = datetime.now().year
    year_choices = [
        (f"{year}-{year+1}", f"{year}-{year+1}")
        for year in range(current_year, current_year + 5)
    ]
    if request.method == "POST":
        with transaction.atomic():
            gen_av = request.POST.get('gen_av')
            prev_grade = request.POST.get('prev_grade')
            school_year = request.POST.get('school_year')
            form = StudentForm(request.POST)
            if form.is_valid():
                lrn_no = form.cleaned_data['lrn_no']
                first_name = form.cleaned_data['first_name']
                middle_name = form.cleaned_data['middle_name']
                last_name = form.cleaned_data['last_name']
                ext_name = form.cleaned_data['ext_name']
                date_of_birth = form.cleaned_data['date_of_birth']  # adjust if you have DOB field

                existing_student = Student.objects.filter(
                    lrn_no = lrn_no,
                    first_name=first_name,
                    last_name=last_name,
                    middle_name=middle_name,
                    ext_name=ext_name,
                    date_of_birth=date_of_birth
                ).first()

                if existing_student:
                    sd = existing_student
                    messages.warning(request, "Student already exists. Adding enrollment if needed.")
                else:
                    sd = form.save()
                    if not Enrollment.objects.filter(student=sd, grade=gen_av,prev_grade=prev_grade).exists():
                        enroll = Enrollment(student=sd, prev_grade=prev_grade, grade=gen_av,school_year = school_year)
                        enroll.save()
                    else:
                        messages.warning(request, "Enrollment for this student and grade already exists")
                    messages.success(request, "Student Successfully Added")
                return redirect('enrollment_form')
            else:
                messages.error(request, "Please correct the errors below")
    else:
        form = StudentForm()
    return render(request, 'enrollment_form.html',{'form': form,'year_choices': year_choices})

