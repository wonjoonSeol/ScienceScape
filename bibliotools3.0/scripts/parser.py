import os
import sys
import glob
import argparse
import utility
from config import CONFIG

# TODO Link with config file
accession_number = CONFIG['accession-number']
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
    # Treat Data
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
                article_authors = getattr(article, CONFIG['authors']).split('; ')
                firstAU = article_authors[0].replace(',','')
                f_articles.write("%d\t%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" %
                    (id,firstAU,getattr(article, year_published),
                    getattr(article, twenty_nine_character_source_abbreviation),
                    getattr(article, volume), getattr(article, beginning_page),
                    getattr(article, doi), getattr(article, publication_type),
                    getattr(article, document_type), getattr(article, wos_core_collection_times_cited),
                    getattr(article, document_title), getattr(article, CONFIG['accession_number'])))

                #authors
                if(getattr(article, authors) != ""):
                    article_authors = getattr(article, authors).split('; ')
                    for i in range(len(article_authors)):
                        article_authors[i] = article_authors[i].replace(',','')
                        aux1 = article_authors[i].rfind(' ')
                        aux2 = len(article_authors[i])
                        authors_lowercase = article_authors[i].lower().capitalize()
                        if aux1 > 0:
                            s1 = authors_lowercase[aux1:aux2]
                            s2 = s1.upper()
                            authors_lowercase = authors_lowercase.replace(s1,s2)
                        aux = authors_lowercase.find('-')
                        if aux > 0:
                            bar1 = authors_lowercase[aux:aux+2]
                            bar2 = '-' + authors_lowercase[aux+1].upper()
                            authors_lowercase = authors_lowercase.replace(bar1,bar2)
                        aux = authors_lowercase.find(' ')
                        if aux > 0:
                            bar1 = authors_lowercase[aux:aux+2]
                            bar2 = ' ' + authors_lowercase[aux+1].upper()
                            authors_lowercase = authors_lowercase.replace(bar1,bar2)
                        f_authors.write("%d\t%d\t%s\n" % (id,i,authors_lowercase)) 

                #keywords
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
                    #... remove ponctuations !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
                    for p in CONFIG['punctuation']: article_author_keywords = article_author_keywords.replace(p,'')
                    article_author_keywords = article_author_keywords.split(' ')
                    for f in article_author_keywords:
                        lowercase = f.lower()
                        if lowercase not in CONFIG['common_words'] and len(lowercase)>0:
                            f_title_keywords.write("%d\tTK\t%s\n" % (id, lowercase.upper()))

                #subjects
                if(getattr(article, wos_categories) != ""):
                    article_wos_cat = getattr(article, wos_categories).split('; ')
                    for i in range(len(article_wos_cat)):
                        f_subjects.write("%d\t%s\n" % (id,article_wos_cat[i]))

                #references
                if(getattr(article, cited_references) != ""):
                     article_refs = getattr(article, cited_references).split('; ')
                     for i in range(len(article_refs)):
                        ref = utility.Utility.new_object('refs', article_refs[i])
                        collection['references'].append(ref)
                        computed_refs += 1
                        
                        if(ref.year > 0):
                            f_refs.write("%d\t%s\t%d\t%s\t%s\t%s\n" %
                                     (id,ref.firstAU,ref.year,ref.journal,ref.volume,ref.page))
                        if(ref.year == 0): computed_corrupt_refs += 1

                #countries / institutions
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

                        if  country[length_split_address-3 : length_split_address] == 'USA' or country[0:3] in CONFIG['usa_country_codes']:
                                f_countries.write("%d\t%d\t%s\n" % (id,i,country))

    # End
    if verbose: print(("..%d parsed articles in total") % (id + 1))
    if verbose: print(("..%d inadequate refs out of %d (%f%%) have been rejected by this parsing process (no publication year, unpublished, ...) ") % (computed_corrupt_refs, computed_refs, (100.0 * computed_corrupt_refs) / computed_refs if computed_refs!=0 else 0))
    files_list = [f_articles.name, f_authors.name, f_isi_keywords.name, 
                    f_subjects.name, f_article_keywords.name, f_title_keywords.name, 
                    f_refs.name, f_countries.name, f_institutions.name]

    #generate items from parsed .dat files and add the to the collection
    utility.Utility.init_utilities(files_list)


    #close the files   
    closeList = [f_articles, f_authors, f_article_keywords, f_title_keywords, f_isi_keywords, f_subjects, f_refs, f_countries, f_institutions]
    for d in closeList:
        d.close()

    return
