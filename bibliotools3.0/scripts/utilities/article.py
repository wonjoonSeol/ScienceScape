#! /usr/bin/env python


class Article:

    def __init__(self, data):
        self.id          = 0
        self.firstAU     = ""       
        self.year        = 0
        self.journal     = ""
        self.volume      = ""
        self.page        = ""
        self.doi         = ""
        self.pubtype     = ""
        self.doctype     = ""
        self.times_cited = ""
        self.title       = ""
        self.uniqueID    = ""

        self.id = int(data[0])
        if(len(data)>1): self.firstAU = data[1]
        if(len(data)>2): self.year = int(data[2]) 
        if(len(data)>3): self.journal = data[3] 
        if(len(data)>4): self.volume = data[4] 
        if(len(data)>5): self.page = data[5] 
        if(len(data)>6): self.doi  = data[6]
        if(len(data)>7): self.pubtype = data[7]
        if(len(data)>8): self.doctype = data[8]
        if(len(data)>9): self.times_cited = data[9]
        if(len(data)>10): self.title = data[10]
        if(len(data)>11): self.uniqueID = data[11]
