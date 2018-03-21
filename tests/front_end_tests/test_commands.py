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
        self.assertEqual(True, check_txt_file(file_to_check))
        os.remove(os.path.join(dir, "a_test_file.txt"))

    def test_remove_zero_whitespace_characters(self):
        string_with_zwc = u"\ufeff" + "abc"
        result = remove_zero_whitespace_character(string_with_zwc)
        self.assertEqual(result, "abc")

    def test_make_header_sets_returns_right_number_of_sets(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        file_to_check = open(os.path.join(dir, "a_test_file.txt"), "w")
        file_to_check.write("Header1\tHeader2\tHeader3")
        file_to_check.close()
        returned_sets = make_header_sets(os.path.join(dir, "a_test_file.txt"))
        os.remove(os.path.join(dir, "a_test_file.txt"))
        self.assertEqual(len(returned_sets), 3)

    def test_make_header_sets_returns_sets(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        file_to_check = open(os.path.join(dir, "a_test_file.txt"), "w")
        file_to_check.write("Header1\tHeader2\tHeader3")
        file_to_check.close()
        returned_sets = make_header_sets(os.path.join(dir, "a_test_file.txt"))
        os.remove(os.path.join(dir, "a_test_file.txt"))
        all_sets = True
        for key in returned_sets:
            if not str(returned_sets[key]) == 'set()':
                all_sets = False
        self.assertEqual(True, all_sets)

    def test_populate_dictionary(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        file_to_check = open(os.path.join(dir, "a_test_file.txt"), "w")
        file_to_check.write("Header1\tHeader2\tHeader3\nValue1\tValue2\tValue3")
        file_to_check.close()
        sets = make_header_sets(os.path.join(dir, "a_test_file.txt"))
        returned_dictionary = populate_dictionary(sets, os.path.join(dir, "a_test_file.txt"))
        os.remove(os.path.join(dir, "a_test_file.txt"))
        self.assertEqual(True, 'Value1' in returned_dictionary['Header1'] and 'Value3' in returned_dictionary['Header3'])

    def test_make_user_folders(self):
        username = "test_user"
        returned_user_file_folder = make_user_folders(username)
        self.assertEqual(returned_user_file_folder, "static/userFiles/test_user")
        dir = os.path.abspath(os.path.join(__file__, '..', '..', '..'))
        result = False
        if os.path.exists(os.path.join(dir, returned_user_file_folder)):
            result = True
            os.rmdir(os.path.join(dir, returned_user_file_folder))
        self.assertEqual(True, result)

    def test_get_all_user_files_for_no_folder(self):
        returned_files = get_all_user_files("test_user_2")
        self.assertEqual(returned_files, [])

    def test_get_all_user_files_for_empty_folder(self):
        make_user_folders("test_user_3")
        dir = os.path.abspath(os.path.join(__file__, '..', '..', '..'))
        if not os.path.exists(os.path.join(dir, "static/userFiles/test_user_3")):
            os.mkdir(os.path.join(dir, "static/userFiles/test_user_3"))
        returned_files = get_all_user_files("test_user_3")
        self.assertEqual(returned_files, [])
        if os.path.exists(os.path.join(dir, "static/userFiles/test_user_3")):
            os.rmdir(os.path.join(dir, "static/userFiles/test_user_3"))


    def test_get_all_user_files_for_folder_with_one_file(self):
        make_user_folders("test_user_4")
        dir = os.path.abspath(os.path.join(__file__, '..', '..', '..'))
        if not os.path.exists(os.path.join(dir, "static/userFiles/test_user_4")):
            os.mkdir(os.path.join(dir, "static/userFiles/test_user_4"))
        file_to_check = open(os.path.join(dir, "static/userFiles/test_user_4", "a_test_file.txt"), "w")
        file_to_check.write("Some text")
        file_to_check.close()

        returned_files = get_all_user_files("test_user_4")
        print("DIRECTORY " + str(dir))
        self.assertEqual(str(returned_files), "['a_test_file.txt']")
        os.remove(os.path.join(dir, "static/userFiles/test_user_4", "a_test_file.txt"))
        os.rmdir(os.path.join(dir, "static/userFiles/test_user_4"))
