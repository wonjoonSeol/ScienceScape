from django.test import TestCase
import sys
import os

lib_path = os.path.abspath(os.path.join(__file__, '..', '..', '..', 'bibliotools3.0', 'scripts'))
sys.path.append(lib_path)

import config

class TestConfig(TestCase):

    """
    This test tests that the config.py script file generates time spans properly.
    """
    def test_config_gen(self):
        test_user = 'test_user' #arbitrary user
        default_headers = ['UT', 'AU', 'DE', 'ID', 'TI', 'WC', 'CR', 'C1', 'PY', 'J9', 'VL', 'BP', 'DI', 'PT', 'DT', 'TC']
        spanYears = [[100,500], [200,600]] #arbitrary values to retrieve from dict
        config.spanYears = spanYears

        #Test with user for the website
        CONFIG = config.gen(test_user, default_headers)
        self.assertEqual([100,500], CONFIG['spans']['span_name_0']['years'])
        self.assertEqual([200,600], CONFIG['spans']['span_name_1']['years'])

        #Test locally for the scripts only (trigerred when the user is a blank space)
        CONFIG = config.gen(' ', default_headers)
        self.assertEqual([100, 500], CONFIG['spans']['span_name_0']['years'])
        self.assertEqual([200,600], CONFIG['spans']['span_name_1']['years'])
