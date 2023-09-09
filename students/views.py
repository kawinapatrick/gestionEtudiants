from django.shortcuts import render, redirect
from .models import Student
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.urls import reverse
from .forms import StudentForm
from django.template.loader import get_template
import pdfkit
import io


# Create your views here.
def index(request):
    student_object = Student.objects.all()
    item = request.GET.get('item')
    if item !='' and item is not None:
        student_object = Student.objects.filter(first_name__icontains=item)
    return render(request, 'students/index.html', { 'students': student_object })

def view_student(request, id):
    student = Student.objects.get(pk=id)
    return HttpResponseRedirect(reverse('index'))

def add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            new_student_number = form.cleaned_data['student_number']
            new_first_name = form.cleaned_data['first_name']
            new_last_name = form.cleaned_data['last_name']
            new_email = form.cleaned_data['email']
            new_field_of_study = form.cleaned_data['field_of_study']
            new_gpa = form.cleaned_data['gpa']

            new_student = Student(
                student_number = new_student_number,
                first_name = new_first_name,
                last_name = new_last_name,
                email = new_email,
                field_of_study = new_field_of_study,
                gpa = new_gpa
           )
            new_student.save()
            return render(request, 'students/add.html', 
                          {'form': StudentForm(), 'success': True})
        
        
    else:
        form = StudentForm()
    return render(request, 'students/add.html', {'form': StudentForm()})

def edit(request, id):
    if request.method == 'POST':
        student = Student.objects.get(pk=id)
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return render(request, 'students/edit.html', {'form': form, 'success': True})
        
    else:
        student = Student.objects.get(pk=id)
        form = StudentForm(instance=student)

    return render(request, 'students/edit.html', {'form': form})

def delete(request, id):
    if request.method == 'POST':
        student = Student.objects.get(pk=id)
        student.delete()
    return HttpResponseRedirect(reverse('index'))

def generer(request, id):
    student = Student.objects.get(pk=id)
    va_student_number = student.student_number
    va_first_name = student.first_name
    va_last_name = student.last_name
    va_email = student.email
    va_field_of_study = student.field_of_study
    va_gpa = student.gpa
    

    template = get_template('students/generator.html')

    context = {'student_number':va_student_number, 'first_name':va_first_name, 'last_name':va_last_name, 'email':va_email, 'field_of_study':va_field_of_study, 'gpa':va_gpa }

    html = template.render(context)
    options = {
        'page-size':'letter',
        'encoding':'UTF-8',
    }
    pdf = pdfkit.from_string(html, False, options)

    reponse = HttpResponse(pdf, content_type='application/pdf')
    reponse['Content-Disposition']="attachement"
    return reponse


    


