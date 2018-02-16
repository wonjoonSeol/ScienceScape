from django import forms

class AbstractField(forms.MultipleChoiceField):

	__choicesInField = [("DEFAULT", "Select a value")]

	def __init__(self, name, choice = [("DEFAULT", "Select a value")]):
		self._name = name
		super().__init__(required=False, choices=choice)
		
	def name(self, aName = None):
		if aName: self._name = aName
		return self._name



class FieldSelectionForm(forms.Form):
	listOfFields = []

	def addFieldSet(self, fields):
		for field in fields:
			self.addFieldSelection(field)

		self.populateForm()

	def addFieldSelection(self, field):
		if isinstance(field, AbstractField):
			field.label = field.name()
			self.listOfFields.append(field)

	def populateForm(self):
		for field in self.listOfFields:
			self.fields['{name}'.format(name=field.name())] = field

class UploadFileForm(forms.Form):
    myFile = forms.FileField()
	