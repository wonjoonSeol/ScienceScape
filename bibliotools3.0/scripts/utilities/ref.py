#! /usr/bin/env python

"""
A class that holds the data from a parsed reference.
"""
class Ref:

    def __init__(self, line):

        self.id      = 0
        self.firstAU = ""
        self.year    = 0
        self.journal = ""
        self.volume  = 0
        self.page    = 0

        self.parse_ref(line)

    """
        Parse the given ref line and store in the object.
    """
    def parse_ref(self, ref):
        ref = ref.split(', ')
        if len(ref) > 0:
            self.firstAU = ref[0].replace('.', '')
        if len(ref) > 1:
            if ref[1].isdigit():
                self.year = int(ref[1])
            else:
                self.year = 0
        if len(ref) > 2:
            self.journal = ref[2]
        if len(ref) > 3:
            if ref[3][0] == 'V':
                self.volume  = ref[3].replace('V','')
            elif ref[3][0] == 'P':
                self.page  = ref[3].replace('P','')
        if len(ref)>4:
            if ref[4][0] == 'P' : self.page  = ref[4].replace('P','')
