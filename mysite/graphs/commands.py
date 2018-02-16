from .forms import AbstractField
from csv import DictReader
from csv import reader
import os
import re
from django.db import models
from .models import Mappings

'''Takes an uploaded file and does the following:
	1.Saves the file to userFiles
	2.Produces a dictionary of raw headers mapped to a set of its records
	3.Attempts to detect which headers belong to which fields
	4.Returns a list of AbstractFields to be added to the fields form.
'''
def handleUploadedFile(f):
    if f:
        print("File has been uploaded successfully!")
        filePath = saveFile(f)
        dictionary = processCSVIntoDictionary(filePath)
        knownAndUnknownValues = detectHeadersFrom(dictionary)
        fields = produceAbstractFields(knownAndUnknownValues['headers'], knownAndUnknownValues['unknownValues'])

        return fields

'''Does the same thing as handleUploadedFile, but from a filePath instead
'''
def loadFromFilePath(fp):
	dictionary = processCSVIntoDictionary(fp)
	knownAndUnknownValues = detectHeadersFrom(dictionary)
	fields = produceAbstractFields(knownAndUnknownValues['headers'], knownAndUnknownValues['unknownValues'])

	return fields

'''Checks a file to make sure it is a csv file
'''
def checkCSV(f):
    if f.name[-4:] == ".csv":
        print("File is .csv")
        return True
    else:
        print("File is not .csv")
        return False

'''Processes the csv file and returns a dictionary of headers mapped to a set of values.
'''
def processCSVIntoDictionary(filePath, forFields = False):

	headerValueSets = dict()

	#open file to make header keys
	with open(filePath) as csvFile:
		myReader = reader(csvFile)
		for headers in myReader:
			for header in headers:
				headerValueSets[header] = set()
			break

	#open a fresh copy to make a DictReader and populate dictionary
	with open(filePath) as csvFile:
		myDictReader = DictReader(csvFile)
		for row in myDictReader:
			for key in headerValueSets:
				if(forFields):
					headerValueSets[key].add((row[key], row[key]))
				else:
					headerValueSets[key].add(row[key])
	return headerValueSets

'''Saves the file to userFiles folder in project root directory
'''
def saveFile(myFile):

    fileName = myFile.name
    folder = "userFiles"
    APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # create the folder if it doesn't exist.
    try:
    	 os.mkdir(os.path.join(APP_DIR, folder))
    	 print("Directory created: {x}".format(x = APP_DIR) )
    except:
    	pass

    # save the uploaded file inside that folder.
    fullFileName = os.path.join(APP_DIR, folder, fileName)
    fileToSave = open(fullFileName,'w')
    fileToSave.write(myFile.read().decode("utf-8"))
    fileToSave.close()
    print("File saved at {s}".format(s=fullFileName))
    return fullFileName

'''dictionary: the dictionary of all headers in the csv file
	unknownValues: values from the csv headers that have not yet been allocated
	Returns a list of AbstractFields to be added to the FieldsForm.
'''
def produceAbstractFields(dictionary, unknownValues):
	fields = []
	unknown = []
	for attribute in unknownValues:
		unknown.append((attribute,attribute ))

	for key in dictionary:
		if dictionary[key] == None:
			fields.append(AbstractField(key, unknown))
		else:
			fields.append(AbstractField(key, [(dictionary[key],dictionary[key]),("Wrong detection?", "Wrong detection?")]))

	return fields


'''Returns a dictionary of attributes mapped to Bibliotools representation of those attributes eg. Date: SS,
	and a list of unknown attributes that could not be detected.

	Reg ex for dates: (((\d(\d)?))/){2}((\d\d)(\d\d)?)
'''
countries = ["United States of America","Afghanistan","Albania","Algeria","Andorra","Angola","Antigua & Deps","Argentina","Armenia","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bhutan","Bolivia","Bosnia Herzegovina","Botswana","Brazil","Brunei","Bulgaria","Burkina","Burma","Burundi","Cambodia","Cameroon","Canada","Cape Verde","Central African Rep","Chad","Chile","People's Republic of China","Republic of China","Colombia","Comoros","Democratic Republic of the Congo","Republic of the Congo","Costa Rica,","Croatia","Cuba","Cyprus","Czech Republic","Danzig","Denmark","Djibouti","Dominica","Dominican Republic","East Timor","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Ethiopia","Fiji","Finland","France","Gabon","Gaza Strip","The Gambia","Georgia","Germany","Ghana","Greece","Grenada","Guatemala","Guinea","Guinea-Bissau","Guyana","Haiti","Holy Roman Empire","Honduras","Hungary","Iceland","India","Indonesia","Iran","Iraq","Republic of Ireland","Israel","Italy","Ivory Coast","Jamaica","Japan","Jonathanland","Jordan","Kazakhstan","Kenya","Kiribati","North Korea","South Korea","Kosovo","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Mauritania","Mauritius","Mexico","Micronesia","Moldova","Monaco","Mongolia","Montenegro","Morocco","Mount Athos","Mozambique","Namibia","Nauru","Nepal","Newfoundland","Netherlands","New Zealand","Nicaragua","Niger","Nigeria","Norway","Oman","Ottoman Empire","Pakistan","Palau","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Prussia","Qatar","Romania","Rome","Russian Federation","Rwanda","St Kitts & Nevis","St Lucia","Saint Vincent & the","Grenadines","Samoa","San Marino","Sao Tome & Principe","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","Solomon Islands","Somalia","South Africa","Spain","Sri Lanka","Sudan","Suriname","Swaziland","Sweden","Switzerland","Syria","Tajikistan","Tanzania","Thailand","Togo","Tonga","Trinidad & Tobago","Tunisia","Turkey","Turkmenistan","Tuvalu","Uganda","Ukraine","United Arab Emirates","United Kingdom","Uruguay","Uzbekistan","Vanuatu","Vatican City","Venezuela","Vietnam","Yemen","Zambia","Zimbabwe"]

def detectHeadersFrom(dictionary):

	headers = dict(Author=None, Date=None, Country=None)
	unknownValues = []
	datePattern = re.compile('(((\d(\d)?))/){2}((\d\d)(\d\d)?)', re.IGNORECASE)

	for k in dictionary:
		unknownValues.append(k)
	print('This is the dictionary {x}'.format(x=dictionary))
	for k in dictionary:
		if datePattern.match(dictionary[k].pop()):
			headers['Date'] = k
			unknownValues.remove(k)
			print("matched date")
		elif dictionary[k] in countries:
			headers['Country'] = k
			unknownValues.remove(k)
			print("matched country")

	return {'headers': headers, 'unknownValues': unknownValues}

'''
'''
def dataProcess(key = None, weights = 0, minOccur = 0):
	return dictionary[key]

'''This method refreshes the database adds mappings of the file names its true value eg mapping SS to Author in file 'fileName'
'''
def refreshDataBase(data, fileName):
	for key in data:
		mapping = Mappings()
		mapping.TRUE_NAME = key
		mapping.FILE_NAME = data[key]
		mapping.FILE_LINK = fileName
		mapping.save()

def generateUser():
	return folderDirectory
