import os
import sys
import glob
import argparse
import utility
from config import CONFIG

# TODO Link with config file
accession_number = CONFIG['accession_number']
authors = CONFIG['authors']
author_keywords = CONFIG['author_keywords']
keywords_plus = CONFIG['keywords_plus']
document_title = CONFIG['document_title']
wos_categories = CONFIG['wos_categories']
cited_references = CONFIG['cited_references']
author_address = CONFIG['author_address']
year_published = CONFIG['year_published']
twenty_nine_character_source_abbreviation = CONFIG['twenty_nine_character_source_abbreviation']
volume = CONFIG['volume']
beginning_page = CONFIG['beginning_page']
doi = CONFIG['doi']
publication_type = CONFIG['publication_type']
document_type = CONFIG['document_type']
wos_core_collection_times_cited = CONFIG['wos_core_collection_times_cited']

def parse_article(id, article, output):
    print(str(id) + 'im here')
    article_authors = getattr(article, authors).split('; ')
    firstAU = article_authors[0].replace(',','')
    output.write("%d\t%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" %
        (id,firstAU,getattr(article, year_published),
        getattr(article, twenty_nine_character_source_abbreviation),
        getattr(article, volume), getattr(article, beginning_page),
        getattr(article, doi), getattr(article, publication_type),
        getattr(article, document_type), getattr(article, wos_core_collection_times_cited),
        getattr(article, document_title), getattr(article, accession_number)))


def parse_authors(id, article, output):
    if getattr(article, authors) != '':
        article_authors = getattr(article, authors).split('; ')

        for i in range(len(article_authors)):
            article_authors[i] = article_authors[i].replace(',','')
            first_name = article_authors[i].split(' ')[0].capitalize()
            last_name = article_authors[i].split(' ')[1].capitalize()
            name = first_name + ' ' + last_name
            output.write(f'{id}\t{i}\t{name}\n')

def parse_keywords(id, article, f_article_keywords, f_isi_keywords, f_title_keywords, punctuation_storage, common_words_storage):
    if(getattr(article, author_keywords) != ""):
        article_author_keywords = getattr(article, author_keywords).split('; ')
        for f in article_author_keywords:
            f_article_keywords.write("%d\tAK\t%s\n" % (id,f.upper()))
    if(getattr(article, keywords_plus) != ""):
        article_author_keywords = getattr(article, keywords_plus).split('; ')
        for f in article_author_keywords:
            f_isi_keywords.write("%d\tIK\t%s\n" % (id,f.upper()))
    if(getattr(article, document_title) != ""):
        article_author_keywords = getattr(article, document_title)
        #... remove punctuations !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
        for p in punctuation_storage: article_author_keywords = article_author_keywords.replace(p,'')
        article_author_keywords = article_author_keywords.split(' ')
        for f in article_author_keywords:
            lowercase = f.lower()
            if lowercase not in common_words_storage and len(lowercase)>0:
                f_title_keywords.write("%d\tTK\t%s\n" % (id, lowercase.upper()))

def parse_subjects(id, article, output):
    if(getattr(article, wos_categories) != ""):
        article_wos_cat = getattr(article, wos_categories).split('; ')
        for i in range(len(article_wos_cat)):
            output.write("%d\t%s\n" % (id,article_wos_cat[i]))


def parse_references(id, article, collection_references, output):
    computed_refs_local = 0
    computed_corrupt_refs_local = 0
    if(getattr(article, cited_references) != ""):
         article_refs = getattr(article, cited_references).split('; ')
         for i in range(len(article_refs)):
            ref = utility.Utility.new_object('refs', article_refs[i])
            collection_references.append(ref)
            computed_refs_local += 1

            if(ref.year > 0):
                output.write("%d\t%s\t%d\t%s\t%s\t%s\n" %
                         (id,ref.firstAU,ref.year,ref.journal,ref.volume,ref.page))
            if(ref.year == 0): computed_corrupt_refs_local += 1
    return (computed_refs_local, computed_corrupt_refs_local)

