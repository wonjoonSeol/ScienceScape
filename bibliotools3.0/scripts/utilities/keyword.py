#! /usr/bin/env python

class Keyword:

    def __init__(self, data):
        self.id      = 0
        self.ktype   = ""       
        self.keyword = ""

        self.id = int(data[0])
        self.ktype = data[1]
        self.keyword = data[2].upper()  

def __str__(self):
        return 'keyword no ' + id + ': ' + keyword + '\n'
