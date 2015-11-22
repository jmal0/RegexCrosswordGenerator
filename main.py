#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import re
from RegexCrossword import RegexCrossword

if __name__ == '__main__':
    xSize = 3
    ySize = 2
    columnRules = [re.compile("UB|IE|AW"), re.compile("[TUBE]*"), re.compile("[BORF].")]
    rowRules = [re.compile("[NOTAD]*"), re.compile("WEL|BAL|EAR")]
    puzzle = RegexCrossword(xSize, ySize, columnRules, rowRules)
    print(puzzle)
    puzzle.solve_bruteforce()
    print(puzzle)