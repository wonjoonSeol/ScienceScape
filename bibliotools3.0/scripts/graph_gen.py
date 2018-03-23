import argparse

'''
Prompt for time spans. This is used to split the data into several time spans.
'''
parser = argparse.ArgumentParser(description='For each time span enter a range \"YYYY-YYYY\". \
                                              For user add the user\'s name. \
                                              For the headers add the headers from WOS only if they have changed value from the default.')
parser.add_argument('-bound', nargs='+', metavar='bound', help='Year value (YYYY-YYYY, ...)', default={"1900-1999", "2000-2018"})

'''
Prompt for user name. This is for a web server setup.
The stored location is the ScienceScape/static/userFiles. /
 (If no user is added, then the bibliotools folder is used, without any user
hierarchy.)
'''
parser.add_argument('-user', default=' ', help='Prompt the user for user name. \
                                                This is for a web server setup.\
                    The stored location is the ScienceScape/static/userFiles/. \
(If no user is added, then the bibliotools folder is used, without any user \
hierarchy.)')

'''
'''
parser.add_argument('-headers', default='UT-AU-DE-ID-TI-WC-CR-C1-PY-J9-VL-BP-DI-PT-DT-TC',\
                        help='Add the headers separated by dashes in the following\
                                order: Accession Number, \
                                Authors, \
                                Author Keywords, \
                                Keywords Plus, \
                                Document Title, \
                                Wos Categories, \
                                Cited References, \
                                Author Address, \
                                Year Published, \
                                Twenty Nine Character Source Abbreviation, \
                                Volume, \
                                Beginning Page, \
                                Doi, \
                                Publication Type, \
                                Document Type, \
                                Wos Core Collection Times Cited.  \
                                Default is: UT-AU-DE-ID-TI-WC-CR-C1-PY-J9-VL-BP-DI-PT-DT-TC')

args = parser.parse_args()

spanYears = []


for range in vars(args)['bound']:
  boundPair = range.split("-") #string separated by '-' retains lowerbound-upperbound ordering
  intBoundPair = list(map(int, boundPair))
  spanYears.append(intBoundPair)

user = args.user
print(user)

# Run all scripts.
import config
config.spanYears = spanYears
CONFIG = config.gen(user, str(args.headers).split('-'))

print("\nMERGING CORPUS\n")
import merging_corpus
merging_corpus.CONFIG = CONFIG
merging_corpus.run()

print("\nPARSE AND GROUP\n")
import parse_and_group
parse_and_group.CONFIG = CONFIG
parse_and_group.run()

print("\nCORPUS PARSED OVERVIEW\n")
import corpus_parsed_overview
corpus_parsed_overview.CONFIG = CONFIG
corpus_parsed_overview.run()

print("\nFILTER AND NETWORK REFERENCES\n")
import filter_and_network_ref
filter_and_network_ref.CONFIG = CONFIG
filter_and_network_ref.run()

print("\nANNOTATIONS MULTIPROC\n")
import annotations_multiproc
annotations_multiproc.CONFIG = CONFIG
annotations_multiproc.run()

print("\n>>>Done. span-name_annotated.graphml graph can be opened in Gephi for example")
