#! /usr/bin/env python

class Country:

    def __init__(self, data):
        self.id     = 0
        self.rank   = 0       
        self.country = ""

        self.id = int(data[0])
        self.rank = int(data[1])
        self.country = data[2].lower().capitalize()  

	def __str__(self):
        return 'country no ' + id + ': ' + country + '\n' 

