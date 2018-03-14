import unittest
import sys
import os

lib_path = os.path.abspath(os.path.join(__file__, '..', '..', '..', 'bibliotools3.0', 'scripts'))
sys.path.append(lib_path)

from corpus_parsed_overview import get_no_articles
from corpus_parsed_overview import get_stats
from corpus_parsed_overview import print_to_overview

class TestCorpusParsedOverview(unittest.TestCase):

    """
    This test tests that when there are no resources to be parsed,
    no output folder is created.
    """
    def test_get_no_articles_for_empty_resource(self):

        dir = os.path.dirname(os.path.dirname(__file__))
        parsed_data_folder = os.path.join(dir, "testFiles/parsed_data")

        self.assertEqual(0, get_no_articles(parsed_data_folder, "span_name"))

    """
    This test tests that the get_no_articles statistics method
    returns a correct value for fifty articles to be parsed.
    """
    def test_get_no_articles_for_fifty_articles(self):

        dir = os.path.dirname(os.path.dirname(__file__))
        parsed_data_folder = os.path.join(dir, "testFiles/parsed_data")

        self.assertEqual(50, get_no_articles(parsed_data_folder, "span_name_2"))

    """
    This test tests that upon calling get_stats,
    the statistics returned are right.
    """
    def test_get_stats_for_articles_file(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        parsed_data_folder = os.path.join(dir, "testFiles/parsed_data")

        # For span_name_2, there should be 50 unique articles, and 50 entities by articles.
        result = get_stats(parsed_data_folder, "span_name_2", "articles.dat")
        self.assertEqual(True, result[2] == 50 and result[3] == 50)

    """
    This test tests that calling statistics for a real references.dat file
    yields a correct output.
    """
    def test_get_stats_for_references_file(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        parsed_data_folder = os.path.join(dir, "testFiles/parsed_data")

        # For the given references.dat file, we know there have to be:
        # 2379 unique references, and 2463 references by articles.
        result = get_stats(parsed_data_folder, "span_name_2", "references.dat")
        self.assertEqual(True, result[2] == 2379 and result[3] == 2463)

    """
    This test tests that printing to overview works without data corruption.
    """
    def test_print_to_overview(self):
        dir = os.path.dirname(os.path.dirname(__file__))
        os.makedirs(os.path.join(dir, "testFiles/reports_for_overview"))
        reports_directory = os.path.join(dir, "testFiles/reports_for_overview")

        print_to_overview("This is a successful test message", reports_directory)

        output = open(os.path.join(dir, "testFiles/reports_for_overview/corpus_overview.txt"))
        lines = output.readlines()
        result = len(lines) == 1 and lines[0] == "This is a successful test message\n"
        output.close()
        os.remove(os.path.join(dir, "testFiles/reports_for_overview/corpus_overview.txt"))
        os.rmdir(os.path.join(dir, "testFiles/reports_for_overview"))
        self.assertEqual(True, result)


if __name__ == '__main__':
    unittest.main()
