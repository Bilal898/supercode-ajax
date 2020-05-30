from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib import messages
from django.core import serializers
from django.core.mail import send_mail, EmailMessage
from django_ajax.settings import EMAIL_HOST_USER


from .models import Students, Teachers, Courses, StudentSubjects, Subjects
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.

def FirstPageController(request):
    return HttpResponse("first page contoller")


def IndexPageController(request):
    return HttpResponse("index page contoller")


def HtmlPageController(request):
    return render(request, "htmlpage.html")


@login_required(login_url="/login_user/")
def addData(request):
    courses = Courses.objects.all()
    context = {
        'courses': courses
    }
    return render(request, "add_data.html", context)


@login_required(login_url="/login_user/")
def add_student(request):
    if request.method != 'POST':
        return HttpResponse("<h3>method not allowed</h3>")
    else:
        file = request.FILES['profile']
        fs = FileSystemStorage()
        profile_img = fs.save(file.name, file)
        try:
            course = Courses.objects.get(id=request.POST.get('course', ''))
            student = Students(name=request.POST.get('name', ''), email=request.POST.get('email', ''), standard=request.POST.get('standard', ''), hobbies=request.POST.get(
                'hobbies', ''), roll_no=request.POST.get('roll_no', ''), bio=request.POST.get('bio', ''), profile_image=profile_img, course=course)
            student.save()

            subject_list = request.POST.getlist('subjects[]')
            for subject in subject_list:
                subj = Subjects.objects.get(id=subject)
                student_subject = StudentSubjects(
                    subject_id=subj, student_id=student)
                student_subject.save()
            messages.success(request, "Student added successfully")
        except:
            messages.error(request, "Failed to add student")
    return HttpResponseRedirect("/addData")


@login_required(login_url="/login_user/")
def show_all_data(request):
    all_teachers = Teachers.objects.all()
    all_students = Students.objects.all()
    context = {
        'students': all_students,
        'teachers': all_teachers
    }
    return render(request, 'show_data.html', context)


@login_required(login_url="/login_user/")
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


@login_required(login_url="/login_user/")
def edit_student(request):
    if request.method != 'POST':
        return HttpResponse("<h3>method not allowed</h3>")
    else:
        student = Students.objects.get(id=request.POST.get('id'))
        if student == None:
            return HttpResponse("no student found")
        else:
            if request.FILES.get('profile') != None:
                file = request.FILES['profile']
                fs = FileSystemStorage()
                profile_img = fs.save(file.name, file)
            else:
                profile_img = None
        if profile_img != None:
            student.profile_image = profile_img

        student.name = request.POST.get('name', '')
        student.email = request.POST.get('email', '')
        student.standard = request.POST.get('standard', '')
        student.hobbies = request.POST.get('hobbies', '')
        student.roll_no = request.POST.get('roll_no', '')
        student.bio = request.POST.get('bio', '')
        student.save()

        messages.success(request, "updated successfully")
        return HttpResponseRedirect("update_student/"+str(student.id)+"")
        # profile_image=profile_img)


def LoginUser(request):
    if request.user == None or request.user == "" or request.user.username == "":
        return render(request, "login_page.html")
    else:
        return HttpResponseRedirect("/homePage")


def RegisterUser(request):
    # if request.user==None:
    return render(request, "register_page.html")
    # else:
    #     return HttpResponseRedirect("/homePage")


def SaveUser(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
            User.objects.create_user(username, email, password)
            messages.success(request, "User Created Successfully")
            return HttpResponseRedirect('/register_user')
        else:
            messages.error(request, "Email or Username Already Exist")
            return HttpResponseRedirect('/register_user')


def DoLoginUser(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed")
    else:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        login(request, user)

        if user != None:
            return HttpResponseRedirect('/homePage')
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect('/login_user')


@login_required(login_url="/login_user/")
def HomePage(request):
    return render(request, "home_page.html")


def LogoutUser(request):
    logout(request)
    request.user = None
    return HttpResponseRedirect("/login_user")


def testStudent(request):
    student = Students.objects.all()
    student_obj = serializers.serialize('python', student)
    return JsonResponse(student_obj, safe=False)


def SendPlainEmail(request):
    message = request.POST.get('message', '')
    subject = request.POST.get('subject', '')
    mail_id = request.POST.get('email', '')
    email = EmailMessage(subject, message, EMAIL_HOST_USER, [mail_id])
    email.content_subtype = 'html'
    email.send()
    return HttpResponse("sent")


def send_mail_plain_with_stored_file(request):
    message = request.POST.get('message', '')
    subject = request.POST.get('subject', '')
    mail_id = request.POST.get('email', '')
    email = EmailMessage(subject, message, EMAIL_HOST_USER, [mail_id])
    email.content_subtype = 'html'

    file = open("README.md", "r")
    email.attach("README.md", file.read(), 'text/plain')
    email.send()
    return HttpResponse("sent")


def send_mail_plain_with_file(request):
    message = request.POST.get('message', '')
    subject = request.POST.get('subject', '')
    mail_id = request.POST.get('email', '')
    email = EmailMessage(subject, message, EMAIL_HOST_USER, [mail_id])
    email.content_subtype = 'html'

    file = request.FILES['file']
    email.attach(file.name, file.read(), file.content_type)
    email.send()
    return HttpResponse("sent")
