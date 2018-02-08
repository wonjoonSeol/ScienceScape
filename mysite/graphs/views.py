from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import *


def home(request) :
		
	uploadForm = addUploadForm(request)
	fieldsFrom = addFieldsForm(request)

	return render(request, 'index.html', {'upload': uploadForm, 'fields': fieldsFrom})
 
 
 
 
def addFieldsForm(request):
	fields = []
	
	for field in range(1, 20):
		f = AbstractField("FIELD: {x}".format(x = field), [(("1", "RECORD 1"))])
		fields.append(f)	
	
	if request.method == 'POST':
		form = FieldSelectionForm(request.POST)
		form.addFieldSet(fields)
		
		if form.is_valid():
			print("valid!") 
	else:
		form = FieldSelectionForm()
	
	return form

def addUploadForm(request):
	
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    
    return form

