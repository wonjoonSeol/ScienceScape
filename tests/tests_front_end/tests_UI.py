"""from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import TestCase
from django.contrib.auth.models import User

class TestUI(TestCase):

    def test_login_with_unregistered_credentials(self):
        browser_driver = webdriver.Chrome()
        browser_driver.get("http://127.0.0.1:8000/")

        login_collapsible = browser_driver.find_element_by_xpath("/html/body/div[4]/div[3]/ul/li[1]/div[1]/i")
        login_collapsible.click()

        username_field = browser_driver.find_element_by_xpath('//*[@id="login-username"]')
        username_field.send_keys("myusername")
        password_field = browser_driver.find_element_by_xpath('//*[@id="login-password"]')
        password_field.send_keys("mypassword")
        submit_button = browser_driver.find_element_by_xpath('/html/body/div[4]/div[3]/ul/li[1]/div[2]/div/form/button')
        submit_button.click()
        self.assertIn("Incorrect credentials", browser_driver.page_source)

        register_collapsible = browser_driver.find_element_by_xpath("/html/body/div[4]/div[3]/ul/li[2]/div[1]")
        register_collapsible.click()
        username_field = browser_driver.find_element_by_xpath('//*[@id="id_username"]')
        username_field.send_keys("avalidusername2")
        email_field = browser_driver.find_element_by_xpath('//*[@id="id_email"]')
        email_field.send_keys("email@email.abc2")
        password_field = browser_driver.find_element_by_xpath('//*[@id="id_password"]')
        password_field.send_keys("itsasecret2")
        submit_button = browser_driver.find_element_by_xpath('/html/body/div[4]/div[3]/ul/li[2]/div[2]/div/form/button')
        submit_button.click()
        self.assertIn("are logged in as", browser_driver.page_source)
        browser_driver.quit()

    def test_registration_when_user_already_exists(self):
        browser_driver = webdriver.Chrome()
        browser_driver.get("http://127.0.0.1:8000/")
        register_collapsible = browser_driver.find_element_by_xpath("/html/body/div[4]/div[3]/ul/li[2]/div[1]")
        register_collapsible.click()
        username_field = browser_driver.find_element_by_xpath('//*[@id="id_username"]')
        username_field.send_keys("avalidusername")
        email_field = browser_driver.find_element_by_xpath('//*[@id="id_email"]')
        email_field.send_keys("email@email.abc")
        password_field = browser_driver.find_element_by_xpath('//*[@id="id_password"]')
        password_field.send_keys("itsasecret")
        submit_button = browser_driver.find_element_by_xpath('/html/body/div[4]/div[3]/ul/li[2]/div[2]/div/form/button')
        submit_button.click()
        self.assertIn("already exists", browser_driver.page_source)
        browser_driver.quit()

    def test_registration_and_login_for_new_user(self):
        browser_driver = webdriver.Chrome()
        browser_driver.get("http://127.0.0.1:8000/")
        register_collapsible = browser_driver.find_element_by_xpath("/html/body/div[4]/div[3]/ul/li[2]/div[1]")
        register_collapsible.click()
        username_field = browser_driver.find_element_by_xpath('//*[@id="id_username"]')
        username_field.send_keys("avalidusername")
        email_field = browser_driver.find_element_by_xpath('//*[@id="id_email"]')
        email_field.send_keys("email@email.abc")
        password_field = browser_driver.find_element_by_xpath('//*[@id="id_password"]')
        password_field.send_keys("itsasecret")
        submit_button = browser_driver.find_element_by_xpath('/html/body/div[4]/div[3]/ul/li[2]/div[2]/div/form/button')
        submit_button.click()
        self.assertIn("are logged in as", browser_driver.page_source)
        browser_driver.quit()"""
