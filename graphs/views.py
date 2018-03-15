from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import *
from .commands import *
from django.forms import formset_factory
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib.auth import logout
import os
from django.contrib.auth import authenticate, login

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def home(request):
	print("Username is: {x}".format(x = request.user.username))
	registration_form = UserRegistrationForm()

	if request.method == 'POST' and request.FILES['file']:
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid:
			uploaded_file = request.FILES['file']
			if uploaded_file and checkCSV(uploaded_file):
				if request.user.username:
					fPath = saveFile(uploaded_file, request.user.username)['FULL_FILE_NAME']
				else:
					fPath = saveFile(uploaded_file)['FULL_FILE_NAME']
				return redirect('fields', fPath)
		else:
			print("Form not Valid")
	else:
		form = UploadFileForm()

	files = ""
	if request.user.is_authenticated:
		files = get_all_user_files(request.user.username)

	return render(request, 'index.html', {'upload': form, 'reg_form': registration_form, 'fpath': "/userFiles/arctic.gexf", 'filename': "Example", 'usersFiles': files })

def edit_fields(request, filename):
	folder = "static/userFiles/{user_name}/{file_name}".format(user_name = request.user.username, file_name = filename)
	file_path = os.path.join(APP_DIR, folder)
	return redirect('fields', file_path)

def delete_file(request, filename):
	folder = "static/userFiles/{user_name}/{file_name}".format(user_name = request.user.username, file_name = filename)
	file_path = os.path.join(APP_DIR, folder)
	os.remove(file_path)
	mapping_exists = Mappings.objects.filter(FILE_LINK = file_path)
	if mapping_exists:
		mapping_exists.delete()
	return redirect('/')

def field_form(request, file_path):
	form = load_from_file_path(file_path)
	message = ""
	if request.method == 'POST':
		data = {}
		form_is_valid = True

		for i in range (0, form['count']):
			print("key: {k} is {v}".format(k = request.POST.get('form-{n}-Name'.format(n = i)), v = request.POST.get('form-{n}-Key'.format(n = i))))
			data[request.POST.get('form-{n}-Name'.format(n = i))] = request.POST.get('form-{n}-Key'.format(n = i))
			for k in data:
				if not k:
					message = "Not all fields have been defined"
					form_is_valid = False

		if form_is_valid:
			refreshDataBase(data, file_path)
			return redirect('/')

	if file_path:
		file_name =  str(file_path)
		tokens = file_name.split('/')
		file_name = tokens[-1]
	else:
		file_name = None

	return render(request, 'index.html', {'fields': form['form'], 'filename': file_name, 'message': message})

def about(request):
	return render(request, 'about.html')

def load_graph(request, file_path):
	upload_gexf_form = UploadFileForm()

	if request.method == 'POST' and request.FILES['file']:
		upload_gexf_form = UploadFileForm(request.POST, request.FILES)
		if upload_gexf_form.is_valid:
			print("VALID")
			uploaded_file = request.FILES['file']
			file_name = uploaded_file.name
			file_path = '/userFiles/' + saveFile(uploaded_file)['USER_FILE_NAME']
			print("file path: {x}".format(x = file_path))
		else:
			print("NOT VALID")
	else:
		file_name = "No file uploaded"
		file_path = "/userFiles/arctic.gexf"

	if file_path == "INITIAL":
		print("checkpoint")
		file_path = "/userFiles/arctic.gexf"
		file_name = "No file uploaded"

	return render(request, 'index.html', {'fpath': file_path, 'upload_gexf': upload_gexf_form,'fname': file_name})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            formData = form.cleaned_data
            username = formData['username']
            password = formData['password']
            email = formData['email']
            if not (User.objects.filter(username = username).exists() or User.objects.filter(email = email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username = username, password = password)
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                raise forms.ValidationError('This user/pswd combination already exists')
    else:
        form = UserRegistrationForm()

    return render(request, 'mysite/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_process(request):
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username = username, password = password)

		if user is not None:
			if user.is_active:
				login(request, user)
	return HttpResponseRedirect('/')

def account(request):
	return render(request, 'account.html')
