import os
import sys
from django.test import *
from graphs.forms import *
APP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class FormModelTest(TestCase):

    def test_produce_form_set_with_no_values(self):
        dictionary = dict(accession_number = "UT", authors = "AU", author_keywords = "DE", keywords_plus = "ID", document_title = "TI", wos_categories = "EC", cited_references = "CR", author_address = "C1", year_published = "PY", twenty_nine_character_source_abbreviation = "J9",
        volume = "VL", beginning_page = "BP", doi = "DI",
        publication_type = "PT", document_type = "DT", wos_core_collection_times_cited = "TC")
        headers = ['UT','AU','DE','ID','TI','EC','CR','C1','PY','J9','VL','BP','DI','PT','DT','TC']
        unknown = []

        for i in headers:
            unknown.append((i,i))

        form = formset_factory(create_mini_form(sorted(unknown)), extra=0)
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
        result = {'form' : finalForm, 'count' : 16}

        self.assertEqual(result['count'], produce_form_set(headers)['count'])

    def test_create_mini_form_no_choice(self):
        choicesInField = [("DEFAULT", "Select a value")]
        self.assertEqual(choicesInField, create_mini_form().choicesInField)

    def test_create_mini_form_with_choice(self):
        choices = [("TEST", "Select a value")]
        self.assertEqual(choices, create_mini_form(choices).choicesInField)

    def test_mini_form_with_request(self):
        client = Client()
        with open(os.path.join(APP_DIR ,'tests','tests_front_end','savedrecs.txt')) as file_path:
            response = client.post('/upload/', {'file': file_path}, follow = True)
            choices= [("TEST", "Select a value")]
            self.assertEqual(choices, create_mini_form(choices, response).choicesInField)
