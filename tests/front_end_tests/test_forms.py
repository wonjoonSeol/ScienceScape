import os
import sys
from django.test import TestCase
from graphs.commands import *
from django.test import *
from django.contrib.auth.models import User
APP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestCommands(TestCase):

    """
    Test that .txt file is accepted by the upload form and submission redirects to the field page when not logged in.
    """
    def test_upload_forms(self):
        client = Client()
        with open(os.path.join(APP_DIR ,'tests','front_end_tests','savedrecs.txt')) as file_path:
            response = client.post('/upload/', {'file': file_path}, follow = True)
        self.assertRedirects(response, "/addFields/{directory}".format(directory = str(os.path.join(APP_DIR ,'static','userFiles','Public','savedrecs.txt')).replace(" ",'%20')))
        
    """
    Test that .txt file is accepted by the upload form and submission redirects to the field page when logged in as a user.
    """
    def test_upload_forms_for_logged_in_user(self):
        client = Client()
        User.objects.create_user('temp', 'temp@temp.com','temp')
        client.login(username='temp', password='temp')
       
        with open(os.path.join(APP_DIR ,'tests','front_end_tests','savedrecs.txt')) as file_path:
            response = client.post('/upload/', {'file': file_path}, follow = True)
        self.assertRedirects(response, "/addFields/{directory}".format(directory = str(os.path.join(APP_DIR ,'static','userFiles','temp','savedrecs.txt')).replace(" ",'%20')))
        
    """
    Tests that the correct values are displayed in the drop down menu for the field forms
    """
    def test_correct_fields_are_displayed_to_user(self):
        client = Client()
        User.objects.create_user('temp', 'temp@temp.com','temp')
        client.login(username='temp', password='temp')
       
        with open(os.path.join(APP_DIR ,'tests','front_end_tests','savedrecs.txt')) as file_path:
            response = client.post('/upload/', {'file': file_path}, follow = True)
            
            default_headers = ['UT', 'AU', 'DE', 'ID', 'TI', 'WC', 'CR', 'C1', 'PY', 'J9', 'VL', 'BP', 'DI', 'PT', 'DT', 'TC']
            headers_in_content = []
            
            for header in default_headers:
                if str(response.content).find(str(header)) > 0:
                    headers_in_content.append(header)
                    
            self.assertEqual(default_headers, headers_in_content)
   
    '''
    Tests that a blank field name in the field forms produces an error message to the user
    '''
    def test_incomplete_field_definitions_display_error_message(self):
        client = Client()
        User.objects.create_user('temp', 'temp@temp.com','temp')
        client.login(username='temp', password='temp')
       
        with open(os.path.join(APP_DIR ,'tests','front_end_tests','savedrecs.txt')) as file_path:
            response = client.post('/upload/', {'file': file_path}, follow = True)
            submission_response = client.post("/addFields/{directory}".format(directory = str(os.path.join(APP_DIR ,'static','userFiles','temp','savedrecs.txt')).replace(" ",'%20')), {'form-1-Name' : ''})
            self.assertEqual(True, str(submission_response.content).find('Not all fields have been defined') > 0)   


        