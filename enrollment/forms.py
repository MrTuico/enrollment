from django import forms
from datetime import date
from enrollment.models import *
from django_select2.forms import Select2Widget
from datetime import datetime

class StudentForm(forms.ModelForm):
    middle_name = forms.CharField(required=False)
    ext_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    contact_number = forms.CharField(required=False)
    address = forms.CharField(max_length=500)

    class Meta:
        model = Student
        fields = [
            'lrn_no',
            'first_name',
            'middle_name',
            'last_name',
            'ext_name',
            'date_of_birth',
            'gender',
            'address',
            'contact_number',
            'email',
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'lrn_no': 'LRN No.',
            'first_name': 'Enter first name',
            'middle_name': 'Enter middle name',
            'last_name': 'Enter last name',
            'ext_name': 'e.g. Jr, Sr',
            'contact_number': '09XXXXXXXXX',
            'email': 'example@email.com',
            'address': 'Enter complete address',
        }

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'

            else:
                field.widget.attrs['class'] = 'form-control'

            if name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[name]

            if name == 'date_of_birth':
                field.widget = forms.DateInput(attrs={
                    'type': 'date',
                    'class': 'form-control'
                })
    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        today = date.today()
        if dob:
            if dob.year < 1900 or dob > today:
                raise forms.ValidationError("Please enter a valid year of birth (e.g., 1995).")
        return dob

class TeacherForm(forms.ModelForm):
    middle_name = forms.CharField(required=False)
    ext_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    contact_number = forms.CharField(required=False)
    address = forms.CharField(max_length=500)

    class Meta:
        model = Instructor
        fields = [
            'first_name',
            'middle_name',
            'last_name',
            'ext_name',
            'date_of_birth',
            'gender',
            'address',
            'contact_number',
            'email',
            'licno',
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'first_name': 'Enter first name',
            'middle_name': 'Enter middle name',
            'last_name': 'Enter last name',
            'ext_name': 'e.g. Jr, Sr',
            'contact_number': '09XXXXXXXXX',
            'email': 'example@email.com',
            'address': 'Enter complete address',
            'licno': 'License Number',
        }

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'

            else:
                field.widget.attrs['class'] = 'form-control'

            if name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[name]

            if name == 'date_of_birth':
                field.widget = forms.DateInput(attrs={
                    'type': 'date',
                    'class': 'form-control'
                })
    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        today = date.today()
        if dob:
            if dob.year < 1900 or dob > today:
                raise forms.ValidationError("Please enter a valid year of birth (e.g., 1995).")
        return dob


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = [
            'student',
            'school_year',
            'prev_grade',
            'grade',
        ]
        widgets = {
            'student': Select2Widget(attrs={'data-placeholder': 'Select a Student','class': 'form-select','id':'id_student'})
            },
            

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'student': 'Select a Student',
            'prev_grade': 'prev_grade',
            'grade': 'Enter grade (optional)',
        }

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

            if name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[name]

            if name == 'date_enrolled':
                field.widget = forms.DateInput(attrs={
                    'type': 'date',
                    'class': 'form-control'
                })
        current_year = datetime.now().year
        year_choices = [(f"{year}-{year+1}", f"{year}-{year+1}") for year in range(current_year, current_year + 5)]
        self.fields['school_year'] = forms.ChoiceField(
            choices=year_choices,
            widget=forms.Select(attrs={'class': 'form-select'})
        )
        
class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = [
            'grade_level',
            'section_name',
            'instructor',
            'semester',
            'room',
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'grade_level': 'Select a Grade Level',
            'section_name': 'Section Name',
            'instructor': 'Select Instructor',
            'semester': 'Semester',
            'school_year': 'e.g. 2025-2026',
            'room': 'room',
           
        }

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

            if name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[name]
        
        