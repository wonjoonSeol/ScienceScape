import os
import parsers
import traceback

'''
File: parse_and_group.py
This script will separate the publications in the data files by year,
and parse each data line to extract some information.
'''

CONFIG = {}
""" Return a Boolean representing whether the input year is within the given range. """
def is_year_within_span(startYear, endYear, year):
	if year >= startYear and year <= endYear:
		return True
	else:
		return False

"""
Create files corresponding to certain year spans, and write wos_headers to the first line.
"""
def create_span_files(years_spans, input_dir, output_dir, files, wos_headers):
	# For each year span:
	for (span,ys) in years_spans.items():
		# Create a folder with the same name
		if not os.path.exists(os.path.join(input_dir, output_dir, span)):
			os.mkdir(os.path.join(input_dir, output_dir, span))
		if os.path.exists(os.path.join(input_dir, output_dir, span, span) + ".txt"):
			print("removed here 1")
			os.remove(os.path.join(input_dir,output_dir, span, span) + ".txt")

		# Create a txt file and write the usual headers to it
		files[span] = open(os.path.join(input_dir, output_dir, span, span) + ".txt", "w")
		files[span].write(wos_headers + "\n")

"""
Place an input line into the correct file corresponding with its publication year value.
"""
def separate_years(line, years_spans, files, year_index_position):
	if "\t" in line:	# Filter blank lines out
		try:
			year = int(line.split("\t")[year_index_position])
			for (span,bounds) in years_spans.items():
				# If the publication year is within a time span,
				# write it in the adequate file
				if is_year_within_span(bounds[0], bounds[1], year):
					files[span].write(line)
		except Exception as e:
			print(traceback.format_exc())
			exit()

"""
Use the Wos_parser function from parsers.py to parse the current span files.
"""
def parse_span(span, input_dir, output_dir, outdir_prefix, files):
	files[span].close()
	if not os.path.exists(os.path.join(outdir_prefix, span)):
		os.mkdir(os.path.join(outdir_prefix, span))

	parsers.wos_parser(os.path.join(input_dir, output_dir, span), os.path.join(outdir_prefix, span), True)

""" Return a dictionary relating parameters in span_items. """
def get_span_parameters(span_items, year_key):
	return dict((s, data[year_key]) for s, data in span_items)

""" Return a list of lines to be separated into time spans.
Open the WOS corpus, discard the first header line, and then fetch all remaining lines.
"""
def get_lines_to_separate(one_file_corpus):
	onefile_output = open(one_file_corpus, "r")
	onefile_output.readline()
	lines_to_write = onefile_output.readlines()
	onefile_output.close()
	return lines_to_write

"""
Create text files for each year span, partition lines into the correct span files, 
and parse the data of each span file.
"""
def parse_and_group_data(one_file_corpus, output_dir, outdir_prefix, span_items, year_index_position, wos_headers):
	input_dir = os.path.dirname(one_file_corpus)
	if not os.path.exists(os.path.join(input_dir, output_dir)):
		os.mkdir(os.path.join(input_dir, output_dir))
	if not os.path.exists(outdir_prefix):
		os.mkdir(outdir_prefix)

	# Create one txt file for each user-defined year span
	years_spans = get_span_parameters(span_items, "years")
	files = {}
	create_span_files(years_spans, input_dir, output_dir, files, wos_headers)
	print("Year spans: " + str(years_spans))
	# Write lines to the adequate span file
	for line in get_lines_to_separate(one_file_corpus):
		separate_years(line, years_spans, files, year_index_position)

	for (span,ys) in years_spans.items():
		parse_span(span, input_dir, output_dir, outdir_prefix, files)	# For each span, parse its data

# -- Main Script --
def run():
    parsers.CONFIG = CONFIG
    parsers.initHeaders()
    parse_and_group_data(CONFIG["one_file_corpus"], CONFIG["wos_data_grouped"], CONFIG["parsed_data"], CONFIG["spans"].items(), CONFIG["year_index_position"], CONFIG["wos_headers"])
