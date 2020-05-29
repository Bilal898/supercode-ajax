from .models import Students, Teachers, Courses, StudentSubjects, Subjects
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def getSubjects(request):
    subject=Subjects.objects.filter(course_id=request.POST.get('course_id'))
    student_obj = serializers.serialize('python', subject)
    return JsonResponse(student_obj, safe=False)
