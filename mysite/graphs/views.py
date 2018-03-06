from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import *
from .commands import *
from django.forms import formset_factory
from .tests import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login

# BE CAREFUL OF REQUEST METHODS

def home(request):

	attemptDatabaseTest()
	print("Username is: {x}".format(x = request.user.username))
	Rform = UserRegForm()

	if request.method == 'POST' and request.FILES['myFile']:
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid:
			uploadedFile = request.FILES['myFile']
			if uploadedFile:
				if checkCSV(uploadedFile):
					if request.user.username:
						fPath = saveFile(uploadedFile, request.user.username)['FULL_FILE_NAME']
					else:
						fPath = saveFile(uploadedFile)['FULL_FILE_NAME']

					return redirect('fields', fPath)
		else:
			print("Form not Valid")
	else:
		form = UploadFileForm()
	
	return render(request, 'index.html', {'upload': form,'reg_form' : Rform, 'fpath':"/userFiles/arctic.gexf", 'filename': "Example"})


def fieldForm(request, filePath):

	form = loadFromFilePath(filePath)
	msg=""
	if request.method == 'POST':
			data = {}
			formValid = True
				
			for i in range (0, form['count']):
				#print("key: {k} is {v}".format(k = request.POST.get('form-{n}-Name'.format(n = i)), v = request.POST.get('form-{n}-Key'.format(n = i))))
				data[request.POST.get('form-{n}-Name'.format(n = i))] = request.POST.get('form-{n}-Key'.format(n = i))
				for k in data:
					if not data[k]:
						msg = "Not all fields have been defined"
						formValid=False
			
			if formValid:
				refreshDataBase(data, filePath)
				return redirect('loadGraph', "INITIAL")
			
	if filePath:
		fname =  str(filePath)
		tokens = fname.split('/')
		fname = tokens[-1]
	else:
		fname = None

	return render(request, 'index.html', {'fields': form['form'], 'filename': fname, 'message': msg})

def about(request):
	return render(request, 'about.html')

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
		filePath="/userFiles/arctic.gexf"
	
	if filePath == "INITIAL":
		print("checkpoint")
		filePath="/userFiles/arctic.gexf"
		fname="No file uploaded"
		
	return render(request, 'index.html', {'fpath': filePath, 'upload_gexf': upload_gexf_form,'fname': fname})


def register(request):
    if request.method == 'POST':
        form = UserRegForm(request.POST)
        if form.is_valid():
            formData = form.cleaned_data
            username = formData['username']
            password = formData['password']
            email = formData['email']
            if not (User.objects.filter(username=username).exists() or
                    User.objects.filter(email=email).exists()):
                    User.objects.create_user(username, email, password)
                    user = authenticate(username = username, password = password)
                    login(request,user)
                    return HttpResponseRedirect('/')
            else:
                raise forms.ValidationError('This user/pswd combination already exists')

    else:
        form = UserRegForm()

    return render(request, 'mysite/register.html', {'form' : form})



def logoutView(request):
    logout(request)
    return HttpResponseRedirect('/')

def loginProcess(request):
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)

		if user is not None:
			if user.is_active:
				login(request, user)

	return HttpResponseRedirect('/')
