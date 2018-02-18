from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import *
from .commands import *
from django.forms import formset_factory

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
	
	form = loadFromFilePath(filePath)	
	if request.method == 'POST':
			data = {}
			for i in range (0, form['count']):
				print("key: {k} is {v}".format(k = request.POST.get('form-{n}-Name'.format(n = i)), v = request.POST.get('form-{n}-Key'.format(n = i))))
				data[request.POST.get('form-{n}-Name'.format(n = i))] = request.POST.get('form-{n}-Key'.format(n = i))
			
			refreshDataBase(data, filePath)
			retrieveFromDataBase(filePath)
			
			APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
			gexfFilePath = os.path.join(APP_DIR, 'userFiles/yeast.gexf')
			
			return redirect('loadGraph', gexfFilePath)

	else:
		print("Blank fields form created")

	if filePath:
		fname =  str(filePath)
		tokens = fname.split('/')
		fname = tokens[-1]
	else:
		fname = None
		print(form)

	return render(request, 'index.html', {'fields': form['form'], 'filename': fname})

def loadGraph(request, filePath):

	return render(request, 'index.html', {'filePath': filePath})
