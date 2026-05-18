from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from enrollment.models import *
from enrollment.forms import SectionForm,EnrollmentForm
from django.contrib import messages
import uuid
from datetime import datetime, date
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@login_required(login_url='login') 
def section_view(request):
    sec = Section.objects.all()
    if request.method == "POST":
        form = SectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student Successfully Added")
            return redirect('section_view')
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
    students_data = [
        {
            "id": i.student.student_id,
            "last_name": i.student.last_name,
            "first_name": i.student.first_name,
            "gender": i.student.gender,
            "age": i.student.age,
            "grade_no": i.section.grade_level.grade_no,
            "section_name": i.section.section_name,
        }
        for i in students
    ]
    
  
    return render(request, 'enrollment/student/section_student_list.html',{'students':students,"students_data": students_data})


@login_required(login_url='login')
def save_attendance(request):
    if request.method == "POST":
        data = json.loads(request.body)

        student_id = data.get("student_id")
        section_id = data.get("section_id")
        am_status = data.get("am_status")
        pm_status = data.get("pm_status")

        Attendance.objects.update_or_create(
            student_id=student_id,
            section_id=section_id,
            date=date.today(),
            defaults={
                "am_status": am_status,
                "pm_status": pm_status,
            }
        )

        return JsonResponse({"status": "success"})

@login_required(login_url='login')
def get_attendance(request):
    section_id = request.GET.get("section_id")

    records = Attendance.objects.filter(
        section_id=section_id,
        date=date.today()
    )

    data = {
        r.student_id: {
            "am": r.am_status,
            "pm": r.pm_status
        }
        for r in records
    }

    return JsonResponse(data)