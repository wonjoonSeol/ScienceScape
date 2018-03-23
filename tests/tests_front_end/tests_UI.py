from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import TestCase

class TestUI(TestCase):

    def test_homepage_shows_correct_information(self):
        browser_driver = webdriver.Chrome()
        browser_driver.get("http://127.0.0.1:8000/")
        self.assertIn("ScienceScape", browser_driver.page_source)
        self.assertIn("ScienceScapeS - Scientometrics, made easy", browser_driver.title)
        self.assertIn("Example Graph", browser_driver.page_source)
        browser_driver.quit()

    def test_user_sees_login_button(self):
        browser_driver = webdriver.Chrome()
        browser_driver.get("http://127.0.0.1:8000/")
        page_source = browser_driver.page_source
        self.assertIn("Log In", page_source)
        browser_driver.quit()

    def test_login_with_unregistered_credentials(self):
        browser_driver = webdriver.Chrome()
        browser_driver.get("http://127.0.0.1:8000/")
        login_collapsible = browser_driver.find_element_by_xpath("/html/body/div[4]/div[3]/ul/li[1]/div[1]/i")
        login_collapsible.click()
        username_field = browser_driver.find_element_by_xpath("""//*[@id="login-username"]""")
        username_field.send_keys("myusername")
        password_field = browser_driver.find_element_by_xpath("""//*[@id="login-password"]""")
        password_field.send_keys("mypassword")
        submit_button = browser_driver.find_element_by_xpath("""/html/body/div[4]/div[3]/ul/li[1]/div[2]/div/form/button""")
        submit_button.click()
        self.assertIn("Incorrect credentials", browser_driver.page_source)
        browser_driver.quit()
