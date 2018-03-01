import os
dir = os.path.dirname(os.path.dirname(__file__))

year_index_position = 44

spanYears = []

def gen():
	CONFIG={
		# step one (merging_corpus.py) mandatory
		"wos_data": os.path.join(dir, "data-wos/"),
		"one_file_corpus": os.path.join(dir, "Result/one_file_corpus.txt"),
		"reports_directory": os.path.join(dir, "Result/report"),

		# step two (parse_and_group.py) mandatory
		"wos_data_grouped": os.path.join(dir, "Result/grouped_data"),
		"parsed_data": os.path.join(dir, "Result/parsed_data"),
		# a span is a period of time defined by years
		# large wos corpus are likely to be cutted into time-spans
		# any data outside spans will be ignored
		"spans":{
				"span_name":{
					"years":[1900,1999],

					#filtering:
					# occ : minimum number of occurences in corpus
					# weight : minimum number of co-occurences with reference in articles (edge weight)

					#filtering on reference are mandatory from step three
					"references":{"occ":2,"weight":1},

					#filtering on items are mandatory from step four
					"subjects":{"occ":0,"weight":1},
					"authors":{"occ":0,"weight":1},
					"institutions":{"occ":0,"weight":1},
					"article_keywords":{"occ":0,"weight":1},
					"title_keywords":{"occ":0,"weight":1},
					"isi_keywords":{"occ":0,"weight":1},
					"countries":{"occ":0,"weight":1},
				},
				"span_name_2":{
					"years":[2000, 2018],
					"references":{"occ":0,"weight":1},
					"subjects":{"occ":0,"weight":1},
					"authors":{"occ":0,"weight":1},
					"institutions":{"occ":0,"weight":1},
					"article_keywords":{"occ":0,"weight":1},
					"title_keywords":{"occ":0,"weight":1},
					"isi_keywords":{"occ":0,"weight":1},
					"countries":{"occ":0,"weight":1},
				}

		},
		#output directory
		"output_directory": os.path.join(dir, "Result/Output"),

		#step three mandatory
		# network formats should be choosen in networkx format list
		"export_ref_format":"gexf",
		"network_colours":{
					"subjects":{"r":225,"g":140,"b":0},
					"authors":{"r":255,"g":215,"b":0},
					"institutions":{"r":107,"g":142,"b":35},
					"article_keywords":{"r":255,"g":105,"b":180},
					"title_keywords":{"r":225,"g":0,"b":0},
					"isi_keywords":{"r":0,"g":255,"b":0},
					"countries":{"r":176,"g":224,"b":230}
					},

		# verbose
		"process_verbose":False,
		"report_verbose":True,
		"report_csv":True,

		# number of processes to use in annotations_multiproc.py
		# beware the more processes the more memory is needed
		"nb_processes":2,


		"export_ref_annotated_format":"graphml",#can't be gexf because of bug #1296 in networkx see https://github.com/networkx/networkx/issues/1296
		# If your wos export file don't have this first line, it's not going to work!
	    "wos_headers" : "PT	AU	BA	BE	GP	AF	BF	CA	TI	SO	SE	BS	LA	DT	CT	CY	CL	SP	HO	DE	ID	AB	C1	RP	EM	RI	OI	FU	FX	CR	NR	TC	Z9	U1	U2	PU	PI	PA	SN	EI	BN	J9	JI	PD	PY	VL	IS	PN	SU	SI	MA	BP	EP	AR	DI	D2	EA	EY	PG	WC	SC	GA	UT	PM	OA	HC	HP	DA",
	    "year_index_position" : 44,

		"common_words": ['a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also', 'am', 'among', 'an', 'and',
		        'any', 'are', 'as', 'at', 'be', 'because', 'been', 'but', 'by', 'can', 'cannot', 'could', 'dear',
		        'did', 'do', 'does', 'either', 'else', 'ever', 'every', 'for', 'from', 'get', 'got', 'had', 'has',
		        'have', 'he', 'her', 'hers', 'him', 'his', 'how', 'however', 'i', 'if', 'in', 'into', 'is', 'it',
		        'its', 'just', 'least', 'let', 'like', 'likely', 'may', 'me', 'might', 'most', 'must', 'my',
		        'neither', 'no', 'nor', 'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our', 'own',
		        'rather', 'said', 'say', 'says', 'she', 'should', 'since', 'so', 'some', 'than', 'that', 'the',
		        'their', 'them', 'then', 'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas', 'us',
		        'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why',
		        'will', 'with', 'would', 'yet', 'you', 'your'],

		"punctuation": ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '.', '/',
		        ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', ' - '],

		#HEADER CODES
		'accession_number' : 'UT',
		'authors' : 'AU',
		'author_keywords' : 'DE',
		'keywords_plus' : 'ID',
		'document_title' : 'TI',
		'wos_categories' : 'WC',
		'cited_references' : 'CR',
		'author_address' : 'C1',
		'year_published' : 'PY',
		'twenty_nine_character_source_abbreviation' : 'J9',
		'volume' : 'VL',
		'beginning_page' : 'BP',
		'doi' : 'DI',
		'publication_type' : 'PT',
		'document_type' : 'DT',
		'wos_core_collection_times_cited' : 'TC',

		'usa_country_codes' : ['USA',
				'AL ', 'AK ', 'AZ ', 'AR ', 'CA ', 'NC ',
				'SC ', 'CO ', 'CT ', 'ND ', 'SD ','DE ', 'FL ', 'GA ', 'HI ' , 'ID ',
				'IL ', 'IN ', 'IA ', 'KS ', 'KY ', 'LA ', 'ME', 'MD ', 'MA ', 'MI ',
				'MN ', 'NJ ', 'NM ', 'NY ', 'OH ', 'OK ', 'PA ', 'RI ','TN ', 'TX ',
				'UT ', 'VT ', 'VA ', 'WV ', 'WA ', 'WI ', 'WY ', 'DC ']

	}
	return CONFIG
