from django.http import HttpResponse

def index(request) :
    return HttpResponse("Hello, this will contain graphs")

# Create your views here.
