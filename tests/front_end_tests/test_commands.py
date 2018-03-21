import os
import sys
from django.test import TestCase
from graphs.commands import *

class TestCommands(TestCase):

    """
    This test tests that upon calling ...
    """
    def test_check_txt(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        file_to_check = open(os.path.join(dir, "a_test_file.txt"), "w")
        file_to_check.close()
        self.assertEqual(True, checkTXT(file_to_check))
        os.remove(os.path.join(dir, "a_test_file.txt"))
