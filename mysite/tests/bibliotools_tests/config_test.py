import unittest
import config

class TestConfig(unittest.TestCase):

    def test_config_gen(self):
        spanYears = ["100-500", "200-600"] #arbitrary values to retrieve from dict
        config.spanYears = spanYears
        CONFIG = config.gen()
        self.assertEqual("100-500", CONFIG['spans']['span_name_0']['years'])
        self.assertEqual("200-600", CONFIG['spans']['span_name_1']['years'])

if __name__ == '__main__':
    unittest.main()
