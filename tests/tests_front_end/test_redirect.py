import os
import sys
from django.test import TestCase
from graphs.commands import *
from django.test import *
from django.contrib.auth.models import User
class TestCommands(TestCase):

    """
    Tests that the domain name with no extension redirects to the home page
    """
    def test_home_page_redirection(self):
        client = Client()
        response = client.get('/', follow = True)
        #print("Redirect for homepage: " + str(response.redirect_chain))
        self.assertEqual(str(response.redirect_chain), "[]")

    """
    Tests that a wrong user redirects to the wrong user domain
    """
    def test_valid_login_redirection(self):
        client = Client()
        response = client.get('/login_on_home/', {'username': '', 'password': ''}, follow = True)
        #print("Redirect for upload: " + str(response.redirect_chain))
        self.assertEqual(response.redirect_chain, [('/upload/%20', 302)])

    """
    Tests that the graph redirection happens properly.
    """
    def test_valid_graph_redirection(self):
        client = Client()
        response = client.get('/graph/', {'username': '', 'password': ''}, follow = True)
        print("Redirect for graphs: " + str(response.redirect_chain))
        self.assertEqual(str(response.redirect_chain), "[]")

    """
    Tests that the about page yields no redirection.
    """
    def test_no_redirect_for_about(self):
        client = Client()
        response = client.get('/about/', follow = True)
        print("Redirect for About: " + str(response.redirect_chain))
        self.assertEqual(str(response.redirect_chain), "[]")

    """
    Tests that there is no upload redirection.
    """
    def test_no_redirect_for_upload(self):
        client = Client()
        response = client.get('/upload/', follow = True)
        print("Redirect for Upload: " + str(response.redirect_chain))
        self.assertEqual(str(response.redirect_chain), "[]")

    """
    Tests that creating an account redirects to the upload page.
    """
    def test_account_redirect_to_upload(self):
        client = Client()
        response = client.get('/account/', follow = True)
        print("Redirect for Account: " + str(response.redirect_chain))
        self.assertEqual(response.redirect_chain, [('/upload/%20', 302)])
