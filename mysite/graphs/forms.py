from django import forms
from django.forms import formset_factory

def createMiniForm(choices = [("DEFAULT", "Select a value")], request = None):
	
	class MiniForm(forms.Form):
		choicesInField = choices
		Name = forms.CharField()
		Key = forms.MultipleChoiceField(required = True, choices = choices)
	
	if request:
		return MiniForm(request)

	return MiniForm
	
	
class UploadFileForm(forms.Form):
    myFile = forms.FileField()


def produceFormSet(dictionary, unknownValues):
	unknown = []
	itial = []
	count = 0
	
	for key in dictionary:
		if dictionary[key]:
			count = count + 1
			itial.append({'Key': dictionary[key],'Name': key})
			print(dictionary[key])
				
	for i in unknownValues:
		unknown.append((i,i))
	
	form = formset_factory(createMiniForm(unknown), extra = (len(unknown) - count))
	finalForm = form(initial = itial) 
	
	return {'form' : finalForm, 'count' : len(unknown)}