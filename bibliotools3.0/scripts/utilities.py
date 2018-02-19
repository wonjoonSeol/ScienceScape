#! /usr/bin/env python

import os
import sys
import glob
import numpy
import argparse
import re

#personal modules
import utilities

class Utilities:
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
                object_name = Utilities.file_name(file_path)
                re_line = re.split(', | ', line)
                Utilities.collection[object_name].append(
                        Utilities.__new_object(object_name, re_line))
 
    
    def __init__(self, files_list):
        for path in files_list: 
            name = path.strip('.dat')
            print('name ' + name)
            Utilities.read_file(path, name)


   
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
            return WosLine(line)

def main():
    path_list = ['/Users/paul/testing/articles.dat']
    utilities = Utilities(path_list)
    print(Utilities.collection)

if __name__ == "__main__":
    main()
