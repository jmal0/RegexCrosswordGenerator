#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

from CrosswordSquare import CrosswordSquare

class RegexCrossword:
    ''' Object representing the puzzle
    The puzzle has x and y dimensions and a corresponding number of regex rules
    '''
    def __init__(self, xSize, ySize, columnRules, rowRules):
        self.xSize = xSize
        self.ySize = ySize
        self.grid = [[" " for c in xrange(xSize)] for r in xrange(ySize)]
        
        if(xSize != len(columnRules)):
            raise ValueError("Length of columnRules must equal xSize")
        if(ySize != len(rowRules)):
            raise ValueError("Length of rowRules must equal ySize")

        self.cRules = columnRules
        self.rRules = rowRules
   
    def check(self):
        ''''Determine if filled grid satisfies all row and column rules'''
        # Check row patterns
        for r in xrange(self.ySize):
            row = ''.join(self.grid[r])
            if(not self.rRules[r].match(row)):
                return False

        # Check column patterns
        for c in xrange(self.xSize):
            col = ''.join([self.grid[r][c] for r in xrange(self.ySize)])
            if(not self.cRules[c].match(col)):
                return False

        return True

    def __str__(self):
        puzzle = ""
        puzzle += "%-10s" % ""
        for r in xrange(self.xSize):
            puzzle += "%-10s" % self.cRules[r].pattern
        puzzle += "\n"

        for r in xrange(self.xSize):
            puzzle += "%-10s" % self.rRules[r].pattern
            for c in xrange(self.ySize):
                puzzle += "%-10s" % self.grid[r][c]
            puzzle += "\n"
        return puzzle