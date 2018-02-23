import os
import datetime
from config import CONFIG

'''
File: merging_corpus.py
This script merges all the data files found in 'data-wos' and writes
all parseable lines to a single file, Result/one_file_corpus.txt
'''
def write_year_distribution(reports_directory, years_spans):
    years_distribution = open(os.path.join(reports_directory, "years_distribution.csv"), "w")
    years_distribution.write("year,nb_articles\n")

    for y,n in sorted(((y,n) for (y,n) in years_spans.items()), key = lambda a: a[0]):
        years_distribution.write("%s,%s\n" %(y,n))
        print("%s: %s articles" %(y,n))

    years_distribution.close()

    print("\nYear distribution reported in %s" %os.path.join(reports_directory,"years_distribution.csv"))


def count_occurences(one_file_corpus, reports_directory):
    # Output the article numbers by year
    years_spans = {}
    onefile_output = open(one_file_corpus, "r")

    # Remove the headers
    onefile_output.readline()

    for line in onefile_output.readlines():

        # Filter the blank lines out
        if "\t" in line:

            # Get the year of the publication
            year = line.split("\t")[CONFIG["year_index_position"]]

            # Increment the counter for that year in years_spans
            years_spans[year] = years_spans[year] + 1 if year in years_spans else 1

    onefile_output.close()

    # Report the year distribution for information
    write_year_distribution(reports_directory, years_spans)

# Preparing the one file corpus
one_file_corpus = CONFIG["one_file_corpus"]

if not os.path.exists(os.path.dirname(one_file_corpus)):
    os.makedirs(os.path.dirname(one_file_corpus))

onefile_output = open(one_file_corpus, "w")
wos_headers = CONFIG["wos_headers"]

# Writing the data file header to the corpus file
onefile_output.write(wos_headers + "\n")

# Check the reports directory
reports_directory = CONFIG["reports_directory"]

if not os.path.exists(reports_directory):
    os.mkdir(reports_directory)

elif not os.path.isdir(reports_directory):
    print("Remove file %s or change 'reports_directory' value in config.py"%reports_directory)
    exit()

# Writing the data file header to the error file
errorsfile_output = open(os.path.join(reports_directory, "wos_lines_with_errors.csv"), "w")
errorsfile_output.write(wos_headers + "\n")

nb_values_in_wos = len(wos_headers.split("\t"))

# Go through all the files in the WOS corpus
nb_extra_trailing_tab = 0

for root, subFolders, files in os.walk(CONFIG["wos_data"]):
    for file in files:
        if not file.startswith('.'):
            filepath = os.path.join(root, file)
            print("Merging %s" %filepath)
            with open(filepath, "r") as f:

                # Remove the first line (containing headers)
                lines = f.read().split("\n")[1:]

                # And remove the last character if it's a trailing tab
                lines = [l.strip(" ") for l in lines]
                lines = [l.strip("\r") for l in lines]

                parseable_lines = []
                lines_with_errors = []

                for l in lines:

                    if "\t" in l:
                        # Filtering blank lines in the file
                        if len(l.split("\t")) > nb_values_in_wos:   # If there are too many columns, the line is not parseable
                            if l[-1] == "\t":
                                parseable_lines.append(l[:-1]) # Stripping extra tab
                                nb_extra_trailing_tab += 1
                            else:
                                print("Warning! Too many columns with %s" %l[-20:])
                                lines_with_errors.append(l)

                        elif len(l.split("\t")) < nb_values_in_wos: # If there are too few columns, the line is not parseable
                            print("Warning! Too few columns with %s"%l[-20:])
                            lines_with_errors.append(l)

                        else:
                            parseable_lines.append(l)

                onefile_output.write("\n".join(parseable_lines) + "\n")
                errorsfile_output.write("\n".join(lines_with_errors) + "\n")

onefile_output.close()

print("All files have been merged into %s \n Repaired %s lines with trailing extra tab \n Found %s non-parseable lines, reported in wos_lines_with_errors.csv" %(one_file_corpus, nb_extra_trailing_tab, len(lines_with_errors)))

count_occurences(one_file_corpus, reports_directory)
