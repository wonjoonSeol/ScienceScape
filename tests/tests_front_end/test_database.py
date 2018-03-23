import os
import sys
from django.test import TestCase

from graphs.commands import *

class DatabaseTestCase(TestCase):

    """
    This test verifies that the data is correctly stored in the database.
    """
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

        self.assertEqual(True, result)

    """
    This test tests that the data is retrievable from the database and is not corrupted.
    """
    def test_data_is_retrievable(self):
        keyValuePair = dict(Key1="Value1", Key2="Value1", Key3="Value1", Key4="Value1", Key5="Value1")
        fPath = "TESTPATH"
        refresh_database(keyValuePair, fPath)
        retrieval = retrieve_from_database(fPath)
        result = False

        if retrieval == keyValuePair:
            mapping = Mappings.objects.filter(FILE_LINK = fPath)
            mapping.delete()
            result = True
        else:
            mapping = Mappings.objects.filter(FILE_LINK = fPath)
            mapping.delete()
        self.assertEqual(True, result)

    """
    This test tests that upon calling the custom method resetDatabase(),
    the database is emptied and contains no data.
    """
    def test_database_resets(self):
        mappings = Mappings.objects.all()
        keyValuePair = dict(Key1="Value1", Key2="Value1", Key3="Value1", Key4="Value1", Key5="Value1")
        fPath = "TESTPATH"
        refresh_database(keyValuePair, fPath)

        result = False
        if mappings:
            resetDatabase()
            if not Mappings.objects.all():
                result = True
        self.assertEqual(True, result)
