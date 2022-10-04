from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're going to die. But how?")