import os
import sys
import glob
import argparse
import utility
import re
import string

CONFIG = {}

def initHeaders():
    global accession_number
    accession_number = CONFIG['accession_number']
    global authors
    authors = CONFIG['authors']
    global author_keywords
    author_keywords = CONFIG['author_keywords']
    global keywords_plus
    keywords_plus = CONFIG['keywords_plus']
    global document_title
    document_title = CONFIG['document_title']
    global wos_categories
    wos_categories = CONFIG['wos_categories']
    global cited_references
    cited_references = CONFIG['cited_references']
    global author_address
    author_address = CONFIG['author_address']
    global year_published
    year_published = CONFIG['year_published']
    global twenty_nine_character_source_abbreviation
    twenty_nine_character_source_abbreviation = CONFIG['twenty_nine_character_source_abbreviation']
    global volume
    volume = CONFIG['volume']
    global beginning_page
    beginning_page = CONFIG['beginning_page']
    global doi
    doi = CONFIG['doi']
    global publication_type
    publication_type = CONFIG['publication_type']
    global document_type
    document_type = CONFIG['document_type']
    global wos_core_collection_times_cited
    wos_core_collection_times_cited = CONFIG['wos_core_collection_times_cited']

def parse_article(id, article, output):
    article_authors = getattr(article, authors).split('; ')
    firstAU = article_authors[0].replace(',','')
    output.write(f'{id}\t{firstAU}\t{getattr(article, year_published)}\t\
            {getattr(article, twenty_nine_character_source_abbreviation)}\t\
            {getattr(article, volume)}\t{getattr(article, beginning_page)}\t\
            {getattr(article, doi)}\t{getattr(article, publication_type)}\t\
            {getattr(article, document_type)}\t\
            {getattr(article, wos_core_collection_times_cited)}\t\
            {getattr(article, document_title)}\t\
            {getattr(article, accession_number)}\n')

def parse_authors(id, article, output):
    if getattr(article, authors) != '':
        article_authors = getattr(article, authors).split('; ')
        for author in article_authors:
            position = article_authors.index(author)
            author = author.replace(',', '')
            first_name = author.split(' ')[0].capitalize()
            last_name = author.split(' ')[1].capitalize()
            name = first_name + ' ' + last_name
            output.write(f'{id}\t{position}\t{name}\n')

def parse_author_keywords(id, article, output):
    if getattr(article, author_keywords) != '':
        article_author_keywords = getattr(article, author_keywords).split('; ')
        for keyword in article_author_keywords:
            output_keyword = keyword.upper()
            output.write(f'{id}\tAK\t{output_keyword}\n')

def parse_isi_keywords(id, article, output):
    if getattr(article, keywords_plus) != '':
        isi_keywords = getattr(article, keywords_plus).split('; ')
        for keyword in isi_keywords:
            output_keyword = keyword.upper()
            output.write(f'{id}\tIK\t{output_keyword}\n')

def parse_title_keywords(id, article, output):
    if getattr(article, document_title) != '':
        title_keywords = getattr(article, document_title)
        #remove punctuation w/ regex
        regex = re.compile('[%s]' % re.escape(string.punctuation))
        title_keywords = regex.sub('', title_keywords)
        for keyword in title_keywords.split(' '):
            output_keyword = keyword.upper()
            if keyword.lower() not in CONFIG['common_words'] and keyword != '':
                output.write(f'{id}\tTK\t{output_keyword}\n')

def parse_subjects(id, article, output):
    if getattr(article, wos_categories) != '':
        article_subjects = getattr(article, wos_categories).split('; ')
        for subject in article_subjects:
            output.write(f'{id}\t{subject}\n')

def parse_references(id, article, collection_references, output):
    computed_refs = 0
    computed_corrupt_refs = 0
    if getattr(article, cited_references) != '':
         article_refs = getattr(article, cited_references).split('; ')
         for article_ref in article_refs:
            ref = utility.Utility.new_object('refs', article_ref)
            computed_refs += 1

            if ref.year > 0:
                output.write(f"{id}\t{ref.firstAU}\t{ref.year}\t\
                               {ref.journal}\t{ref.volume}\t{ref.page}\n")
            elif ref.year == 0:
                computed_corrupt_refs += 1
    return (computed_refs, computed_corrupt_refs)

