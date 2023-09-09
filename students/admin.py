from django.contrib import admin
from .models import Student

# Register your models here.
class AdminStudent(admin.ModelAdmin):
    list_display = ('student_number', 'first_name', 'last_name', 'email', 'field_of_study', 'gpa')

admin.site.register(Student, AdminStudent)
