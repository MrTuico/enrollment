from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from enrollment.models import *
from enrollment.forms import StudentForm, EnrollmentForm
from django.contrib import messages
from django.http import JsonResponse
import uuid
from datetime import datetime

@login_required(login_url='login') 
def enrollment_create(request):
    section = Section.objects.all()
    grade_levels = range(1, 13)
    grade_id = request.GET.get('gl')
    sc = request.GET.get('school_year')
    stat = request.GET.get('status')
    sec_id = request.GET.get('sec')
    STATUS_CHOICES = [
        ('enrollee', 'Enrollee'),
        ('enrolled', 'Enrolled'),
        ('dropped', 'Dropped'),
        ('completed', 'Completed'),
    ]
    current_year = datetime.now().year
    
    year_choices = [
        (f"{year}-{year+1}", f"{year}-{year+1}")
        for year in range(current_year - 5, current_year + 6)
    ]
    if not sc:
        sc = f"{current_year}-{current_year+1}"
    # Base queryset
    students_enrollee = Enrollment.objects.filter(school_year=sc)

    # Filter by status if provided
    if stat:
        students_enrollee = students_enrollee.filter(status=stat)

    if stat == "enrollee":
        if grade_id:
            students_enrollee = students_enrollee.filter(prev_grade=grade_id)

    elif stat == "enrolled":
        if sec_id:
            students_enrollee = students_enrollee.filter(section_id=sec_id)
    if not stat:
        students_enrollee = Enrollment.objects.none()

    form = EnrollmentForm()
    if request.method == 'POST':
        if 'enroll_button' in request.POST:
            selected_ids = request.POST.getlist('e_id[]')
            section_id = request.POST.get('gle')
            school_year = request.POST.get('e_school_year')

            if not selected_ids:
                messages.warning(request, "No students selected.")
                return redirect('enrollment_create')

            enrollments = Enrollment.objects.filter(enrollment_id__in=selected_ids)

            updated_count = 0

            for enroll in enrollments:
                enroll.section_id = section_id
                enroll.status = "enrolled"
                enroll.save()
                updated_count += 1

            messages.success(request, f"{updated_count} students enrolled successfully.")
            return redirect('enrollment_create')
        elif 'add_enrollee' in request.POST:
            form = EnrollmentForm(request.POST)
            if form.is_valid():
                student = form.cleaned_data['student']
                grade = form.cleaned_data['grade']
                school_year = form.cleaned_data['school_year']
                if not Enrollment.objects.filter(student = student,grade=grade,school_year = school_year).exists():
                    form.save()
                    messages.success(request, "Student Successfully Enrolled")
                else:
                    messages.warning(request, "Enrollment for this student and grade already exists")
                return redirect('enrollment_create')
            else:
                messages.error(request, "Please correct the errors below")
    return render(request, 'enrollment/student/enrollment.html', {'gl': request.GET.get('gl', ''),'status_choices': STATUS_CHOICES,'form': form,'grade_levels': grade_levels,'students': students_enrollee,'grade_id':grade_id,'year_choices': year_choices, 'current_school_year': sc,'sec':section})


