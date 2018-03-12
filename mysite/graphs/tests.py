from django.test import TestCase
from .commands import *
# Create your tests here.

def attemptDatabaseTest():
	if isFormDataStoredInDatabase():
		isDataRetrievable()

	#doesDatabaseReset()

def isFormDataStoredInDatabase():
	fPath = "TESTFILEPATH"
	keyValuePair = dict(Key1="Value1", Key2="Value1", Key3="Value1", Key4="Value1", Key5="Value1")

	refreshDataBase(keyValuePair, fPath)

	mapping = Mappings.objects.filter(FILE_LINK = fPath)
	dictionary = dict()
	if mapping:
		for k in mapping:
			dictionary[k.TRUE_NAME] = k.FILE_NAME
		if dictionary == keyValuePair:
			mapping.delete()
			print("Data store passed.")
			return True
		else:
			print("Data store failed. Data was stored but not in the correct format")
			mapping.delete()
			return False
	else:
		print("Data store failed. Data was not stored at all")
		return False


def isDataRetrievable():
	keyValuePair = dict(Key1="Value1", Key2="Value1", Key3="Value1", Key4="Value1", Key5="Value1")
	fPath = "TESTPATH"
	refreshDataBase(keyValuePair, fPath)
	retrieval = retrieveFromDataBase(fPath)
	if retrieval == keyValuePair:
		print("Data retrieval passed")
		mapping = Mappings.objects.filter(FILE_LINK = fPath)
		mapping.delete()
		return True
	else:
		print("Data retrieval failed")
		mapping = Mappings.objects.filter(FILE_LINK = fPath)
		mapping.delete()
		return False


def doesDatabaseReset():
	mappings = Mappings.objects.all()
	if mappings:
		resetDatabase()
		if Mappings.objects.all():
			print("Database reset failed as there are still Mapping objects in the Database.")
			return False
		else:
			print("Database reset passed.")
			return True
	else:
		print("Cannot perform test on empty Database.")
		return None


def testLoadFilesForUser(name = "saadman"):
	APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	folder = os.path.join(APP_DIR, "static/userFiles/{x}".format(x = name))
	files = getAllFilesForUser(folder)
	for f in files:
		print(f)
