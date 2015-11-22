#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import re
from RegexCrossword import RegexCrossword

if __name__ == '__main__':
    xSize = 2
    ySize = 2
    columnRules = [re.compile("[^SPEAK]+"), re.compile("EP|IP|EF")]
    rowRules = [re.compile("HE|LL|O+"), re.compile("[PLEASE]+")]
    puzzle = RegexCrossword(xSize, ySize, columnRules, rowRules)
    puzzle.solve_bruteforce()
    print(puzzle)