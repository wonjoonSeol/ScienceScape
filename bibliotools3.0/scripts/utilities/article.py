#! /usr/bin/env python


class Article:
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

    def __init__(self, data):
        self.id = int(s[0])
        if(len(data)>1): self.firstAU = s[1]
        if(len(data)>2): self.year = int(s[2]) 
        if(len(data)>3): self.journal = s[3] 
        if(len(data)>4): self.volume = s[4] 
        if(len(data)>5): self.page = s[5] 
        if(len(data)>6): self.doi  = s[6]
        if(len(data)>7): self.pubtype = s[7]
        if(len(data)>8): self.doctype = s[8]
        if(len(data)>9): self.times_cited = s[9]
        if(len(data)>10): self.title = s[10]
        if(len(data)>11): self.uniqueID = s[11]
