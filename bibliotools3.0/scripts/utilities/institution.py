#! /usr/bin/env python

class Institution:
   def __init__(self, data):
        self.id = 0
        self.rank = 0       
        self.institution = ""
        if len(data) == 3:
            self.id = int(data[0])
            self.rank = int(data[1])
            self.institution = data[2].upper()  




