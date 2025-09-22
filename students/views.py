from django.http import HttpResponse


def students(request):
    return HttpResponse("Welcome")