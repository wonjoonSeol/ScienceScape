"""import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Sciencescape(unittest.TestCase):

    def setUp(self):
        ## Uses Chrome webdriver
        self.driver = webdriver.Chrome()
        ## Uses Firefox webdriver
        #self.driver = webdriver.Firefox()

    def test_title_in_sciencescape(self):
        driver = self.driver
        ## Localhost - link
        #driver.get("http://127.0.0.1:8000/")
        ## Heroku - link
        driver.get("https://sciencescape.herokuapp.com/")
        self.assertIn("ScienceScape", driver.title)
        assert "No results found." not in driver.page_source

    def tearDown(self):
        ## Quits the browser entirely
        self.driver.quit()
        ## Closes the tab of the browser instead of quitting the browser entirely
        #self.driver.close()

if __name__ == "__main__":
    unittest.main()
"""
