import unittest
import sys
import os

lib_path = os.path.abspath(os.path.join(__file__, '..', '..', '..', 'bibliotools3.0', 'scripts'))
sys.path.append(lib_path)

import config
import parsers

class TestParsers(unittest.TestCase):

    """
    These tests assess the ability of parsers.py to parse a test input and
    separate the information into different categories.

    These test wos_parser, which tests all the units in the parsers.py file.
    """

    dir = os.path.dirname(os.path.dirname(__file__))
    CONFIG = config.gen()
    parsers.CONFIG = CONFIG
    parsers.initHeaders()
    test_input_txt = open(os.path.join(dir, "testFiles/parser_tests/input_parser.txt"), "r")
    parsers.wos_parser(os.path.join(dir, "testFiles/parser_tests"), os.path.join(dir, "testFiles/parser_tests/test_output"), False)
    test_input_txt.close()

    def test_parse_articles(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.join(dir, "testFiles/parser_tests/test_output/articles.dat"), "r") as myfile:
            output = myfile.read().replace("\n", "")

        with open(os.path.join(dir, "testFiles/parser_tests/desired_output/articles.dat"), "r") as myfile:
            desired_output = myfile.read().replace("\n", "")

        self.assertEqual(output, desired_output)

    def test_parse_authors(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.join(dir, "testFiles/parser_tests/test_output/authors.dat"), "r") as myfile:
            output = myfile.read().replace("\n", "")

        with open(os.path.join(dir, "testFiles/parser_tests/desired_output/authors.dat"), "r") as myfile:
            desired_output = myfile.read().replace("\n", "")

        self.assertEqual(output, desired_output)

    def test_parse_countries(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.join(dir, "testFiles/parser_tests/test_output/countries.dat"), "r") as myfile:
            output = myfile.read().replace("\n", "")

        with open(os.path.join(dir, "testFiles/parser_tests/desired_output/countries.dat"), "r") as myfile:
            desired_output = myfile.read().replace("\n", "")

        self.assertEqual(output, desired_output)

    def test_parse_article_keywords(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.join(dir, "testFiles/parser_tests/test_output/article_keywords.dat"), "r") as myfile:
            output = myfile.read().replace("\n", "")

        with open(os.path.join(dir, "testFiles/parser_tests/desired_output/article_keywords.dat"), "r") as myfile:
            desired_output = myfile.read().replace("\n", "")

        self.assertEqual(output, desired_output)

    def test_parse_institutions(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.join(dir, "testFiles/parser_tests/test_output/institutions.dat"), "r") as myfile:
            output = myfile.read().replace("\n", "")

        with open(os.path.join(dir, "testFiles/parser_tests/desired_output/institutions.dat"), "r") as myfile:
            desired_output = myfile.read().replace("\n", "")

        self.assertEqual(output, desired_output)

if __name__ == '__main__':
    unittest.main()
