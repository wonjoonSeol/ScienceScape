import os
import parser
import traceback

CONFIG = {}

'''
File: parse_and_group.py
This script will separate the publications in the data files by year,
and parse each data line to extract some information.
'''

input_dir = None
output_dir = None
outdir_prefix = None
years_spans = None

def init():
	global input_dir
	input_dir = os.path.dirname(CONFIG["one_file_corpus"])
	global output_dir
	output_dir = CONFIG["wos_data_grouped"]
	global outdir_prefix
	outdir_prefix = CONFIG["parsed_data"]
	# Collect the user-defined year span preferences
	global years_spans
	years_spans = dict((s, data["years"]) for s, data in CONFIG["spans"].items())


files = {}	# Collection of span files

def is_year_within_span(startYear, endYear, year):
	if year >= startYear and year <= endYear:
		return True
	else:
		return False

def create_span_files():
	# For each year span:
	for (span,ys) in years_spans.items():

		# Create a folder with the same name
		if not os.path.exists(os.path.join(input_dir, output_dir, span)):
			os.mkdir(os.path.join(input_dir, output_dir, span))
		if os.path.exists(os.path.join(input_dir, output_dir, span, span) + ".txt"):
			os.remove(os.path.join(input_dir,output_dir, span, span) + ".txt")

		# Create a txt file and write the usual headers to it
		files[span] = open(os.path.join(input_dir, output_dir, span, span) + ".txt", "w")
		files[span].write(CONFIG["wos_headers"] + "\n")

def separate_years(line):
	if "\t" in line:	# Filter blank lines out
		try:
			year = int(line.split("\t")[CONFIG["year_index_position"]])
			for (span,bounds) in years_spans.items():
				# If the publication year is within a time span,
				# write it in the adequate file
				if is_year_within_span(bounds[0], bounds[1], year):
					files[span].write(line)
		except Exception as e:
			print(traceback.format_exc())
			exit()

def parse_span(span):
	files[span].close()
	if not os.path.exists(os.path.join(outdir_prefix, span)):
		os.mkdir(os.path.join(outdir_prefix, span))

	# Use Wos_parser function from parser.py to parse the lines
	parser.Wos_parser(os.path.join(input_dir, output_dir, span), os.path.join(outdir_prefix, span), True)

# -- Main Script --
def run():
	parser.CONFIG = CONFIG
	init()
	if not os.path.exists(os.path.join(input_dir, output_dir)):
		os.mkdir(os.path.join(input_dir, output_dir))

	if not os.path.exists(outdir_prefix):
		os.mkdir(outdir_prefix)

	# Create one txt file for each user-defined year span
	create_span_files()

	onefile_output = open(CONFIG["one_file_corpus"], "r")
	onefile_output.readline()

	lines_to_write = onefile_output.readlines()

	# Write lines to the adequate span file
	for line in lines_to_write:
		separate_years(line)

	onefile_output.close()

	for (span,ys) in years_spans.items():
		parse_span(span)	# For each span, parse its data
