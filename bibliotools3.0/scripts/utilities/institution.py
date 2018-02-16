#! /usr/bin/env python

class Institution:
        self.id = 0
        self.rank = 0       
        self.institution = ""

    def __init__(self, data):
        if len(data) == 3:
          self.id = int(data[0])
          self.rank = int(data[1])
          self.institution = data[2].upper()  




