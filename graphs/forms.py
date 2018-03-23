from django import forms
from django.forms import formset_factory

class UploadFileForm(forms.Form):
    file = forms.FileField(label = '')

"""
This class defines the structure for the basic Django user reg form.
"""
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

class DefineYears(forms.Form):
	From = forms.IntegerField()
	To = forms.IntegerField()

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
def produce_form_set(unknown_values):
	unknown = []
	initial = []
	entry_count = 0

	for i in unknown_values:
		unknown.append((i,i))

	form = formset_factory(create_mini_form(sorted(unknown)), extra=0)
	headers = ['UT','AU','DE','ID','TI','EC','CR','C1','PY','J9','VL','BP','DI','PT','DT','TC']
	initial = [{'Name': "accession_number", 'Key': headers[0]},
	{'Name': "authors",'Key': headers[1]},
	{'Name': "author_keywords",'Key': headers[2]},
	{'Name': "keywords_plus",'Key': headers[3]},
	{'Name': "document_title",'Key': headers[4]},
	{'Name': "wos_categories",'Key': headers[5]},
	{'Name': "cited_references",'Key': headers[6]},
	{'Name': "author_address",'Key': headers[7]},
	{'Name': "year_published",'Key': headers[8]},
	{'Name': "twenty_nine_character_source_abbreviation",'Key': headers[9]},
	{'Name': "volume",'Key': headers[10]},
	{'Name': "beginning_page",'Key': headers[11]},
	{'Name': "doi",'Key': headers[12]},
	{'Name': "publication_type",'Key': headers[13]},
	{'Name': "document_type",'Key': headers[14]},
	{'Name': "wos_core_collection_times_cited",'Key': headers[15]}]

	finalForm = form(initial = initial)

	return {'form' : finalForm, 'count' : 16}
