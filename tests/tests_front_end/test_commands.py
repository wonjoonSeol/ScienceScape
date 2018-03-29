import os
import sys
from django.test import TestCase
from graphs.commands import *

class TestCommands(TestCase):

    # These tests have significant set-up and tear-down costs associated with them.

    """
    This test tests that upon calling check_txt_file upon a .txt file, the correct value
    is returned representing whether the input file is a .txt or not. (Case 1: it's a txt)
    """
    def test_check_txt(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        file_to_check = open(os.path.join(dir, "a_test_file.txt"), "w")
        file_to_check.close()
        self.assertEqual(True, check_txt_file(file_to_check))
        os.remove(os.path.join(dir, "a_test_file.txt"))

    """
    This test tests that upon calling check_txt_file upon a .txt file, the correct value
    is returned representing whether the input file is a .txt or not. (Case 2: it's not a txt)
    """
    def test_check_none_txt(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        file_to_check = open(os.path.join(dir, "a_test_file.csv"), "w")
        file_to_check.close()
        self.assertEqual(False, check_txt_file(file_to_check))
        os.remove(os.path.join(dir, "a_test_file.csv"))

    """
    This test checks that calling remove_zero_whitespace_character correctly removes
    whitespaces from an input string.
    """
    def test_remove_zero_whitespace_characters(self):
        string_with_zwc = u"\ufeff" + "abc"
        result = remove_zero_whitespace_character(string_with_zwc)
        self.assertEqual(result, "abc")

    """
    This test checks that calling make_header_sets returns the correct number of sets.
    """
    def test_make_header_sets_returns_right_number_of_sets(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        file_to_check = open(os.path.join(dir, "a_test_file.txt"), "w")
        file_to_check.write("Header1\tHeader2\tHeader3")
        file_to_check.close()
        returned_sets = make_header_sets(os.path.join(dir, "a_test_file.txt"))
        os.remove(os.path.join(dir, "a_test_file.txt"))
        self.assertEqual(len(returned_sets), 3)

    """
    This test checks that calling make_header_sets correctly creates a set of headers
    from an input file.
    """
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

    """
    This test checks that calling populate_dictionary correctly sets up and populates
    the header->value dictionary.
    """
    def test_populate_dictionary(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        file_to_check = open(os.path.join(dir, "a_test_file.txt"), "w")
        file_to_check.write("Header1\tHeader2\tHeader3\nValue1\tValue2\tValue3")
        file_to_check.close()
        sets = make_header_sets(os.path.join(dir, "a_test_file.txt"))
        returned_dictionary = populate_dictionary(sets, os.path.join(dir, "a_test_file.txt"))
        os.remove(os.path.join(dir, "a_test_file.txt"))
        self.assertEqual(True, 'Value1' in returned_dictionary['Header1'] and 'Value3' in returned_dictionary['Header3'])

    """
    This test checks that calling make_user_folders for a particular input username

    executes correctly and creates the specified directory, tearing it down afterwards.
    """
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

    """
    This test checks that a get_all_user_files call with no folder associated with the input
    username returns an empty list.
    """
    def test_get_all_user_files_for_no_folder(self):
        returned_files = get_all_user_files("test_user_2")
        self.assertEqual(returned_files, [])

    """
    This test checks that the returned files for a get_all_user_files call on an empty folder
    returns an empty list.
    """
    def test_get_all_user_files_for_empty_folder(self):
        make_user_folders("test_user_3")
        dir = os.path.abspath(os.path.join(__file__, '..', '..', '..'))
        if not os.path.exists(os.path.join(dir, "static/userFiles/test_user_3")):
            os.mkdir(os.path.join(dir, "static/userFiles/test_user_3"))
        returned_files = get_all_user_files("test_user_3")
        self.assertEqual(returned_files, [])
        if os.path.exists(os.path.join(dir, "static/userFiles/test_user_3")):
            os.rmdir(os.path.join(dir, "static/userFiles/test_user_3"))

    """
    This test checks that the returned files for a get_all_user_files call for a folder
    with one file returns just one, specific file.
    """
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

    """
    This test checks that the bibliotools ignition command is properly generated by the script.
    This is very important for results accuracy and critical to debugging errors. (Case 1: no headers provided)
    """
    def test_generate_bibliotools_command_with_no_header_parameters(self):
        expected_command = "python3 bibliotools3/scripts/graph_gen.py -user User1 -bound 1998-2018"
        self.assertEqual(generate_bibliotools_launch_command("User1", 1998, 2018, ""), expected_command)

    """
    This test checks that the bibliotools ignition command is properly generated by the script.
    This is very important for results accuracy and critical to debugging errors (Case 2: headers provided)
    """
    def test_generate_bibliotools_command_with_some_header_parameters(self):
        headers_as_string = "UT-AU-DE-ID-TI-AB-CR-C1-PY-J9-VL-BP-DI-AB-DT-TC"
        expected_command = "python3 bibliotools3/scripts/graph_gen.py -user User1 -bound 1998-2018 -headers " + headers_as_string
        self.assertEqual(generate_bibliotools_launch_command("User1", 1998, 2018, headers_as_string), expected_command)

    """
    This test tests that the bibliotools environment is properly recreated by the front end
    Case 1: No folder exists in the user folder.
    """
    def test_reproduce_bibliotools_environment_when_no_folder_exists(self):
        # Mock a user folder, and run test.
        user_files_folder = "tests/tests_front_end/test_user_5"
        os.mkdir(os.path.join(user_files_folder))
        reproduce_bibliotools_environment_in(user_files_folder, "../savedrecs.txt")
        result = True
        if not os.path.exists(os.path.join(user_files_folder, 'data-wos')):
            result = False
        if not os.path.exists(os.path.join(user_files_folder, 'Result')):
            result = False
        if not os.path.exists(os.path.join(user_files_folder, 'data-wos', 'savedrecs.txt')):
            result = False
        shutil.rmtree('tests/tests_front_end/test_user_5')
        self.assertEqual(True, result)

    """
    This test tests that the bibliotools environment is properly recreated by the front end
    Case 2: Only a data-wos folder exists in the user folder.
    """
    def test_reproduce_bibliotools_environment_when_datawos_folder_exists(self):
        # Mock a user folder, and run test.
        user_files_folder = "tests/tests_front_end/test_user_5"
        os.mkdir(os.path.join(user_files_folder))
        os.mkdir(os.path.join(user_files_folder, 'data-wos'))
        reproduce_bibliotools_environment_in(user_files_folder, "../savedrecs.txt")
        result = True
        if not os.path.exists(os.path.join(user_files_folder, 'data-wos')):
            result = False
        if not os.path.exists(os.path.join(user_files_folder, 'Result')):
            result = False
        if not os.path.exists(os.path.join(user_files_folder, 'data-wos', 'savedrecs.txt')):
            result = False
        shutil.rmtree('tests/tests_front_end/test_user_5')
        self.assertEqual(True, result)

    """
    This test tests that the bibliotools environment is properly recreated by the front end
    Case 3: Only a Results folder exists in the user folder.
    """
    def test_reproduce_bibliotools_environment_when_result_folder_exists(self):
        # Mock a user folder, and run test.
        user_files_folder = "tests/tests_front_end/test_user_5"
        os.mkdir(os.path.join(user_files_folder))
        os.mkdir(os.path.join(user_files_folder, 'Result'))
        reproduce_bibliotools_environment_in(user_files_folder, "../savedrecs.txt")
        result = True
        if not os.path.exists(os.path.join(user_files_folder, 'data-wos')):
            result = False
        if not os.path.exists(os.path.join(user_files_folder, 'Result')):
            result = False
        if not os.path.exists(os.path.join(user_files_folder, 'data-wos', 'savedrecs.txt')):
            result = False
        shutil.rmtree('tests/tests_front_end/test_user_5')
        self.assertEqual(True, result)

    """
    This test tests that the bibliotools environment is properly recreated by the front end
    Case 4: Both data-wos and Result exist in the user folder
    """
    def test_reproduce_bibliotools_environment_when_result_folder_exists(self):
        # Mock a user folder, and run test.
        user_files_folder = "tests/tests_front_end/test_user_5"
        os.mkdir(os.path.join(user_files_folder))
        os.mkdir(os.path.join(user_files_folder, 'data-wos'))
        os.mkdir(os.path.join(user_files_folder, 'Result'))
        reproduce_bibliotools_environment_in(user_files_folder, "../savedrecs.txt")
        result = True
        if not os.path.exists(os.path.join(user_files_folder, 'data-wos')):
            result = False
        if not os.path.exists(os.path.join(user_files_folder, 'Result')):
            result = False
        if not os.path.exists(os.path.join(user_files_folder, 'data-wos', 'savedrecs.txt')):
            result = False
        shutil.rmtree('tests/tests_front_end/test_user_5')
        self.assertEqual(True, result)

    """
    This test tests that a string of headers is properly constructed.
    """
    def test_construct_string_of_headers(self):
        input_dictionary = {"Header1" : 'H1', "Header2" : 'H2'}
        output = construct_string_of_headers(input_dictionary)
        self.assertEqual(output, 'H1-H2')

    def test_graph_collection(self):
        user_files_folder = "tests/tests_front_end/test_user_5"
        os.mkdir(os.path.join(user_files_folder))
        reproduce_bibliotools_environment_in(user_files_folder, "../savedrecs.txt")
        os.mkdir(os.path.join(user_files_folder, "Result", "parsed_data"))
        os.mkdir(os.path.join(user_files_folder, "Result", "parsed_data", "span_name_0"))
        open(os.path.join(user_files_folder, "Result", "parsed_data", "span_name_0", "span_name_0.gexf"), "w")

        output = get_produced_graph_path(os.path.join(user_files_folder, "Result"), "parsed_data")
        shutil.rmtree('tests/tests_front_end/test_user_5')
        self.assertEqual(str(output), "['tests/tests_front_end/test_user_5/Result/parsed_data/span_name_0/span_name_0.gexf']")
