from django.contrib import admin

from .models import Students,Teachers,Courses,Subjects,StudentSubjects

# Register your models here.
admin.site.register(Students)
admin.site.register(Teachers)
admin.site.register(Courses)
admin.site.register(Subjects)
admin.site.register(StudentSubjects)