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
    #list for all the utily objects
    __articles = []
    __authors = []
    __countries = []
    __institutions = []
    __keywords = []
    __labs = []
    __refs = []
    __subjects = []

    __woslines = []

    #dictionary for all the objects
    collection = { 'articles': __articles , 'authors' : __authors, 
            'countries' : __countries, 'institutions' : __institutions, 
            'keywords' : __keywords, 'labs' : __labs, 'refs' : __refs, 
            'subjects' : __subjects, 'woslines' : __woslines }

    def file_name(file_path):
        base = os.path.basename(file_path)
        return os.path.splitext(base)[0]

    def read_file(file_path, object_name):
        with open(file_path) as f:
            content = [x.strip('\n') for x in f.readlines()]
            for line in content: 
                #parse line based on object type
                object_name = Utility.file_name(file_path)
                re_line = re.split(', | ', line)
                Utility.collection[object_name].append(
                        Utility.__new_object(object_name, re_line))
 



     def init_wos(source_list):
         #call parser here to create .dat files
        ''' for src in srclst:
            Utility.read_file(src, 'woslines')
            
            if len(__woslines) > 0:
                for wosline in __woslines:
                    parse_wosline();
        '''

     def init_utilites(source_list):
         #after we have .dat files created by parser, use utility to store them
         #in the collection
         for path in files_list: 
            name = path.strip('.dat')
            print('name ' + name)
            Utility.read_file(path, name)


    def __init__(self, srclines):
          
   
    def __new_object(object_name, line):
        if(object_name == 'articles'):
            from utilities import article
            return article.Article(line)
        elif(object_name == 'authors'):
            from utilites import author
            return author.Author(line)
        elif(object_name == 'countries'):
            from utilites import country
            return country.Country(line)
        elif(object_name == 'institutions'):
            from utilites import institution 
            return institution.Institution(line)
        elif(object_name == 'keywords'):
            from utilites import keyword 
            return keyword.Keyword(line)
        elif(object_name == 'labs'):
            from utilities import lab 
            return keyword.Lab(line)
        elif(object_name == 'refs'):
            from utilities import ref 
            return ref.Ref(line)
        elif(object_name == 'subjects'):
            from utilities import subject 
            return subject.Subject(line)
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
