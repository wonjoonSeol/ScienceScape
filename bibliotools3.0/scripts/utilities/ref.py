#! /usr/bin/env python

class Ref:

    def __init__(self, line):

        self.id      = 0
        self.firstAU = ""
        self.year    = 0
        self.journal = ""
        self.volume  = 0
        self.page    = 0

        self.parse_ref(line)

    #TODO see what this does in the grand scheme of things
    def parse_ref(self, ref):
        """
        parse a ref of the WoS txt format
        """
        s = ref.split(', ')

        if(len(s)>0):
            aux1 = s[0].rfind(' ')
            aux2 = len(s[0])
            foo = s[0].lower().capitalize()
            if aux1 > 0:
                s1 = foo[aux1:aux2]
                s2 = s1.upper()
                foo = foo.replace(s1,s2)
                foo = foo.replace('.','')
            self.firstAU = foo
        if(len(s)>1):
            if s[1].isdigit(): self.year = int(s[1])
            else:              self.year = 0
        if(len(s)>2): self.journal = s[2]
        if(len(s)>3):
            if(s[3][0]=='V'): self.volume  = s[3].replace('V','')
        if(len(s)>3):
            if(s[3][0]=='P'): self.page  = s[3].replace('P','')
        if(len(s)>4):
            if(s[4][0]=='P'): self.page  = s[4].replace('P','')
