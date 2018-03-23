from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import TestCase

class TestUI(TestCase):

    def test_homepage(self):
        self.browser_driver = webdriver.Chrome()
        self.browser_driver.get("http://127.0.0.1:8000/")
        self.assertIn("ScienceScape", self.browser_driver.page_source)
        self.browser_driver.quit()
