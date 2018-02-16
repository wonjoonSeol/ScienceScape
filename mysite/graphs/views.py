from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import *
from .commands import *

# BE CAREFUL OF REQUEST METHODS

def home(request):
	
	if request.method == 'POST' and request.FILES['myFile']:
		print("Check")
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid:
			print("File uploaded and valid")
			uploadedFile = request.FILES['myFile']
			if uploadedFile:
				print("There is a file")
				if checkCSV(uploadedFile):	
					fPath = saveFile(uploadedFile)
					return redirect('fields', fPath)
		else:
			print("Upload error possibly due to encryption or method")
	else:
		form = UploadFileForm()
	
	return render(request, 'index.html', {'upload': form})
	

def fieldForm(request, filePath):
	
	fields = loadFromFilePath(filePath)
		
	if request.method == 'POST':

			form = FieldSelectionForm(request.POST)
			form.addFieldSet(fields)
			
			if form.is_valid():
				data = form.cleaned_data
				
				refreshDataBase(data,filePath)
				
				print("Field selection valid")
				print(data)
				
			else:
				print("Field selection not valid")
				
	else:
		form = FieldSelectionForm()
		form.addFieldSet(fields)
		print("Blank Fields form created")
	
	if filePath:
		fname =  str(filePath)
		tokens = fname.split('/')
		fname = tokens[-1]
	else:
		fname = None
		print(form)
		
	return render(request, 'index.html', {'fields': form, 'filename': fname})

	