def parse_countries_and_institutions(id, article, f_institutions, f_countries, usa_country_codes_storage):
    if(getattr(article, author_address) != ""):
        addresses = getattr(article, author_address)
        regex = re.compile('\[(.*?)\]', re.IGNORECASE)
        addresses = regex.sub('', addresses)

        address_list = addresses.split('; ')

        for address in address_list:
            split_address = address.split(', ')
            institution = split_address[0]
            country = split_address[-1]
            position = address_list.index(address)

            #filter USA
            country_list = country.split(' ')
            if country_list[-1] == 'USA':
                country = country_list[-1]

            f_institutions.write(f'{id}\t{position}\t{institution}\n')
            f_countries.write(f'{id}\t{position}\t{country}\n')

def all_txt_files(directory):
    reg_ex = "%s/*.txt" % directory
    return glob.glob(reg_ex)

def open_dat_files(out_dir):
    return { "articles": open(os.path.join(out_dir, "articles.dat"),'w'),
    "authors": open(os.path.join(out_dir, "authors.dat"), 'w'),
    "title_keywords" : open(os.path.join(out_dir, "title_keywords.dat"), 'w'),
    "article_keywords" : open(os.path.join(out_dir, "article_keywords.dat"), 'w'),
    "isi_keywords" : open(os.path.join(out_dir, "isi_keywords.dat"), 'w'),
    "subjects" : open(os.path.join(out_dir, "subjects.dat"), 'w'),
    "refs" : open(os.path.join(out_dir, "references.dat"), 'w'),
    "countries": open(os.path.join(out_dir, "countries.dat"), 'w'),
    "institutions" : open(os.path.join(out_dir, "institutions.dat"), 'w'),
    }

def close_dat_files(open_dat_files):
    for key in open_dat_files:
        open_dat_files[key].close()

def parse_all_criteria(id, article, dat_files):
    parse_article(id, article, dat_files["articles"])
    parse_authors(id, article, dat_files["authors"])
    parse_author_keywords(id, article, dat_files["article_keywords"])
    parse_isi_keywords(id, article, dat_files["isi_keywords"])
    parse_title_keywords(id, article, dat_files["title_keywords"])
    parse_subjects(id, article, dat_files["subjects"])

def wos_parser(in_dir, out_dir, verbose):
    id = int(-1)

    dat_files = open_dat_files(out_dir)

    f_articles = dat_files["articles"]
    f_authors = dat_files["authors"]
    f_title_keywords = dat_files["title_keywords"]
    f_article_keywords = dat_files["article_keywords"]
    f_isi_keywords = dat_files["isi_keywords"]
    f_subjects = dat_files["subjects"]
    f_refs = dat_files["refs"]
    f_countries = dat_files["countries"]
    f_institutions = dat_files["institutions"]

    computed_refs = 0
    computed_corrupt_refs = 0

    WOS_IDS = dict()  # list the articles' wos-ids
    collection = utility.Utility.collection

    for src in all_txt_files(in_dir):
        utility.Utility.init_wos(src)
        if verbose:
            print("..processing %d articles in file %s" % (len(collection['woslines']), src))
        if (len(collection['woslines']) > 0):
            for article in collection['woslines']:

              if getattr(article, CONFIG['accession_number']) not in WOS_IDS:
                WOS_IDS[getattr(article, CONFIG['accession_number'])] = ''
                id = id + 1

                parse_all_criteria(id, article, dat_files)
                parsed_references_stats = parse_references(id, article, collection["references"], f_refs)
                computed_refs = parsed_references_stats[0]
                computed_corrupt_refs = parsed_references_stats[1]

                parse_countries_and_institutions(id, article, f_institutions, f_countries, CONFIG["usa_country_codes"])

        # Reset collection to avoid corrupted span files
        collection["articles"] = []
        collection["references"] = []
        collection["woslines"] = []

    if verbose:
        print(("..%d parsed articles in total") % (id + 1))
        print(("..%d inadequate refs out of %d (%f%%) have been rejected by this parsing process (no publication year, unpublished, ...) ") % (computed_corrupt_refs, computed_refs, (100.0 * computed_corrupt_refs) / computed_refs if computed_refs != 0 else 0))

    close_dat_files(dat_files)
    return
