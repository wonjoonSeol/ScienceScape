#! /usr/bin/env python

import os
import sys
import glob
import numpy
import argparse

class Wosline:
    
    def __init__(self):
        #TODO create a map which reads these values from an external file to
        # improve decoupling, readability and efficiency

        self.PT = "" ## Publication Type (J=Journal; B=Book; S=Series)
        self.AU = "" ## Authors
        self.BA = "" ## Book Authors
        self.BE = "" ## Book Editor
        self.GP = "" ## Book Group Authors
        self.AF = "" ## Author Full Name
        self.CA = "" ## Group Authors
        self.TI = "" ## Document Title
        self.SO = "" ## Publication Name
        self.SE = "" ## Book Series Title
        self.LA = "" ## Language
        self.DT = "" ## Document Type
        self.CT = "" ## Conference Title 
        self.CY = "" ## Conference Date 
        self.CL = "" ## Conference Location 
        self.SP = "" ## Conference Sponsors 
        self.FO = "" ## Funding Organization
        self.DE = "" ## Author Keywords
        self.ID = "" ## Keywords Plus
        self.AB = "" ## Abstract
        self.C1 = "" ## Author Address
        self.RP = "" ## Reprint Address
        self.EM = "" ## E-mail Address
        self.FU = "" ## Funding Agency and Grant Number
        self.FX = "" ## Funding Text
        self.CR = "" ## Cited References
        self.NR = "" ## Cited Reference Count
        self.TC = "" ## Times Cited
        self.Z9 = "" ## 
        self.PU = "" ## Publisher
        self.PI = "" ## Publisher City
        self.PA = "" ## Publisher Address
        self.SN = "" ## ISSN
        self.BN = "" ## ISBN
        self.J9 = "" ## 29-Character Source Abbreviation
        self.JI = "" ## ISO Source Abbreviation
        self.PD = "" ## Publication Date
        self.PY = 0 ## Year Published
        self.VL = "" ## Volume
        self.IS = "" ## Issue
        self.PN = "" ## Part Number
        self.SU = "" ## Supplement
        self.SI = "" ## Special Issue
        self.BP = "" ## Beginning Page
        self.EP = "" ## Ending Page
        self.AR = "" ## Article Number
        self.DI = "" ## Digital Object Identifier (DOI)
        self.D2 = "" ## 
        self.PG = "" ## Page Count
        self.P2 = "" ## 
        self.WC = "" ## Web of Science Category
        self.SC = "" ## Subject Category
        self.GA = "" ## Document Delivery Number
        self.UT = "" ## Unique Article Identifier

    def parse_line(self, line, defCols, numCols):
        """
        parse a line of the WoS txt output file  
        """
        s = line.split("\t")

        if len(s)==numCols:
            if(s[defCols['PT']]=='J'): self.PT = 'Journal' ## Publication Type (J=Journal; B=Book; S=Series)
            if(s[defCols['PT']]=='B'): self.PT = 'Book' 
            if(s[defCols['PT']]=='S'): self.PT = 'Series' 
            self.AU = s[defCols['AU']] ## Authors
            self.TI = s[defCols['TI']] ## Document Title
            self.SO = s[defCols['SO']] ## Publication Name
            self.DT = s[defCols['DT']] ## Document Type
            self.DE = s[defCols['DE']] ## Author Keywords
            self.ID = s[defCols['ID']] ## Keywords Plus
            self.C1 = s[defCols['C1']] ## Author Address
            self.CR = s[defCols['CR']] ## Cited References
            self.TC = s[defCols['TC']] ## Times Cited
            self.J9 = s[defCols['J9']] ## 29-Character Source Abbreviation
            self.PD = s[defCols['PD']] ## Publication Date
            if s[defCols['PY']].isdigit(): self.PY = int(s[defCols['PY']])
            else:               self.PY = 0  ## Year Published
            self.VL = s[defCols['VL']] ## Volume
            self.IS = s[defCols['IS']] ## Issue
            self.BP = s[defCols['BP']] ## Beginning Page
            self.WC = s[defCols['WC']] ## Web of Science Category
            self.UT = s[defCols['UT']] ## Unique Article Identifier
        else:
            print(("ARG %s != %s"%(len(s),numCols)))
## ##################################################

def defColumns(line):

  # initialize
  Cols = ['PT', 'AU', 'TI', 'SO', 'DT', 'DE', 'ID', 'C1', 'CR', 'TC', 'J9', 'PD', 'PY', 'VL', 'IS', 'BP', 'WC', 'UT'];
  defCols = dict();
  
  # match columns number in "line"
  foo = line.replace('\xef\xbb\xbf','').split('\t')
  for i in range(len(foo)):
    if foo[i] in Cols: 
      defCols[foo[i]] = i
  numCols = len(foo)

  return (defCols, numCols)


