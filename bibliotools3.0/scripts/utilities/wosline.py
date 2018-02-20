#! /usr/bin/env python

#TODO see what this does in the grand scheme of things. it's different from the
# other objects in the utilities

import os
import sys
import glob
import numpy
import argparse

class Wosline:

    """
    parse a line(converted to list) of the WoS txt output file  
    """
    def parse_list(self, list_from_line, defCols, numCols):
        if len(list_from_line) == numCols :
            ## Publication Type (J=Journal; B=Book; S=Series)
            if(list_from_line[defCols['PT']]=='J'): 
                self.PT = 'Journal'             
            if(list_from_line[defCols['PT']]=='B'): 
                self.PT = 'Book' 
            if(list_from_line[defCols['PT']]=='S'): 
                self.PT = 'Series' 

            self.AU = list_from_line[defCols['AU']] ## Authors
            self.TI = list_from_line[defCols['TI']] ## Document Title
            self.SO = list_from_line[defCols['SO']] ## Publication Name
            self.DT = list_from_line[defCols['DT']] ## Document Type
            self.DE = list_from_line[defCols['DE']] ## Author Keywords
            self.ID = list_from_line[defCols['ID']] ## Keywords Plus
            self.C1 = list_from_line[defCols['C1']] ## Author Address
            self.CR = list_from_line[defCols['CR']] ## Cited References
            self.TC = list_from_line[defCols['TC']] ## Times Cited
            self.J9 = list_from_line[defCols['J9']] ## 29-Character Source Abbreviation
            self.PD = list_from_line[defCols['PD']] ## Publication Date
            if list_from_line[defCols['PY']].isdigit(): 
                self.PY = int(s[defCols['PY']])
            else:
                self.PY = 0  ## Year Published
            self.VL = list_from_line[defCols['VL']] ## Volume
            self.IS = list_from_line[defCols['IS']] ## Issue
            self.BP = list_from_line[defCols['BP']] ## Beginning Page
            self.WC = list_from_line[defCols['WC']] ## Web of Science Category
            self.UT = list_from_line[defCols['UT']] ## Unique Article Identifier
        else:
            print(("ARG %s != %s"%(len(list_from_line), numCols)))
 
    def __init__(self, list_from_line, def_cols, num_cols):
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
        self.PY = 0  ## Year Published
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

        self.parse_list(list_from_line, def_cols, num_cols)

   
####################################################

def defColumns(parsed_line_list):

  # initialize
  cols = ['PT', 'AU', 'TI', 'SO', 'DT', 'DE', 'ID', 'C1', 'CR', 
          'TC', 'J9', 'PD', 'PY', 'VL', 'IS', 'BP', 'WC', 'UT']
  def_cols = dict()
  
  # match columns number in "line"

  for i in range(len(parsed_line_list)):
    if parsed_line_list[i] in cols: 
      def_cols[parsed_line_list[i]] = i

  num_cols = len(parsed_line_list)

  return (def_cols, num_cols)


