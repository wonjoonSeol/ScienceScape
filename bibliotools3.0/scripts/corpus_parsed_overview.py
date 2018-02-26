import os
import itertools

CONFIG = {}

'''
File: corpus_parsed_overview.py
This file essentially prints statistics about the content of all span files
'''

def get_no_articles(parsed_data_folder, span):
    with open(os.path.join(parsed_data_folder, span, "articles.dat"), "r") as file:
        data_lines = file.read().split("\n")[:-1]
        return len(data_lines)

"""
This function returns a set of statistics:
position 1: all the unique entities
position 2: all the entities by articles
position 3: the number of unique entities
position 4: the number of entities by articles
"""
def get_stats(parsed_data_folder, span, dat_file_name):
    with open(os.path.join(parsed_data_folder, span, dat_file_name), "r") as file:
        data_lines = file.read().split("\n")[:-1]
        if dat_file_name != "references.dat":
            entities_by_articles = [dline.split("\t")[-1] for dline in data_lines]
        else:
            entities_by_articles = [",".join(dline.split("\t")[1:]) for dline in data_lines]
        unique_entities = set(entities_by_articles)
        return (unique_entities, entities_by_articles, len(unique_entities), len(entities_by_articles))

def print_to_overview(message, reports_directory):
    print(message)
    with open(os.path.join(reports_directory, "corpus_overview.txt"), "a") as f:
        f.write(message + "\n")

def print_statistics_of(parsed_data_folder, reports_directory, filename, span):
    stats = get_stats(parsed_data_folder, span, filename)
    entity_name = filename.split(".")[0]
    print_to_overview("- number of %s : unique %s total links with articles %s" %(entity_name, stats[2], stats[3]), reports_directory)

    # Cumulative distribution of Entities distribution
    with open(os.path.join(reports_directory, "%s_%s_distribution.csv" %(span,entity_name)), "w") as f:
        f.write("occ,nb_%s,cumulative %%\n" %(entity_name))
        occurences = [len(list(g)) for (k,g) in itertools.groupby(sorted(stats[1], reverse = True))]
        l = []
        nb_occ_cumul = 0
        for occurence, v in itertools.groupby(sorted(occurences,reverse = True)):
            nb_occ_cumul += len(list(v))
            occ_cumul = 100 * float(nb_occ_cumul) / stats[2]
            l.append((occurence, nb_occ_cumul, occ_cumul))
        to_write = ""
        for e in l:
            to_write += "%02d,%02d,%04.1f%%\n" %(e)
        f.write(to_write)

def print_statistics(parsed_data_folder, reports_directory, span):
    dat_files = ["authors.dat", "countries.dat", "institutions.dat", "isi_keywords.dat",
    "article_keywords.dat", "title_keywords.dat", "references.dat", "subjects.dat"]
    for item in dat_files:
            print_statistics_of(parsed_data_folder, reports_directory, item, span)

# -- Main script --
def run():
    if os.path.exists(os.path.join(CONFIG["reports_directory"], "corpus_overview.txt")):
        os.remove(os.path.join(CONFIG["reports_directory"], "corpus_overview.txt"))

        reports_directory = CONFIG["reports_directory"]
        parsed_data_folder = CONFIG["parsed_data"]
        if os.path.exists(os.path.join(reports_directory, "corpus_overview.txt")):
            os.remove(os.path.join(reports_directory, "corpus_overview.txt"))

        for span in CONFIG["spans"]:
            print_to_overview("\n\n#%s" %span, reports_directory)
            print_to_overview("- number of articles : %s" %get_no_articles(parsed_data_folder, span), reports_directory)
            print_statistics(parsed_data_folder, reports_directory, span)
