from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request) :
    return HttpResponse("The generated force-vector spatializations should appear here.")

# Create your views here.
