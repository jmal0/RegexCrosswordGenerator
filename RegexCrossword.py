#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import re
from CrosswordSquare import CrosswordSquare

class RegexCrossword:
    ''' Object representing the puzzle
    The puzzle has x and y dimensions and a corresponding number of regex rules
    '''
    def __init__(self, xSize, ySize, columnRules, rowRules):
        self.xSize = xSize
        self.ySize = ySize
        self.grid = [[" " for c in xrange(xSize)] for r in xrange(ySize)]
        
        if xSize != len(columnRules):
            raise ValueError("Length of columnRules must equal xSize")
        if ySize != len(rowRules):
            raise ValueError("Length of rowRules must equal ySize")

        self.cRules = columnRules
        self.rRules = rowRules

    def setGrid(self, newGrid):
        try:
            for r in xrange(self.ySize):
                for c in xrange(self.ySize):
                    if len(newGrid[r][c] != 1):
                        raise ValueError("Each square must have only 1 character in it")
                    self.grid[r][c] = newGrid[r][c]
        except IndexError:
            raise ValueError("Grid must have correct number of rows and columns")

    def check(self):
        '''Determine if filled grid satisfies all row and column rules'''
        # Check row patterns
        for r in xrange(self.ySize):
            row = ''.join(self.grid[r])
            m = self.rRules[r].match(row)
            if not(m and len(m.group(0)) == self.xSize):
                return False

        # Check column patterns
        for c in xrange(self.xSize):
            col = ''.join([self.grid[r][c] for r in xrange(self.ySize)])
            m = self.cRules[c].match(col)
            if not(m and len(m.group(0)) == self.ySize):
                return False

        return True
    
    def solve_bruteforce(self):
        # Gotta start somewhere
        for r in xrange(self.ySize):
            for c in xrange(self.xSize):
                self.grid[r][c] = '0'

        changeR = 0
        changeC = 0
        while not self.check():
            [changeR,changeC] = self.nextChangeSquare()
            if changeR == -1:
                print("FUCK")
                return False;
            
            self.grid[changeR][changeC] = chr(incrementCharacter(self.grid[changeR][changeC]))
            
            [nextR, nextC] = nextRC(changeR, changeC, self.ySize, self.xSize)
            while(nextR != -1):
                self.grid[nextR][nextC] = '0'
                [nextR, nextC] = nextRC(nextR, nextC, self.ySize, self.xSize)

            #print(self)
        return True

    def nextChangeSquare(self):
        changeR = self.ySize - 1
        changeC = self.xSize - 1
        while(changeR != -1 and self.grid[changeR][changeC][0] == 'Z'):
            [changeR, changeC] = prevRC(changeR, changeC, self.ySize, self.xSize)
        return [changeR, changeC]

    def solve(self):
        self.possibilities = [[CrosswordSquare(self.cRules[c], self.rRules[r]) for c in xrange(self.xSize)] for r in xrange(self.ySize)]

    def __str__(self):
        puzzle = ""
        puzzle += "%-10s" % ""
        for r in xrange(self.xSize):
            puzzle += "%-10s" % self.cRules[r].pattern
        puzzle += "\n"

        for r in xrange(self.ySize):
            puzzle += "%-10s" % self.rRules[r].pattern
            for c in xrange(self.xSize):
                puzzle += "%-10s" % self.grid[r][c]
            puzzle += "\n"
        return puzzle

def incrementCharacter(ch):
    """Increments ch to next possible character. Returns next character"""
    val = ord(ch) + 1
    if val == 58: # end of numbers
        return 65 # reset to A
    elif val == 91: # end of uppercase letters
        return 48 # reset to 0
    return val

def prevRC(r, c, nRows, nCols):
    c -= 1
    if c == -1:
        r -= 1
        c = nCols - 1
        if r == -1:
            return [-1, -1]
    return [r,c]

def nextRC(r, c, nRows, nCols):
    c += 1
    if c == nCols:
        r += 1
        c = 0
        if r == nRows:
            return [-1, -1]
    return [r,c]
