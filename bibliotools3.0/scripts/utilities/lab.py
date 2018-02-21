#! /usr/bin/env python

class Lab:
    def __init__(self, data):
        self.id = 0      
        self.lab = ""

        if len(data) == 2:
            self.id = int(data[0])
            self.lab = data[1]
   
	def __str__(self):
        return 'lab no ' + id + ': ' + lab + '\n'

