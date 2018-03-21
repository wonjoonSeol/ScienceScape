from .forms import *
from csv import DictReader
from csv import reader
import shutil
import os
import re
from django.db import models
from .models import Mappings
import glob

"""
Takes an uploaded file and does the following:
	1.Produces a dictionary of raw headers mapped to a set of its records
	2.Checks whether this file has been uploaded before and hence retrieves the header values
	3.Otherwise attempts to detect which headers belong to which fields
	4.Returns a form set.
"""

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

countries = ["United States of America","Afghanistan","Albania","Algeria","Andorra","Angola","Antigua & Deps","Argentina","Armenia","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bhutan","Bolivia","Bosnia Herzegovina","Botswana","Brazil","Brunei","Bulgaria","Burkina","Burma","Burundi","Cambodia","Cameroon","Canada","Cape Verde","Central African Rep","Chad","Chile","People's Republic of China","Republic of China","Colombia","Comoros","Democratic Republic of the Congo","Republic of the Congo","Costa Rica,","Croatia","Cuba","Cyprus","Czech Republic","Danzig","Denmark","Djibouti","Dominica","Dominican Republic","East Timor","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Ethiopia","Fiji","Finland","France","Gabon","Gaza Strip","The Gambia","Georgia","Germany","Ghana","Greece","Grenada","Guatemala","Guinea","Guinea-Bissau","Guyana","Haiti","Holy Roman Empire","Honduras","Hungary","Iceland","India","Indonesia","Iran","Iraq","Republic of Ireland","Israel","Italy","Ivory Coast","Jamaica","Japan","Jonathanland","Jordan","Kazakhstan","Kenya","Kiribati","North Korea","South Korea","Kosovo","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Mauritania","Mauritius","Mexico","Micronesia","Moldova","Monaco","Mongolia","Montenegro","Morocco","Mount Athos","Mozambique","Namibia","Nauru","Nepal","Newfoundland","Netherlands","New Zealand","Nicaragua","Niger","Nigeria","Norway","Oman","Ottoman Empire","Pakistan","Palau","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Poland","Portugal","Prussia","Qatar","Romania","Rome","Russian Federation","Rwanda","St Kitts & Nevis","St Lucia","Saint Vincent & the","Grenadines","Samoa","San Marino","Sao Tome & Principe","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore","Slovakia","Slovenia","Solomon Islands","Somalia","South Africa","Spain","Sri Lanka","Sudan","Suriname","Swaziland","Sweden","Switzerland","Syria","Tajikistan","Tanzania","Thailand","Togo","Tonga","Trinidad & Tobago","Tunisia","Turkey","Turkmenistan","Tuvalu","Uganda","Ukraine","United Arab Emirates","United Kingdom","Uruguay","Uzbekistan","Vanuatu","Vatican City","Venezuela","Vietnam","Yemen","Zambia","Zimbabwe"]

""" Return a set of forms
Loads a file from a given file path and detects its headers.
Produces a form from this set of headers and returns it.
"""
def load_from_file_path(file_path):
	dictionary = process_txt_into_dictionary(file_path)
	in_database = retrieve_from_database(file_path)
	headers = detect_headers_from_and_remove(dictionary)

	form_set = produce_form_set(headers['headers'], headers['unknownValues'])
	return form_set

""" Return True if a file is .txt.
Checks a file to make sure it is a txt file.
"""
def check_txt_file(file):
    if file.name[-4:] == ".txt":
        return True
    else:
        return False

"""Return a zero-whitespace free string
Removes the UTF-8 whitespace character \ufeff from the input string.
"""
def remove_zero_whitespace_character(string_in):
	return str(string_in).strip("\ufeff")

"""Return a dictionary of sets.
For each header in a dictionary, this function creates a set in a dictionary.
"""
def make_header_sets(file_path):
	header_value_sets = dict()
	# Open file to make header keys
	with open(file_path) as txt_file:
		txt_reader = reader(txt_file, delimiter = '\t')
		for headers in txt_reader:
			for header in headers:
				header_value_sets[header] = set()
			break
	return header_value_sets

"""Return a populated dictionary
Populates a dictionary with actual data from a txt file.
"""
def populate_dictionary(header_value_sets, file_path, for_fields = False):
	populated = header_value_sets
	with open(file_path) as txt_file:
		dict_reader = DictReader(txt_file, delimiter = '\t')
		for row in dict_reader:
			for key in populated:
				if for_fields:
					populated[key].add((row[key], row[key]))
				else:
					populated[key].add(row[key])
	return populated

""" Return a dictionary of header/value sets.
Processes the txt file and returns a dictionary of headers mapped to a set of values.
"""
def process_txt_into_dictionary(file_path, for_fields = False):
	header_value_sets = make_header_sets(file_path)
	return populate_dictionary(header_value_sets, file_path, for_fields)

def make_user_folders(username):
	static_user_files_directory = "static/userFiles"
	public_user_files_directory = "static/userFiles/Public"
	user_files_folder = "static/userFiles/{x}".format(x = username)

	if not os.path.exists(os.path.join(APP_DIR, static_user_files_directory)):
		os.mkdir(os.path.join(APP_DIR, static_user_files_directory))

	if not os.path.exists(os.path.join(APP_DIR, public_user_files_directory)):
		os.mkdir(os.path.join(APP_DIR, public_user_files_directory))

	if not os.path.exists(os.path.join(APP_DIR, user_files_folder)):
		os.mkdir(os.path.join(APP_DIR, user_files_folder))

	return user_files_folder

