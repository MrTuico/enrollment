from django.db import models
import uuid
from datetime import date
from django.utils import timezone


# ----------------------
# Course Model
# ----------------------
class GradeLevel(models.Model):
    grade_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    grade_no = models.CharField(max_length=5,unique=True)

    def __str__(self):
        return self.grade_no

# ----------------------
# Course Model
# ----------------------
class Course(models.Model):
    course_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    grade = models.ForeignKey(GradeLevel, on_delete=models.CASCADE,null=True, blank=True)
    course_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.course_name

# ----------------------
# Student Model
# ----------------------
GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
class Student(models.Model):
    student_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    lrn_no = models.CharField(max_length=50,unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    ext_name = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    contact_number = models.CharField(max_length=20,default=0,blank=True)
    email = models.EmailField(blank=True,null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['first_name','middle_name','ext_name', 'last_name', 'date_of_birth'], 
                name='unique_student_identity'
            )
        ]

    @property
    def age(self):
        today = date.today()
        dob = self.date_of_birth
        age = today.year - dob.year
        if (today.month, today.day) < (dob.month, dob.day):
            age -= 1
        return age

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class StudentGuardian(models.Model):
    student_guardian = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    ext_name = models.CharField(max_length=20)
    relationToStudent = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=20)
    address = models.TextField()
    email = models.EmailField(unique=True,blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# ----------------------
# Instructor Model
# ----------------------
class Instructor(models.Model):
    instructor_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    ext_name = models.CharField(max_length=20)
    date_of_birth = models.DateField(default=timezone.now)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,default='M')
    address = models.TextField(default='N/A')
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=20,default='N/A')
    licno = models.CharField(max_length=50,default='N/A',unique=True)

    @property
    def age(self):
        today = date.today()
        dob = self.date_of_birth
        age = today.year - dob.year
        if (today.month, today.day) < (dob.month, dob.day):
            age -= 1
        return age

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# ----------------------
# Enrollment Model
# ----------------------
STATUS_CHOICES = [
        ('enrollee', 'Enrollee'),
        ('enrolled', 'Enrolled'),
        ('dropped', 'Dropped'),
        ('completed', 'Completed'),
    ]

class Section(models.Model):
    section_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    grade_level = models.ForeignKey(GradeLevel, on_delete=models.CASCADE,null=True, blank=True)
    section_name = models.CharField(max_length=20)  # e.g GRADE 7
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE,null=True, blank=True)
    semester = models.CharField(max_length=20,null=True, blank=True)
    room = models.CharField(max_length=20,default="N/A")

    def __str__(self):
        return f"{self.grade_level} - {self.section_name}"

class Enrollment(models.Model):
    enrollment_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    student = models.ForeignKey(Student, on_delete=models.RESTRICT)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True)
    date_enrolled = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='enrollee')
    school_year = models.CharField(max_length=10,null=True, blank=True)
    prev_grade =   models.CharField(max_length=2,default=0)
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'grade','prev_grade'], name='unique_student_grade')
        ]

    def __str__(self):
        return f"{self.student}"



# ----------------------
# Subject Model
# ----------------------
class Subject(models.Model):
    subject_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    subject_code = models.CharField(max_length=50)
    subject_name = models.CharField(max_length=100)
    units = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.RESTRICT)

    def __str__(self):
        return f"{self.subject_code} - {self.subject_name}"


# ----------------------
# Schedule Model
# ----------------------
DAY_CHOICES = [
        ('Sun', 'Sunday'),
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
    ]
class Schedule(models.Model):
    schedule_id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    subject = models.ForeignKey(Subject, on_delete=models.RESTRICT)
    section = models.ForeignKey(Section, on_delete=models.RESTRICT)
    instructor = models.ForeignKey(Instructor, on_delete=models.RESTRICT)
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    time_start = models.TimeField()
    time_end = models.TimeField()
    room = models.CharField(max_length=20)

    def clean(self):
        conflicts = Schedule.objects.filter(section=self.section,day=self.day).exclude(pk=self.pk)

        for sched in conflicts:
            if (self.time_start < sched.time_end and self.time_end > sched.time_start):
                raise ValidationError("Schedule conflict detected!")

    def __str__(self):
        return f"{self.section} ({self.day} {self.time_start}-{self.time_end})"


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Late'),
        ('E', 'Excused'),
    ]


    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    date = models.DateField()
    am_status = models.CharField(max_length=1, choices=STATUS_CHOICES,blank=True, null=True)
    pm_status = models.CharField(max_length=1, choices=STATUS_CHOICES,blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
   

    class Meta:
        unique_together = ('student', 'section', 'date')

    def __str__(self):
        return f"{self.date} - {self.student} - AM:{self.am_status} PM:{self.pm_status}"

    


