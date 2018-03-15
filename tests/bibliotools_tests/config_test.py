import unittest
import sys
import os

lib_path = os.path.abspath(os.path.join(__file__, '..', '..', '..', 'bibliotools3.0', 'scripts'))
sys.path.append(lib_path)

import config

class TestConfig(unittest.TestCase):

    """
    This test tests that the config.py script file generates time spans properly.
    """
    def test_config_gen(self):
        spanYears = [[100,500], [200,600]] #arbitrary values to retrieve from dict
        config.spanYears = spanYears
        CONFIG = config.gen()
        self.assertEqual([100,500], CONFIG['spans']['span_name_0']['years'])
        self.assertEqual([200,600], CONFIG['spans']['span_name_1']['years'])

if __name__ == '__main__':
    unittest.main()
