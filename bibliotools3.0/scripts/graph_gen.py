import argparse

# Prompt the user for a time span.
parser = argparse.ArgumentParser(description='For each time span enter a range \"YYYY-YYYY\"')
parser.add_argument('-bound', nargs='+', metavar='bound', help='Year value', default={"1900-1999", "2000-2018"})
parser.add_argument('-user')
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
CONFIG = config.gen(user)

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
