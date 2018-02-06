from django.http import HttpResponse
from django.shortcuts import render

def index(request) :
    return HttpResponse("The generated force-vector spatializations should appear here.")

# Create your views here.
