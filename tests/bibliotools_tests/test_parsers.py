from django.test import TestCase
import sys
import os
import glob

lib_path = os.path.abspath(os.path.join(__file__, '..', '..', '..', 'bibliotools3.0', 'scripts'))
sys.path.append(lib_path)

import config
import parsers

class TestParsers(TestCase):

    """
    These tests assess the ability of parsers.py to parse a test input and
    separate the information into different categories.

    These test wos_parser, which tests all the units in the parsers.py file.
    """

    dir = os.path.dirname(os.path.dirname(__file__))
    CONFIG = config.gen('test_user')
    parsers.CONFIG = CONFIG
    parsers.initHeaders()
    os.mkdir(os.path.join(dir, "bibliotools_tests/testFiles/parser_tests/test_output"))
    test_input_txt = open(os.path.join(dir, "bibliotools_tests/testFiles/parser_tests/input_parser.txt"), "r")
    parsers.wos_parser(os.path.join(dir, "bibliotools_tests/testFiles/parser_tests"), os.path.join(dir, "bibliotools_tests/testFiles/parser_tests/test_output"), False)
    test_input_txt.close()

    """
    This test tests that after parsing articles, the output is correct with respects
    to a known-correct base folder FOR ARTICLES.
    """
    def test_parse_articles(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.join(dir, "bibliotools_tests/testFiles/parser_tests/test_output/articles.dat"), "r") as myfile:
            output = myfile.read().replace("\n", "")

        with open(os.path.join(dir, "bibliotools_tests/testFiles/parser_tests/desired_output/articles.dat"), "r") as myfile:
            desired_output = myfile.read().replace("\n", "")

        self.assertEqual(output, desired_output)

    """
    This test tests that after parsing articles, the output is correct with respects
    to a known-correct base folder FOR AUTHORS.
    """
    def test_parse_authors(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.join(dir, "bibliotools_tests/testFiles/parser_tests/test_output/authors.dat"), "r") as myfile:
            output = myfile.read().replace("\n", "")

        with open(os.path.join(dir, "bibliotools_tests/testFiles/parser_tests/desired_output/authors.dat"), "r") as myfile:
            desired_output = myfile.read().replace("\n", "")

        self.assertEqual(output, desired_output)

    """
    This test tests that after parsing articles, the output is correct with respects
    to a known-correct base folder FOR COUNTRIES.
    """
    def test_parse_countries(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.join(dir, "bibliotools_tests/testFiles/parser_tests/test_output/countries.dat"), "r") as myfile:
            output = myfile.read().replace("\n", "")

        with open(os.path.join(dir, "bibliotools_tests/testFiles/parser_tests/desired_output/countries.dat"), "r") as myfile:
            desired_output = myfile.read().replace("\n", "")

        self.assertEqual(output, desired_output)

    """
    This test tests that after parsing articles, the output is correct with respects
    to a known-correct base folder FOR ARTICLE KEYWORDS.
    """
    def test_parse_article_keywords(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.join(dir, "bibliotools_tests/testFiles/parser_tests/test_output/article_keywords.dat"), "r") as myfile:
            output = myfile.read().replace("\n", "")

        with open(os.path.join(dir, "bibliotools_tests/testFiles/parser_tests/desired_output/article_keywords.dat"), "r") as myfile:
            desired_output = myfile.read().replace("\n", "")

        self.assertEqual(output, desired_output)

    """
    This test tests that after parsing articles, the output is correct with respects
    to a known-correct base folder FOR INSTITUTIONS.
    """
    def test_parse_institutions(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.join(dir, "bibliotools_tests/testFiles/parser_tests/test_output/institutions.dat"), "r") as myfile:
            output = myfile.read().replace("\n", "")

        with open(os.path.join(dir, "bibliotools_tests/testFiles/parser_tests/desired_output/institutions.dat"), "r") as myfile:
            desired_output = myfile.read().replace("\n", "")

        self.assertEqual(output, desired_output)

    """
    This test tests meticulously the output .dat files to ensure they are not corrupted.
    """
    def test_open_dat_files(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        os.makedirs(os.path.join(dir, "bibliotools_tests/testFiles/test_open_dat_files_folder"))
        output_dir = os.path.join(dir, "bibliotools_tests/testFiles/test_open_dat_files_folder")
        open_files = parsers.open_dat_files(output_dir)

        for file_key in open_files:
            open_files[file_key].close()

        no_of_files_created = len(glob.glob("%s/*.dat" % output_dir))

        if os.path.exists(os.path.dirname(os.path.join(dir, "bibliotools_tests/testFiles/test_open_dat_files_folder/article_keywords.dat"))):
            os.remove(os.path.join(dir, "bibliotools_tests/testFiles/test_open_dat_files_folder/article_keywords.dat"))
            os.remove(os.path.join(dir, "bibliotools_tests/testFiles/test_open_dat_files_folder/articles.dat"))
            os.remove(os.path.join(dir, "bibliotools_tests/testFiles/test_open_dat_files_folder/authors.dat"))
            os.remove(os.path.join(dir, "bibliotools_tests/testFiles/test_open_dat_files_folder/countries.dat"))
            os.remove(os.path.join(dir, "bibliotools_tests/testFiles/test_open_dat_files_folder/institutions.dat"))
            os.remove(os.path.join(dir, "bibliotools_tests/testFiles/test_open_dat_files_folder/isi_keywords.dat"))
            os.remove(os.path.join(dir, "bibliotools_tests/testFiles/test_open_dat_files_folder/references.dat"))
            os.remove(os.path.join(dir, "bibliotools_tests/testFiles/test_open_dat_files_folder/subjects.dat"))
            os.remove(os.path.join(dir, "bibliotools_tests/testFiles/test_open_dat_files_folder/title_keywords.dat"))

        if os.path.exists(os.path.dirname(os.path.join(dir, "bibliotools_tests/testFiles/test_open_dat_files_folder"))):
            os.rmdir(os.path.join(dir, "bibliotools_tests/testFiles/test_open_dat_files_folder"))

        self.assertEqual(no_of_files_created, 9)

    """
    This is a test teardown that closes and removes any open/useless files.
    """
    def test_teardown(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        if os.path.exists(os.path.dirname(os.path.join(dir, "bibliotools_tests/testFiles/parser_tests/test_output/article_keywords.dat"))):
            os.remove(os.path.join(dir, "bibliotools_tests/testFiles/parser_tests/test_output/article_keywords.dat"))
            os.remove(os.path.join(dir, "bibliotools_tests/testFiles/parser_tests/test_output/articles.dat"))
            os.remove(os.path.join(dir, "bibliotools_tests/testFiles/parser_tests/test_output/authors.dat"))
            os.remove(os.path.join(dir, "bibliotools_tests/testFiles/parser_tests/test_output/countries.dat"))
            os.remove(os.path.join(dir, "bibliotools_tests/testFiles/parser_tests/test_output/institutions.dat"))
            os.remove(os.path.join(dir, "bibliotools_tests/testFiles/parser_tests/test_output/isi_keywords.dat"))
            os.remove(os.path.join(dir, "bibliotools_tests/testFiles/parser_tests/test_output/references.dat"))
            os.remove(os.path.join(dir, "bibliotools_tests/testFiles/parser_tests/test_output/subjects.dat"))
            os.remove(os.path.join(dir, "bibliotools_tests/testFiles/parser_tests/test_output/title_keywords.dat"))

        if os.path.exists(os.path.dirname(os.path.join(dir, "bibliotools_tests/testFiles/parser_tests/test_output"))):
            os.rmdir(os.path.join(dir, "bibliotools_tests/testFiles/parser_tests/test_output"))

    """
    This test tests that all_txt_files returns a correct number
    when there is one .txt file in the given folder.
    """
    def test_all_txt_files_for_at_least_one_file(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        directory = os.path.join(dir, "bibliotools_tests/testFiles")
        myfile = open(os.path.join(directory, "all_txt_file.txt"), "w")
        result = False
        if len(parsers.all_txt_files(directory)) >= 1:
            result = True
            myfile.close()
            os.remove(os.path.join(directory, "all_txt_file.txt"))
        self.assertEqual(True, result)
