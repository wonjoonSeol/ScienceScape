#! /usr/bin/env python

class Keyword:
    self.id      = 0
    self.ktype   = ""       
    self.keyword = ""


    def __init__(self, data):
        self.id = int(data[0])
        self.ktype = data[1]
        self.keyword = data[2].upper()  


