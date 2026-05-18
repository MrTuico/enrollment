from django.contrib import admin
from .models import Course, Student, Instructor, Subject, Section, Schedule, Enrollment,GradeLevel, Attendance


# ----------------------
# Inline: Schedule inside Section
# ----------------------
class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 1


# ----------------------
# Course Admin
# ----------------------
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name',)
    search_fields = ('course_name',)


# ----------------------
# Student Admin
# ----------------------
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'contact_number')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('gender',)


# ----------------------
# Instructor Admin
# ----------------------
@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'contact_number')
    search_fields = ('first_name', 'last_name')


# ----------------------
# Subject Admin
# ----------------------
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_code', 'subject_name', 'course', 'units')
    search_fields = ('subject_code', 'subject_name')
    list_filter = ('course',)


# ----------------------
# Section Admin (IMPORTANT)
# ----------------------
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('section_name', 'instructor', 'semester', 'room')
    list_filter = ('semester',)
    search_fields = ('section_name',)

    inlines = [ScheduleInline]  # 👈 schedules inside section

    def student_count(self, obj):
        return obj.enrollment_set.count()

    student_count.short_description = "Students"


# ----------------------
# Enrollment Admin
# ----------------------
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student',  'status', 'date_enrolled','school_year', 'grade')
    list_filter = ('status','school_year')
    search_fields = ('student__first_name', 'student__last_name')

    autocomplete_fields = ('student',)  # 🔥 faster selection

@admin.register(GradeLevel)
class GradeLevelAdmin(admin.ModelAdmin):
    list_display = ('grade_id','grade_no')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student','section')