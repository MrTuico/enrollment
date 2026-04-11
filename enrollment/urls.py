from django.urls import path
from django.conf import settings
from .views import home,auth,student,enrollment,teacher,section

urlpatterns = [
    path('', home.homie, name='homie'),
    path('login/', auth.login_view, name='login'),
    path("logout/", auth.sign_out, name="logout"),
    path('registration/', auth.registration, name='registration'),

    path('student_view/', student.student_view, name='student_view'),

    path('enrollment_create/', enrollment.enrollment_create, name='enrollment_create'),
    

    path('teacher_view/', teacher.teacher_view, name='teacher_view'),

    path('section_view/', section.section_view, name='section_view'),
    path('<str:sec_id>/section_student_list/', section.section_student_list, name='section_student_list'),


]