def parse_countries_and_institutions(id, article, f_institutions, f_countries, usa_country_codes_storage):
    if(getattr(article, author_address) != ""):
        address = getattr(article, author_address)
        aux1 = address.find('[')
        aux2 = address.find(']')

        while (aux1 < aux2):
            aux = address[aux1:aux2+2]
            address = address.replace(aux,'')
            aux1 = address.find('[')
            aux2 = address.find(']')

        article_address = address.split('; ')
        for i in range(len(article_address)):
            article_address[i] = article_address[i].replace(', ', ',')
            split_address = article_address[i].split(',')
            length_of_address = len(split_address)

            for j in range(length_of_address - 2):
                f_institutions.write("%d\t%d\t%s\n" % (id,i,split_address[j]))

            country = split_address[length_of_address-1]
            length_split_address = len(split_address[length_of_address-1])

            if  country[length_split_address-3 : length_split_address] == 'USA' or country[0:3] in usa_country_codes_storage:
                    f_countries.write("%d\t%d\t%s\n" % (id,i,country))

def Wos_parser(in_dir, out_dir, verbose):

    # Initialisation
    srccomp = "%s/*.txt" % in_dir
    srclst = glob.glob(srccomp)
    id = int(-1)

    f_articles = open(os.path.join(out_dir, "articles.dat"),'w')
    f_authors = open(os.path.join(out_dir, "authors.dat"), 'w')
    f_title_keywords = open(os.path.join(out_dir, "title_keywords.dat"), 'w')
    f_article_keywords = open(os.path.join(out_dir, "article_keywords.dat"), 'w')
    f_isi_keywords = open(os.path.join(out_dir, "isi_keywords.dat"), 'w')
    f_subjects = open(os.path.join(out_dir, "subjects.dat"), 'w')
    f_refs = open(os.path.join(out_dir, "references.dat"), 'w')
    f_countries = open(os.path.join(out_dir, "countries.dat"), 'w')
    f_institutions = open(os.path.join(out_dir, "institutions.dat"), 'w')

    computed_refs = 0
    computed_corrupt_refs = 0

    WOS_IDS = dict()  # list the articles' wos-ids
    collection = utility.Utility.collection

    for src in srclst:
        utility.Utility.init_wos(src)

        if verbose:
            print("..processing %d articles in file %s" % (len(collection['woslines']), src))
        if (len(collection['woslines']) > 0):
            for article in collection['woslines']:

              if getattr(article, CONFIG['accession_number']) not in WOS_IDS:
                WOS_IDS[getattr(article, CONFIG['accession_number'])] = ''
                id = id + 1

                #article
                parse_article(id, article, f_articles)

                #authors
                parse_authors(id, article, f_authors)

                #keywords
                parse_keywords(id, article, f_article_keywords, f_isi_keywords, f_title_keywords, CONFIG['punctuation'], CONFIG['common_words'])

                #subjects
                parse_subjects(id, article, f_subjects)

                #references
                parsed_references_stats = parse_references(id, article, collection["references"], f_refs)
                computed_refs = parsed_references_stats[0]
                computed_corrupt_refs = parsed_references_stats[1]

                #countries / institutions
                parse_countries_and_institutions(id, article, f_institutions, f_countries, CONFIG["usa_country_codes"])

    # End
    if verbose: print(("..%d parsed articles in total") % (id + 1))
    if verbose: print(("..%d inadequate refs out of %d (%f%%) have been rejected by this parsing process (no publication year, unpublished, ...) ") % (computed_corrupt_refs, computed_refs, (100.0 * computed_corrupt_refs) / computed_refs if computed_refs!=0 else 0))
    files_list = [f_articles.name, f_authors.name, f_isi_keywords.name,
                    f_subjects.name, f_article_keywords.name, f_title_keywords.name,
                    f_refs.name, f_countries.name, f_institutions.name]


    #close the files
    closeList = [f_articles, f_authors, f_article_keywords, f_title_keywords, f_isi_keywords, f_subjects, f_refs, f_countries, f_institutions]
    for d in closeList:
        d.close()

    return