""" Return a dictionary containing the full file name and the user file name.
Saves the file to the userFiles folder in the project's root directory.
"""
def save_file(file, username = "Public"):
	file_name = file.name

	# Save the uploaded file inside that folder.
	full_file_name = os.path.join(APP_DIR, make_user_folders(username), file_name)

	file_to_save = open(full_file_name,'w')
	file_to_save.write(file.read().decode("utf-8"))
	file_to_save.close()

	print("File saved at {s}".format(s = full_file_name))
	return {'FULL_FILE_NAME': full_file_name, 'USER_FILE_NAME': file_name }

""" Return a dictionary of attributes mapped to Bibliotools representation.
of those attributes (eg. Date: SS), and a list of unknown attributes that could not be detected.
Detects headers from a dictionary.
"""
def detect_headers_from_and_remove(dictionary):
	print("dic: " + str(dictionary))
	headers = dict(Author = None, Date = None, Country = None)
	undetectable_values = []
	date_pattern = re.compile('(((\d(\d)?))/){2}((\d\d)(\d\d)?)', re.IGNORECASE)

	# All values are undetectable until they can be detected
	for entry in dictionary:
		undetectable_values.append(entry)

	for entry in dictionary:
		if date_pattern.match(dictionary[entry].pop()):
			headers['Date'] = entry
			undetectable_values.remove(entry)
			print(headers['Date'])
			print("Matched date header")
		elif dictionary[entry] in countries:
			headers['Country'] = entry
			undetectable_values.remove(entry)
			print("Matched country header")

	return {'headers': headers, 'unknownValues': undetectable_values}

"""
Refreshes the database, adding mappings of the file names to their true values (e.g. mapping SS to Author in file 'fileName')
"""
def refresh_database(dictionary, file_path):
	record = Mappings.objects.filter(FILE_LINK = file_path)
	if record:
		record.delete()

	for key in dictionary:
		mapping = Mappings()
		mapping.TRUE_NAME = key
		mapping.FILE_NAME = dictionary[key]
		mapping.FILE_LINK = file_path
		mapping.save()

""" Return a dictionary created from a file path, containing the true name, file name of the file
    and the link to the file, for each entry.
Retrieves mappings of file names to their true values for the file of the file path passed in.
"""
def retrieve_from_database(file_path):
	print("retrieving for file path: " + str(file_path))
	dictionary = dict()
	files_in_database = Mappings.objects.filter(FILE_LINK = file_path)
	if files_in_database:
		for file in files_in_database:
			dictionary[file.TRUE_NAME] = file.FILE_NAME
	else:
		return None

	for key in dictionary:
		dictionary[key] = remove_zero_whitespace_character(dictionary[key])

	return dictionary

"""
Deletes all records in the Mappings database
"""
def resetDatabase():
	mappings = Mappings.objects.all()
	mappings.delete()

""" Return a list of file paths.
Gets all files for a user files folder, computed with the user's name.
"""
def get_all_user_files(username):
	user_files_folder = "static/userFiles/{x}".format(x = username)

	if not os.path.exists(os.path.join(APP_DIR, user_files_folder)):
		return []
	else:
		file_path = os.path.join(APP_DIR, user_files_folder)
		files_in_directory = os.listdir(file_path)
		files_valid = []
		for file in files_in_directory:
			if file[-4:] == ".txt":
				files_valid.append(file)

		return files_valid

""" Return the path to the created graph file
Starts processing a graph file using the Bibliotools3.0 back-end source code.
"""
def start_bibliotools(year_start, year_end, file_path, username='Public'):
	static_user_files_directory = "static/userFiles"
	user_files_folder = "static/userFiles/{x}".format(x = username)
	print("FILE PATH! " + str(file_path))
	dictionary_of_fields = retrieve_from_database(file_path)
	headers_as_string = ""
	
	print("File Path: {f} -> Dictionary: {d}".format(f=file_path, d = str(dictionary_of_fields)))	
	
	if dictionary_of_fields: 
		for header in dictionary_of_fields:
			headers_as_string += "{x}-".format(x = dictionary_of_fields[header])
		
		headers_as_string = headers_as_string[:len(headers_as_string) - 1]
		headers_as_string = headers_as_string.rstrip()	



	if os.path.exists(os.path.join(user_files_folder, "data-wos")):
	    shutil.rmtree(os.path.join(user_files_folder, 'data-wos'))

	if os.path.exists(os.path.join(user_files_folder, "Result")):
	    shutil.rmtree(os.path.join(user_files_folder, 'Result'))

	if not os.path.exists(os.path.join(user_files_folder, 'data-wos')):
		os.mkdir(os.path.join(user_files_folder, 'data-wos'))

	user_wos_folder = os.path.join(user_files_folder, 'data-wos')

	if not os.path.exists(os.path.join(user_files_folder, 'Result')):
		os.mkdir(os.path.join(user_files_folder, 'Result'))

	user_results_folder = os.path.join(user_files_folder, 'Result')
	shutil.copy(os.path.join(user_files_folder, file_path), user_wos_folder)

	print(f'python3 bibliotools3.0/scripts/graph_gen.py -user {username} -bound {year_start}-{year_end} -headers {headers_as_string}')

	os.system(f'python3 bibliotools3.0/scripts/graph_gen.py -user {username} -bound {year_start}-{year_end} -headers {headers_as_string}')

	graph_file_path = str(collect_graph_file(os.path.join(user_results_folder, "parsed_data"))).replace("static/", "")
	return graph_file_path

def collect_graph_file(directory, span_name = "span_name_0", format = "gexf"):
	output_directory = os.path.join(directory, span_name)
	file_to_collect = "%s/*" + format
	reg_ex = file_to_collect % output_directory
	return glob.glob(reg_ex)
