import os
import sys
from django.test import TestCase

lib_path = os.path.abspath(os.path.join(__file__, '..', '..', '..', 'graphs'))
sys.path.append(lib_path)

from commands import *

class DatabaseTestCase(TestCase):

    def test_form_data_is_stored_in_database(self):
    	fPath = "TESTFILEPATH"
    	keyValuePair = dict(Key1 = "Value1", Key2 = "Value1", Key3 = "Value1", Key4 = "Value1", Key5 = "Value1")

    	refresh_database(keyValuePair, fPath)

    	mapping = Mappings.objects.filter(FILE_LINK = fPath)
    	dictionary = dict()

        result = False

    	if mapping:
    		for k in mapping:
    			dictionary[k.TRUE_NAME] = k.FILE_NAME
    		if dictionary == keyValuePair:
    			mapping.delete()
    			result = True
    		else:
    			mapping.delete()

        assertEqual(True, result)

    def test_data_is_retrievable(self):
    	keyValuePair = dict(Key1="Value1", Key2="Value1", Key3="Value1", Key4="Value1", Key5="Value1")
    	fPath = "TESTPATH"
    	refresh_database(keyValuePair, fPath)
    	retrieval = retrieveFromDataBase(fPath)
        result = False

    	if retrieval == keyValuePair:
    		mapping = Mappings.objects.filter(FILE_LINK = fPath)
    		mapping.delete()
    		result = True
    	else:
    		mapping = Mappings.objects.filter(FILE_LINK = fPath)
    		mapping.delete()
        assertEqual(True, result)

    def test_database_resets(self):
    	mappings = Mappings.objects.all()
        result = False
    	if mappings:
    		resetDatabase()
    		if not Mappings.objects.all():
                result = True
        assertEqual(True, result)
