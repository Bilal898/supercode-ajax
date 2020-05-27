from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages

from .models import Students, Teachers

# Create your views here.

def FirstPageController(request):
    return HttpResponse("first page contoller")

def IndexPageController(request):
    return HttpResponse("index page contoller")

def HtmlPageController(request):
    return render(request, "htmlpage.html")

def addData(request):
    return render(request, "add_data.html")

def add_student(request):
    if request.method !='POST':
        return HttpResponse("<h3>method not allowed</h3>")
    else:
        file=request.FILES['profile']
        fs=FileSystemStorage()
        profile_img=fs.save(file.name,file)
        try:
            student=Students(name=request.POST.get('name',''),email=request.POST.get('email',''),standard=request.POST.get('standard',''),hobbies=request.POST.get('hobbies',''),roll_no=request.POST.get('roll_no',''),bio=request.POST.get('bio',''),profile_image=profile_img)
            # ,course=course
            student.save()
            messages.success(request, "Student added successfully")
        except:
            messages.error(request, "Failed to add student")
    return HttpResponseRedirect("/addData")

def show_all_data(request):
    all_teachers = Teachers.objects.all()
    all_students = Students.objects.all()
    context = {
        'students': all_students,
        'teachers': all_teachers
    }
    return render(request, 'show_data.html', context)
    
def delete_student(request, student_id):
    student = Students.objects.get(id=student_id)
    if student == None:
        return HttpResponse("no student found")
    else:
        student.delete()
        messages.success(request, "deleted successfully")
        return HttpResponseRedirect("/show_all_data")
    
def update_student(request, student_id):
    student = Students.objects.get(id=student_id)
    if student == None:
        return HttpResponse("no student found")
    else:
        context = {
            'student': student
        }
        return render(request, 'student_edit.html', context)

def edit_student(request):
    if request.method !='POST':
        return HttpResponse("<h3>method not allowed</h3>")
    else:
        student = Students.objects.get(id=request.POST.get('id'))
        if student == None:
            return HttpResponse("no student found")
        else:
            if request.FILES.get('profile')!=None:
                file=request.FILES['profile']
                fs=FileSystemStorage()
                profile_img=fs.save(file.name,file)
            else:
                profile_img=None
        if profile_img!=None:
            student.profile_image = profile_img

        student.name=request.POST.get('name','')
        student.email=request.POST.get('email','')
        student.standard=request.POST.get('standard','')
        student.hobbies=request.POST.get('hobbies','')
        student.roll_no=request.POST.get('roll_no','')
        student.bio=request.POST.get('bio','')
        student.save()

        messages.success(request, "updated successfully")
        return HttpResponseRedirect("update_student/"+str(student.id)+"")
        # profile_image=profile_img)
