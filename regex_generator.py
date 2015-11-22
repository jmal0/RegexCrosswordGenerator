#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import random
import re


class RegexGenerator(object):
    """
    Class for generating random regular expressions.
    """
    ALLOWED_CHARACTERS = ("abcdefghijklmnopqrstuvwxyz" +
                          "ABCDEFGHIJKLMNOPQRSTUVWXYZ" +
                          "1234567890")

    PATTERNS = [
        "{}{}|{}{}|{}+",
        "[{}{}{}{}{}{}]+",
        "[^{}{}{}{}{}]+",
        "{}{}|{}{}|{}{}"
    ]

    def __init__(self, width=2, height=2):
        self._rows = [self._regex_from_pattern() for i in xrange(width)]
        self._cols = [self._regex_from_pattern() for i in xrange(height)]

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

    def _regex_from_pattern(self):
        pattern = random.choice(self.PATTERNS)
        while pattern.count("{}") > 0:
            rand_char = random.choice(self.ALLOWED_CHARACTERS)
            pattern = pattern.replace("{}", rand_char, 1)
        return re.compile(pattern)

if __name__ == "__main__":
    RegexGenerator()
