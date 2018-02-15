import os
import itertools
from config import CONFIG

'''
File: corpus_parsed_overview.py
This file essentially prints statistics about the content of all span files
'''

def process_span(span):
	print_and_report("\n\n#%s" %span)
	with open(os.path.join(CONFIG["parsed_data"], span, "articles.dat"), "r") as file:
		data_lines = file.read().split("\n")[:-1]
		print_and_report("- number of articles : %s"%len(data_lines))

def print_statistics():
	print_statistics_of("authors.dat")
	print_statistics_of("countries.dat")
	print_statistics_of("institutions.dat")
	print_statistics_of("isi_keywords.dat")
	print_statistics_of("article_keywords.dat")
	print_statistics_of("title_keywords.dat")
	print_statistics_of("references.dat")
	print_statistics_of("subjects.dat")

def print_and_report(message):
	print(message)
	with open(os.path.join(CONFIG["reports_directory"], "corpus_overview.txt"), "a") as f:
		f.write(message + "\n")

def print_statistics_of(filename):
	with open(os.path.join(CONFIG["parsed_data"], span, filename), "r") as file:

		# .dat files all have one trailing blank line
		data_lines = file.read().split("\n")[:-1]
		entity_name = filename.split(".")[0]

		if filename != "references.dat":
			entities_by_articles = [aba.split("\t")[-1] for aba in data_lines]
		else:
			entities_by_articles = [",".join(aba.split("\t")[1:]) for aba in data_lines]

		unique_entities = set(entities_by_articles)
		print_and_report("- number of %s : unique %s total links with articles %s" %(entity_name, len(unique_entities), len(entities_by_articles)))

		# Cumulative distribution of Entities distribution

		with open(os.path.join(CONFIG["reports_directory"], "%s_%s_distribution.csv" %(span,entity_name)), "w") as f:
			f.write("occ,nb_%s,cumulative %%\n" %(entity_name))
			occurences = [len(list(g)) for (k,g) in itertools.groupby(sorted(entities_by_articles,reverse = True))]
			l = []
			nb_occ_cumul = 0
			for occurence, v in itertools.groupby(sorted(occurences,reverse = True)):
				nb_occ_cumul += len(list(v))
				occ_cumul = 100 * float(nb_occ_cumul) / len(unique_entities)
				l.append((occurence, nb_occ_cumul, occ_cumul))
			to_write = ""
			for e in l:
				to_write += "%02d,%02d,%04.1f%%\n" %(e)
			f.write(to_write)

# -- Main script --

if os.path.exists(os.path.join(CONFIG["reports_directory"], "corpus_overview.txt")):
	os.remove(os.path.join(CONFIG["reports_directory"], "corpus_overview.txt"))

for span in CONFIG["spans"]:
	process_span(span)
	print_statistics()
