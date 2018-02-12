from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import *
from .commands import checkCSV, handleUploadedFile

# BE CAREFUL OF REQUEST METHODS

def home(request):
	uploadForm = addUploadForm(request)
	return render(request, 'index.html', {'upload': uploadForm})

def fieldForm(request, fieldSet):
	fieldForm = addFieldsForm(request, fieldSet)
	return render(request, 'fields.html', {'fields': fieldForm})
	
	
def addFieldsForm(fields, request):
	if request:
		if request.method == 'POST':
			
			form = FieldSelectionForm(request.POST)
			
			if form.is_valid():
				print("Field selection valid")
			else:
				print("Field selection not valid")
				
	else:
		form = FieldSelectionForm()
		form.addFieldSet(fields)
		print("Blank Fields form created")
		
	return form

def addUploadForm(request):
	if request.method == 'POST' and request.FILES['myFile']:
		print("Check")
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid:
			print("File uploaded and valid")
			uploadedFile = request.FILES['myFile']
			if uploadedFile:
				print("There is a file")
				if checkCSV(uploadedFile):
					fields = handleUploadedFile(uploadedFile)
					return addFieldsForm(fields, None)
		else:
			print("Upload error possibly due to encryption")
	else:
		form = UploadFileForm()
		return form
