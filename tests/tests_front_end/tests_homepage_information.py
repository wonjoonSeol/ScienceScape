"""from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import TestCase

class TestHomepageInformation(TestCase):

    def test_homepage_shows_correct_information(self):
        browser_driver = webdriver.Chrome()
        browser_driver.get("http://127.0.0.1:8000/")
        self.assertIn("ScienceScape", browser_driver.page_source)
        self.assertIn("ScienceScapeS - Scientometrics, made easy", browser_driver.title)
        self.assertIn("Example Graph", browser_driver.page_source)
        browser_driver.quit()

    def test_user_sees_login_button(self):
        browser_driver2 = webdriver.Chrome()
        browser_driver2.get("http://127.0.0.1:8000/")
        page_source = browser_driver2.page_source
        self.assertIn("Log In", page_source)
        browser_driver2.quit()"""
