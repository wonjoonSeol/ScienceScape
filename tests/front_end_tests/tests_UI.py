import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Sciencescape(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        #self.driver = webdriver.Firefox()

    def test_title_in_sciencescape(self):
        driver = self.driver
        #driver.get("http://127.0.0.1:8000/")
        #driver.get("https://sciencescape.herokuapp.com/")
        self.assertIn("ScienceScape", driver.title)
        assert "No results found." not in driver.page_source

    def tearDown(self):
        self.driver.quit()
        #self.driver.close() - closes the tab of the browser instead of quitting entirely

if __name__ == "__main__":
    unittest.main()
