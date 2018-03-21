import os
import sys
from django.test import TestCase
from graphs.commands import *
from django.test import *
from django.contrib.auth.models import User
class TestCommands(TestCase):

    """
    Test that the domain name with no extension redirects to the home page
    """
    def test_home_page_redirection(self):
        client = Client()
        response = client.get('/', follow = True)
        print("Redirect for homepage: " + str(response.redirect_chain))
        self.assertEqual(str(response.redirect_chain), "[]")
    
    """
    Test that a wrong user redirects to the wrong user domain
    """
    def test_valid_login_redirection(self):
        client = Client()
        response = client.get('/login_on_home/', {'username': '', 'password':''}, follow = True)
        print("Redirect for upload: " + str(response.redirect_chain))
        self.assertEqual(response.redirect_chain, [('/upload/%20', 302)])
       
    '''
    Test that a logged in user can see there previously uploaded files
    '''
    def test_logged_in_user_views_uploaded_table(self):
        client = Client()
        User.objects.create_user('temp', 'temp@temp.com','temp')
        client.login(username='temp', password='temp')
        response = client.get('/upload', follow = True)
        self.assertEqual(True, str(response.content).find('Uploaded Files') > 1 )