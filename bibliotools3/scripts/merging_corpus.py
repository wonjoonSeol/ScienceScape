import os
import datetime


'''
File: merging_corpus.py
This script merges all the data files found in 'data-wos' and writes
all parseable lines to a single file, Result/one_file_corpus.txt
'''

CONFIG = {}

"""
Writes year distributions for all spans into a CSV file.
"""
def write_year_distribution(reports_directory, years_spans):
    print("reports dir: " + str(reports_directory))
    years_distribution = open(os.path.join(reports_directory, "years_distribution.csv"), "w")
    years_distribution.write("year,nb_articles\n")

    for y,n in sorted(((y,n) for (y,n) in years_spans.items()), key = lambda a: a[0]):
        years_distribution.write("%s,%s\n" %(y,n))
        print("%s: %s articles" %(y,n))

    years_distribution.close()
    print("\nYear distribution reported in %s" %os.path.join(reports_directory,"years_distribution.csv"))

"""
Counts occurrences of years within years_spans and reports the resulting year distribution.
"""
def count_occurences(one_file_corpus, reports_directory):
    # Output the article numbers by year
    years_spans = {}
    onefile_output = open(one_file_corpus, "r")
    onefile_output.readline()   # Remove the headers

    for line in onefile_output.readlines():
        # Filter the blank lines out
        if "\t" in line:
            year = line.split("\t")[CONFIG["year_index_position"]]
            years_spans[year] = years_spans[year] + 1 if year in years_spans else 1

    onefile_output.close()
    write_year_distribution(reports_directory, years_spans)     # Report year distribution for information

"""
Writes text to a file.
"""
def write_to_file(open_file, text):
    open_file.write(text)

""" Return the number of columns present in a line of text, split by tab. """
def number_columns(line):
    return len(line.split("\t"))

""" Return an integer that is set to 1 if the line was stripped of a trailing tab.
Parse an input line, filtering out blank lines and ensuring that the number of columns
corresponds to the selected headers.
"""
def parse_line(l, nb_values_in_wos, parseable_lines, lines_with_errors):
    repaired = 0
    if "\t" in l:
        # Filtering blank lines in the file
        if number_columns(l) > nb_values_in_wos:   # If there are too many columns, the line is not parseable
            if l[-1] == "\t":
                parseable_lines.append(l[:-1])     # Stripping extra tab
                repaired += 1
            else:
                print("Warning! Too many columns with %s" %l[-20:])
                lines_with_errors.append(l)
        elif number_columns(l) < nb_values_in_wos: # If there are too few columns, the line is not parseable
            print("Warning! Too few columns with %s"%l[-20:])
            lines_with_errors.append(l)
        else:
            parseable_lines.append(l)
    return repaired     # For statistics

"""
Write the parsed output and errors output to result files.
"""
def write_report(parseable_lines, lines_with_errors, onefile_output, errorsfile_output):
    write_to_file(onefile_output, "\n".join(parseable_lines) + "\n")
    write_to_file(errorsfile_output, "\n".join(lines_with_errors) + "\n")
    print("Found %s non-parseable lines, reported in wos_lines_with_errors.csv" %(len(lines_with_errors)))

""" Return a counter of all lines that were repaired in the file.
Parse an entire file, removing the headers and parsing each line individually.
"""
def parse_file(file, root, nb_values_in_wos, onefile_output, errorsfile_output):
    new_trailing_tabs = 0
    if not file.startswith('.'):
        filepath = os.path.join(root, file)
        print("Merging %s" %filepath)
        with open(filepath, "r") as f:

            # Remove the first line (containing headers)
            lines = f.read().split("\n")[1:]
            lines = [l.strip(" ") for l in lines]
            lines = [l.strip("\r") for l in lines]

            parseable_lines = []
            lines_with_errors = []

            for line in lines:
                new_trailing_tabs += parse_line(line, nb_values_in_wos, parseable_lines, lines_with_errors)
            write_report(parseable_lines, lines_with_errors, onefile_output, errorsfile_output)
    return new_trailing_tabs

""" Return the final output file.
Construct output file.
"""
def prepare_output_file(one_file_corpus, wos_headers):
    if not os.path.exists(os.path.dirname(one_file_corpus)):
        os.makedirs(os.path.dirname(one_file_corpus))
    onefile_output = open(one_file_corpus, "w")
    write_to_file(onefile_output, wos_headers + "\n")
    return onefile_output
"""
Construct a directory to place reports in.
"""
def prepare_report_directory(reports_directory):
    if not os.path.exists(reports_directory):
        os.mkdir(reports_directory)
    elif not os.path.isdir(reports_directory):
        print("Remove file %s or change 'reports_directory' value in config.py" %reports_directory)
        exit()

"""
Construct a file to place error reports in.
"""
def prepare_error_file(reports_directory, wos_headers):
    errorsfile_output = open(os.path.join(reports_directory, "wos_lines_with_errors.csv"), "w")
    write_to_file(errorsfile_output, wos_headers + "\n")
    return errorsfile_output

"""
Parse and merge all output files in the WOS corpus into one.
"""
def merge_corpus(one_file_corpus, wos_headers, reports_directory, wos_data):
    print("wos data is " + str(wos_data))
    nb_values_in_wos = len(wos_headers.split("\t"))

    # Prepare output files/folders (write headers and have them ready for writing)
    onefile_output = prepare_output_file(one_file_corpus, wos_headers)
    prepare_report_directory(reports_directory)
    errorsfile_output = prepare_error_file(reports_directory, wos_headers)

    # Go through all the files in the WOS corpus
    nb_extra_trailing_tab = 0
    for root, _, files in os.walk(wos_data):
        for file in files:
            print("file!")
            nb_extra_trailing_tab += parse_file(file, root, nb_values_in_wos, onefile_output, errorsfile_output)

    print("All files have been merged into %s \nRepaired %s lines with trailing extra tab \n" %(one_file_corpus, nb_extra_trailing_tab))
    onefile_output.close()
    errorsfile_output.close()
    count_occurences(one_file_corpus, reports_directory)

# -- Main script --
def run():
    merge_corpus(CONFIG["one_file_corpus"], CONFIG["wos_headers"], CONFIG["reports_directory"], CONFIG["wos_data"])
