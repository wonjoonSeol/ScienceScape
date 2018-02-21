#! /usr/bin/env python

class Subject:
    def __init__(self, data):
        self.id      = 0
        self.subject = ""       

        self.id = int(data[0])
        self.subject = data[1] 

	def __str__(self):
        return 'subject no ' + id + ': ' + subject + '\n'