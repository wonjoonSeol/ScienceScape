#! /usr/bin/env python

import os
import sys
import glob
import numpy
import argparse

#personal modules
import utilies

class Utilities:
    #list for all the utily objects
    self.__articles = []
    self.__authors = []
    self.__countries = []
    self.__institutions = []
    self.__keywords = []
    self.__labs = []
    self.__refs = []
    self.__subjects = []
    self.__woslines = []
   
    #dictionary for all the objects
    self.collection = { 'articles': articles , 'authors' : authors, 
            'countries' : countries, 'institutions' : institutions, 
            'keywords' : keywords, 'labs' : labs, 'refs' : refs, 
            'subjects' : subjects, 'woslines' : woslines }

    
    def __init__(self, files_list):
        for(path in files_list): 
            name = path.strip('.dat')
            read_file(path, name)


    def read_file(self, filename, object_name):
        with open(filename) as f:
            content = [x.strip('\n') for x in f.readlines()]
            for(line in content): 
                collection[object_name].append(new_object(object_name, line))
    
    
    def __new_object(object_name, line):
        if(object_name == 'articles'):
          return Article(line)
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
        elif(object_name = 'woslines'):
            return WosLine(line)


if __name__ == "__main__":
    main()
