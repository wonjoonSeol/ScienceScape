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

def home(request, message = ""):
	print("Username is: {x}".format(x = request.user.username))
	registration_form = UserRegistrationForm()

	files = ""
	if request.user.is_authenticated:
		return redirect('upload', '')

	return render(request, 'index.html', {'msg': message, 'reg_form': registration_form, 'fpath': "/javascript/sigma.js-1.2.1/examples/data/standard_graph.gexf" })

def upload_file(request, message = ""):
	print("Username is: {x}".format(x = request.user.username))

	if request.method == 'POST' and request.FILES['file']:
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid:
			uploaded_file = request.FILES['file']
			if uploaded_file and check_txt_file(uploaded_file):
				if request.user.username:
					fPath = save_file(uploaded_file, request.user.username)['FULL_FILE_NAME']
				else:
					fPath = save_file(uploaded_file)['FULL_FILE_NAME']
				return redirect('fields', fPath)
			else:
				message = "Please upload a tab delimited file"
		else:
			print("Form not Valid")
	else:
		form = UploadFileForm()

	files = ""
	if request.user.is_authenticated:
		files = get_all_user_files(request.user.username)

	return render(request, 'logged_in.html', {'msg': message,'upload': form,  'usersFiles': files })


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
	return redirect(upload_file, " ")

def select_years(request, file_path):
	if request.method == 'POST':
		year_form = DefineYears(request.POST)
		if year_form.is_valid():
			from_date = request.POST.get('From')
			to_date = request.POST.get('To')
			print("From date {x}, and To date {y}".format(x=to_date,y=from_date))
			if request.user.is_authenticated:
				output_path = start_bibliotools(from_date, to_date, file_path, request.user.username)
			else:
				output_path = start_bibliotools(from_date, to_date, file_path)
			return redirect('load_graph', output_path)
	else:
		year_form = DefineYears()
	return render(request, 'select_years.html', {'years': year_form, 'fpath': file_path})

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
			refresh_database(data, file_path)
			if request.user.is_authenticated:
				return redirect('upload', ' ')
			else:
				return redirect(select_years, file_path)

	if file_path:
		file_name =  str(file_path)
		tokens = file_name.split('/')
		file_name = tokens[-1]
	else:
		file_name = None

	return render(request, 'enter_fields_template.html', {'fields': form['form'], 'filename': file_name, 'message': message})

def about(request):
	return render(request, 'about.html')

def upload_single_gexf_file(request, file_path):
	upload_gexf_form = UploadFileForm()

	if request.method == 'POST' and request.FILES['file']:
		upload_gexf_form = UploadFileForm(request.POST, request.FILES)
		if upload_gexf_form.is_valid:
			print("VALID")
			uploaded_file = request.FILES['file']
			file_name = uploaded_file.name
			file_path = '/userFiles/' + save_file(uploaded_file)['USER_FILE_NAME']
			print("file path: {x}".format(x = file_path))
		else:
			print("NOT VALID")
	else:
		file_name = "No file uploaded"
		file_path = "/userFiles/arctic.gexf"

def turn_path_into_string(path_with_brackets):
	return path_with_brackets.replace("['", "").replace("']", "")

def load_graph(request, file_path):
	return render(request, 'graph_template.html', {'fpath': turn_path_into_string(file_path), 'fname': "Your beautiful graph file"})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            formData = form.cleaned_data
            username = formData['username']
            password = formData['password']
            email = formData['email']
            create_user_folder(username)
            if not (User.objects.filter(username = username).exists() or User.objects.filter(email = email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username = username, password = password)
                login(request, user)
                return redirect('upload',  " ")
            else:
                return redirect('wrongUser', "User password combination already exists")
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
			else:
				return redirect('wrongUser', "Incorrect credentials")
		else:
			 return redirect('wrongUser', "Incorrect credentials")

	return redirect('upload', " ")

def account(request):
	return render(request, 'account.html')
