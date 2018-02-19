#! /usr/bin/env python

import os
import sys
import glob
import numpy
import argparse
import re

#personal modules
import utilities

class Utility:
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

#    #list for all the utily objects
#   __articles = []
#    __authors = []
#    __countries = []
#    __institutions = []
#    __keywords = []
#    __labs = []
#    __refs = []
#    __subjects = []
    __woslines = []
    __parsed_woslines = [] 
#    #dictionary for all the objects
#    collection = { 'articles': __articles , 'authors' : __authors, 
#            'countries' : __countries, 'institutions' : __institutions, 
#            'keywords' : __keywords, 'labs' : __labs, 'refs' : __refs, 
#            'subjects' : __subjects, 'woslines' : __woslines }
#
#    def file_name(file_path):
#        base = os.path.basename(file_path)
#        return os.path.splitext(base)[0]
#
    def read_file(file_path, object_name):
        with open(file_path) as f:
            content = [x.strip('\n') for x in f.readlines()]
            for line in content: 
               #parse line based on object type
                object_name = Utility.file_name(file_path)
                re_line = re.split(', | ', line)
                Utility.collection[object_name].append(
                        Utility.__new_object(object_name, re_line))
 
    
    def __init__(self, srclines):
        self.counter = 0
        for src in srclst:
            Utility.read_file(src, 'woslines')
            
            if len(__woslines) > 0:
                for wosline in __woslines:
                    parse_wosline();

    def parse_wosline(line):
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


        if getattr(line, accession_number) not in __parse_woslines:
            __parsed_woslines.append(getattr(line, accession_number))
            counter = counter + 1
            #line
            line_authors = getattr(line, authors).split('; ')
            firstAU = line_authors[0].replace(',','')
            f_lines.write("%d\t%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (id,firstAU,getattr(line, year_published),getattr(line, twenty_nine_character_source_abbreviation),getattr(line, volume),getattr(line, beginning_page),getattr(line, doi),getattr(line, publication_type),getattr(line, document_type),getattr(line, wos_core_collection_times_cited),getattr(line, document_title),getattr(line, accession_number)))

                #authors
                if(getattr(line, authors) != ""):
                    line_authors = getattr(line, authors).split('; ')
                    for i in range(len(line_authors)):
                        line_authors[i] = line_authors[i].replace(',','')
                        aux1 = line_authors[i].rfind(' ')
                        aux2 = len(line_authors[i])
                        authors_lowercase = line_authors[i].lower().capitalize()
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
                if(getattr(line, author_keywords) != ""):
                    line_author_keywords = getattr(line, author_keywords).split('; ')
                    for f in line_author_keywords:
                        f_line_keywords.write("%d\tAK\t%s\n" % (id,f.upper()))
                if(getattr(line, keywords_plus) != ""):
                    line_author_keywords = getattr(line, keywords_plus).split('; ')
                    for f in line_author_keywords:
                        f_isi_keywords.write("%d\tIK\t%s\n" % (id,f.upper()))
                if(getattr(line, document_title) != ""):
                    line_author_keywords = getattr(line, document_title)
                    #... remove ponctuations !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
                    for p in punctuation: line_author_keywords = line_author_keywords.replace(p,'')
                    line_author_keywords = line_author_keywords.split(' ')
                    for f in line_author_keywords:
                      lowercase = f.lower()
                      if lowercase not in common_words and len(lowercase)>0:
                        f_title_keywords.write("%d\tTK\t%s\n" % (id, lowercase.upper()))

                #subjects
                if(getattr(line, wos_categories) != ""):
                    line_wos_cat = getattr(line, wos_categories).split('; ')
                    for i in range(len(line_wos_cat)):
                        f_subjects.write("%d\t%s\n" % (id,line_wos_cat[i]))

                #references
                if(getattr(line, cited_references) != ""):
                     line_refs = getattr(line, cited_references).split('; ')
                     for i in range(len(line_refs)):
                         ref = Utils.Ref()
                         ref.parse_ref(line_refs[i])
                         kompt_refs += 1
                         if(ref.year > 0):
                             f_refs.write("%d\t%s\t%d\t%s\t%s\t%s\n" % (id,ref.firstAU,ref.year,ref.journal,ref.volume,ref.page))
                         if(ref.year == 0): kompt_corrupt_refs += 1

                #countries / institutions
                if(getattr(line, author_address) != ""):
                    address = getattr(line, author_address)
                    aux1 = address.find('[')
                    aux2 = address.find(']')

                    while (aux1 < aux2):
                        aux = address[aux1:aux2+2]
                        address = address.replace(aux,''):qrhsgw[;]];];        
            f_articles.close()
            f_authors.close()
            f_article_keywords.close()
            f_title_keywords.close()
            f_isi_keywords.close()
            f_subjects.close()
            f_refs.close()
            f_countries.close()
            f_institutions.close()

#        for path in files_list: 
#            name = path.strip('.dat')
#            print('name ' + name)
#            Utility.read_file(path, name)
#
#
#   
    def __new_object(object_name, line):
        if(object_name == 'articles'):
            from utilities import article
            return article.Article(line)
        elif(object_name == 'authors'):
          return Author(line)
        elif(object_name == 'countries'):
          return Country(line)
        elif(object_name == 'institutions'):
          return Institution(line)
        elif(object_name == 'keywords'):
          return Keyword(line)
        elif(object_name == 'labs'):
          return Lab(line)
        elif(object_name == 'refs'):
            return Ref(line)
        elif(object_name == 'subjects'):
            return Subject(line)
        elif(object_name == 'woslines'):
            from utilities import wosline
            return wosline.WosLine(line)
#
#def main():
#    path_list = ['/Users/paul/testing/articles.dat']
#    utilities = Utility(path_list)
#    print(Utility.collection)
#
#if __name__ == "__main__":
#    main()
