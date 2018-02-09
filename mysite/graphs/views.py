from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import *
from .commands import *

# BE CAREFUL OF REQUEST METHODS

def home(request) :

	uploadForm = addUploadForm(request)
	fieldsFrom = addFieldsForm(request)
	return render(request, 'index.html', {'upload': uploadForm, 'fields': fieldsFrom})




def addFieldsForm(request):
	print("Fields form called")
	fields = []

	for field in range(1, 20):
		f = AbstractField("FIELD: {x}".format(x = field), [(("1", "RECORD 1"))])
		fields.append(f)

	if request.method == 'POST':
		form = FieldSelectionForm(request.POST)
		print("Fields form created")

		if form.is_valid():
			print("Valid from fields")
		else:
			print("Not valid")

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
					handleUploadedFile(uploadedFile)
		else:
			print("Upload error possibly due to encryption")
	else:
		form = UploadFileForm()
		return form
