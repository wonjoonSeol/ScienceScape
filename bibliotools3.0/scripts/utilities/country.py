#! /usr/bin/env python

class Country:
        self.id     = 0
        self.rank   = 0       
        self.country = ""
 
    def __init__(self, data):
        self.id = int(data[0])
        self.rank = int(data[1])
        self.country = data[2].lower().capitalize()  

 

