from django.urls import path
from django.conf import settings
from .views import home,auth,student,enrollment,teacher,section

urlpatterns = [
    path('', home.homie, name='homie'),
    path('enrollment_form', home.enrollment_form, name='enrollment_form'),


    path('login/', auth.login_view, name='login'),
    path("logout/", auth.sign_out, name="logout"),
    path('registration/', auth.registration, name='registration'),

    path('student_view/', student.student_view, name='student_view'),
    path('<str:s_id>/student_profile/', student.student_profile, name='student_profile'),

    path('enrollment_create/', enrollment.enrollment_create, name='enrollment_create'),
    

    path('teacher_view/', teacher.teacher_view, name='teacher_view'),

    path('section_view/', section.section_view, name='section_view'),
    path('<str:sec_id>/section_student_list/', section.section_student_list, name='section_student_list'),

    path('save_attendance', section.save_attendance, name='save_attendance'),
    path('get_attendance', section.get_attendance, name='get_attendance'),




]