from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import *
from .commands import *
from django.forms import formset_factory
from .tests import *
from django.conf import settings

# BE CAREFUL OF REQUEST METHODS

def home(request):
	
	attemptDatabaseTest()
	
	if request.method == 'POST' and request.FILES['myFile']:
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid:
			uploadedFile = request.FILES['myFile']
			if uploadedFile:
				if checkCSV(uploadedFile):
					fPath = saveFile(uploadedFile)['FULL_FILE_NAME']
					return redirect('fields', fPath)
		else:
			print("Form not Valid")
	else:
		form = UploadFileForm()
	
	return render(request, 'index.html', {'upload': form, 'fpath':"/userFiles/arctic.gexf"})


def fieldForm(request, filePath):
	
	form = loadFromFilePath(filePath)	
	if request.method == 'POST':
			data = {}
			for i in range (0, form['count']):
				print("key: {k} is {v}".format(k = request.POST.get('form-{n}-Name'.format(n = i)), v = request.POST.get('form-{n}-Key'.format(n = i))))
				data[request.POST.get('form-{n}-Name'.format(n = i))] = request.POST.get('form-{n}-Key'.format(n = i))
			
			refreshDataBase(data, filePath)
			
			return redirect('loadGraph', "INITIAL")

	if filePath:
		fname =  str(filePath)
		tokens = fname.split('/')
		fname = tokens[-1]
	else:
		fname = None
		print(form)

	return render(request, 'index.html', {'fields': form['form'], 'filename': fname})


def loadGraph(request, filePath):
	
	upload_gexf_form = UploadFileForm()
	if request.method == 'POST' and request.FILES['myFile']:
		upload_gexf_form = UploadFileForm(request.POST, request.FILES)
		if upload_gexf_form.is_valid:
			print("VALID")
			
			uploadedFile = request.FILES['myFile']
			fname=uploadedFile.name
			filePath = '/userFiles/' + saveFile(uploadedFile)['USER_FILE_NAME']
			print("file path: {x}".format(x=filePath))
		
		else:
			print("NOT VALID")
	else:
		fname="No file uploaded"
		filePath="userFile/arctic.gexf"
		
	return render(request, 'index.html', {'fpath': filePath, 'upload_gexf': upload_gexf_form,'fname': fname})
