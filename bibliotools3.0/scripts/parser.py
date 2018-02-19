"""
   Author : Sebastian Grauwin (http://www.sebastian-grauwin.com/)
   Copyright (C) 2012
   All rights reserved.
   BSD license.
   .... If you are using these scripts, please cite our "Scientometrics" paper:
   .... S Grauwin, P Jensen, Mapping Scientific Institutions. Scientometrics 89(3), 943-954 (2011)
"""

import os
import sys
import glob
import argparse
import utility

common_words = ['a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also', 'am', 'among', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'but', 'by', 'can', 'cannot', 'could', 'dear', 'did', 'do', 'does', 'either', 'else', 'ever', 'every', 'for', 'from', 'get', 'got', 'had', 'has', 'have', 'he', 'her', 'hers', 'him', 'his', 'how', 'however', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'just', 'least', 'let', 'like', 'likely', 'may', 'me', 'might', 'most', 'must', 'my', 'neither', 'no', 'nor', 'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our', 'own', 'rather', 'said', 'say', 'says', 'she', 'should', 'since', 'so', 'some', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas', 'us', 'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'yet', 'you', 'your']

punctuation = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', ' - ']

"""
# TODO Use config file accessors instead when the config file is working!
accession_number = 'UT'
authors = 'AU'
author_keywords = 'DE'
keywords_plus = 'ID'
document_title = 'TI'
wos_categories = 'WC'
cited_references = 'CR'
author_address = 'C1'
year_published = 'PY'
twenty_nine_character_source_abbreviation = 'J9'
volume = 'VL'
beginning_page = 'BP'
doi = 'DI'
publication_type = 'PT'
document_type = 'DT'
wos_core_collection_times_cited = 'TC'
"""

def Wos_parser(in_dir, out_dir, verbose):

    # Initialisation
    if verbose: print("..Analysing files %s/*.txt" %in_dir)

    srccomp = "%s/*.txt" % in_dir
    srclst = glob.glob(srccomp)
    id = int(-1)
   
    utility = utility.Utility(srclst)
"""
    dst1  = os.path.join(out_dir, "articles.dat")
    f_articles = open(dst1,'w')

    dst2  = os.path.join(out_dir, "authors.dat")
    f_authors = open(dst2,'w')

    dst31  = os.path.join(out_dir, "title_keywords.dat")
    f_title_keywords = open(dst31,'w')

    dst32  = os.path.join(out_dir, "article_keywords.dat")
    f_article_keywords = open(dst32,'w')

    dst33  = os.path.join(out_dir, "isi_keywords.dat")
    f_isi_keywords = open(dst33,'w')

    dst4  = os.path.join(out_dir, "subjects.dat")
    f_subjects = open(dst4,'w')

    dst5  = os.path.join(out_dir, "references.dat")
    f_refs = open(dst5,'w')

    dst6  = os.path.join(out_dir, "countries.dat")
    f_countries = open(dst6,'w')

    dst7  = os.path.join(out_dir, "institutions.dat")
    f_institutions = open(dst7,'w')

    kompt_refs = 0
    kompt_corrupt_refs = 0

    WOS_IDS = dict()  # list the articles' wos-ids

    # Treat Data
    for src in srclst:
        pl = Utils.ArticleList()
        pl.read_file(src)
        if verbose:
            print("..processing %d articles in file %s" % (len(pl.articles), src))
        if (len(pl.articles) > 0):
            for article in pl.articles:

              if getattr(article, accession_number) not in WOS_IDS:
                WOS_IDS[getattr(article, accession_number)] = ''
                id = id + 1

                #article
                article_authors = getattr(article, authors).split('; ')
                firstAU = article_authors[0].replace(',','')
                f_articles.write("%d\t%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (id,firstAU,getattr(article, year_published),getattr(article, twenty_nine_character_source_abbreviation),getattr(article, volume),getattr(article, beginning_page),getattr(article, doi),getattr(article, publication_type),getattr(article, document_type),getattr(article, wos_core_collection_times_cited),getattr(article, document_title),getattr(article, accession_number)))

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
                    for p in punctuation: article_author_keywords = article_author_keywords.replace(p,'')
                    article_author_keywords = article_author_keywords.split(' ')
                    for f in article_author_keywords:
                      lowercase = f.lower()
                      if lowercase not in common_words and len(lowercase)>0:
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
                         ref = Utils.Ref()
                         ref.parse_ref(article_refs[i])
                         kompt_refs += 1
                         if(ref.year > 0):
                             f_refs.write("%d\t%s\t%d\t%s\t%s\t%s\n" % (id,ref.firstAU,ref.year,ref.journal,ref.volume,ref.page))
                         if(ref.year == 0): kompt_corrupt_refs += 1

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

                        if (country[length_split_address-3:length_split_address] == 'USA' or country[0:3] == 'AL ' or country[0:3] == 'AK ' or country[0:3] == 'AZ ' or country[0:3] == 'AR ' or country[0:3] == 'CA ' or country[0:3] == 'NC ' or country[0:3] == 'SC ' or country[0:3] == 'CO ' or country[0:3] == 'CT ' or country[0:3] == 'ND ' or country[0:3] == 'SD ' or country[0:3] == 'DE ' or country[0:3] == 'FL ' or country[0:3] == 'GA ' or country[0:3] == 'HI ' or country[0:3] == 'ID ' or country[0:3] == 'IL ' or country[0:3] == 'IN ' or country[0:3] == 'IA ' or country[0:3] == 'KS ' or country[0:3] == 'KY ' or country[0:3] == 'LA ' or country[0:3] == 'ME ' or country[0:3] == 'MD ' or country[0:3] == 'MA ' or country[0:3] == 'MI ' or country[0:3] == 'MN ' or country[0:3] == 'MS ' or country[0:3] == 'MO ' or country[0:3] == 'MT ' or country[0:3] == 'NE ' or country[0:3] == 'NV ' or country[0:3] == 'NH ' or country[0:3] == 'NJ ' or country[0:3] == 'NM ' or country[0:3] == 'NY ' or country[0:3] == 'OH ' or country[0:3] == 'OK ' or country[0:3] == 'or ' or country[0:3] == 'PA ' or country[0:3] == 'RI ' or country[0:3] == 'TN ' or country[0:3] == 'TX ' or country[0:3] == 'UT ' or country[0:3] == 'VT ' or country[0:3] == 'VA ' or country[0:3] == 'WV ' or country[0:3] == 'WA ' or country[0:3] == 'WI ' or country[0:3] == 'WY ' or country[0:3] == 'DC '): country = 'USA'

                        f_countries.write("%d\t%d\t%s\n" % (id,i,country))
"""
    """
    if verbose: print(("..%d parsed articles in total") % (id + 1))
    if verbose: print(("..%d inadequate refs out of %d (%f%%) have been rejected by this parsing process (no publication year, unpublished, ...) ") % (kompt_corrupt_refs, kompt_refs, (100.0 * kompt_corrupt_refs) / kompt_refs if kompt_refs!=0 else 0))

    f_articles.close()
    f_authors.close()
    f_article_keywords.close()
    f_title_keywords.close()
    f_isi_keywords.close()
    f_subjects.close()
    f_refs.close()
    f_countries.close()
    f_institutions.close()
    """
    return
