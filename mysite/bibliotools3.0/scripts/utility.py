#! /usr/bin/env python

#outer modules
import os
import sys
import glob
import numpy
import argparse
import re

#personal modules
import utilities


"""
This class contains logic for various utilities used thoughout the scripts.
It has a collection of data parsed from the wos text files.
"""
class Utility:
    __articles = []
    __refs = []
    __woslines = []

    #dictionary for all the objects
    collection = { 'articles': __articles , 'references' : __refs,
                    'woslines' : __woslines }

    """ Return a filename with extension removed. """
    def file_name(file_path):
        base = os.path.basename(file_path)
        return os.path.splitext(base)[0]

    """
    Take a WOS .txt file as source and create a WOS Line in the collection.
    """
    def init_wos(src):
        with open(src) as f:
            content = [x.strip('\n') for x in f.readlines()]
            has_header = False
            for line in content:
                if line != "":
                    re_line = line.replace('\xef\xbb\xbf','').split('\t')
                    if not has_header: # define columns thanks to 1st line
                        from utilities import wosline
                        (def_cols, num_cols) = wosline.defColumns(re_line)
                        has_header = True
                    elif has_header: # do not take 1st line into account!
                        Utility.collection['woslines'].append(wosline.Wosline(re_line, def_cols, num_cols))

    """ Return the created item.
    A factory that creates items based on a given name. It passes the given
    line to its constructor.
    """
    def new_object(object_name, line):
        if(object_name == 'articles'):
            from utilities import article
            return article.Article(line)
        elif(object_name == 'refs'):
            from utilities import ref
            return ref.Ref(line)
        elif(object_name == 'woslines'):
            from utilities import wosline
            return wosline.WosLine(line)

    """
    	Sets all the collection to empty lists.
    """
    def reset():
        Utility.collection["articles"] = []
        Utility.collection["references"] = []
        Utility.collection["woslines"] = []
