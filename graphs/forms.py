from django import forms
from django.forms import formset_factory

class UploadFileForm(forms.Form):
    file = forms.FileField(label = '')

class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        required = True,
        label = 'Username',
        max_length = 32,
    )
    email = forms.EmailField(
        required = True,
        label = 'Email',
        max_length = 32,
    )
    password = forms.CharField(
        required = True,
        label = 'Password',
        max_length = 32,
        widget = forms.PasswordInput(),
    )

""" Return a MiniForm.
Creates a mini form from a list of choices (default or "select a value").
"""
def create_mini_form(choices = [("DEFAULT", "Select a value")], request = None):

	class MiniForm(forms.Form):
		choicesInField = choices
		Name = forms.CharField()
		Key = forms.ChoiceField(required = True, choices = choices)

	if request:
		return MiniForm(request)
	else:
		return MiniForm

""" Return a dictionary containing the final form and the number
of unknown values.
Produces a set of forms from a dictionary and a list of unknown values.
"""
def produce_form_set(dictionary, unknown_values):
	unknown = []
	initial = []
	entry_count = 0

	for entry in dictionary:
		if dictionary[entry]:
			entry_count = entry_count + 1
			initial.append({'Key': dictionary[entry],'Name': entry})
			print(dictionary[entry])

	for i in unknown_values:
		unknown.append((i,i))

	form = formset_factory(create_mini_form(unknown), extra = (len(unknown) - entry_count))
	finalForm = form(initial = initial)

	return {'form' : finalForm, 'count' : len(unknown)}
