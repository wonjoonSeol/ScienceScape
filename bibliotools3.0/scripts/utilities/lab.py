#! /usr/bin/env python

class Lab:
    self.id = 0      
    self.lab = ""

    def __init__(self, data):
       if len(data) == 2:
          self.id = int(data[0])
          self.lab = data[1]
   


