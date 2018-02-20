import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/")
        self.assertIn("Sciencescape beta", driver.title)
        #elem = driver.find_element_by_name("q")
        #elem.send_keys("pycon")
        #elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source


    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
