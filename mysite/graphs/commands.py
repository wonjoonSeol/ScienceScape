from .forms import AbstractField
from csv import DictReader
from csv import reader
import os


def handleUploadedFile(f):
    if f:
        print("File has been uploaded successfully!")
        filePath = saveFile(f)
        dictionary = processBodyIntoDictionary(filePath)      
        fields = produceAbstractFields(dictionary)
        
        return fields
        

def checkCSV(f):
    if f.name[-4:] == ".csv":
        print("File is .csv")
        return True
    else:
        print("File is not .csv")
        return False

def processBodyIntoDictionary(filePath):

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
				headerValueSets[key].add((row[key], row[key]))
	
	return headerValueSets
		
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
  
def produceAbstractFields(dictionary):
	fields = []
	
	for header in dictionary:
		fields.append(AbstractField(header, dictionary[header]))
	
	return fields