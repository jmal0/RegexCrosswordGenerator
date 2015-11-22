#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import random
import re


class RegexGenerator(object):
    """
    Class for generating random regular expressions.

    1:
    - bracket_pattern
    - not_bracket_pattern

    N:
    - whole_word_pattern

    Patterns:
    "{}{}|{}{}|{}+"
    "[{}{}{}{}{}{}]+"
    "[^{}{}{}{}{}]+"
    "{}{}|{}{}|{}{}"
    """
    ALLOWED_CHARACTERS = ("abcdefghijklmnopqrstuvwxyz" +
                          "ABCDEFGHIJKLMNOPQRSTUVWXYZ" +
                          "1234567890")

    def __init__(self, width=2, height=2):
        self._rows = [self._regex_from_pattern(width) for i in xrange(height)]
        self._cols = [self._regex_from_pattern(height) for i in xrange(width)]

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

    def whole_word_pattern(self, length):
        """
        Returns pattern matching {} len times.
        """
        return "{}" * length

    def bracket_pattern(self, min_num=3, max_num=5):
        """
        Returns pattern matching [{}{}{}...]
        """
        return "[" + "{}" * random.randrange(min_num, max_num + 1) + "]"

    def not_bracket_pattern(self, min_num=3, max_num=5):
        """
        Returns pattern matching [^{}{}{}...]
        """
        return "[^" + "{}" * random.randrange(min_num, max_num + 1) + "]"

    def unique_chars(self, num):
        """
        Get list of unique chars from the ALLOWED_CHARACTERS
        """
        chars = ""
        while len(chars) < num:
            rand_char = random.choice(self.ALLOWED_CHARACTERS)
            if rand_char not in chars:
                chars += rand_char
        return sorted(chars)

    def _regex_from_pattern(self, length):
        i = random.randrange(4)
        if i == 0:
            pattern = (self.whole_word_pattern(length) + "|" +
                       self.whole_word_pattern(length) + "|" +
                       self.whole_word_pattern(length))
        elif i == 1:
            pattern = self.bracket_pattern() + "+"
        elif i == 2:
            pattern = self.not_bracket_pattern() + "+"
        elif i == 3:
            pattern = (self.whole_word_pattern(length) + "|" +
                       self.whole_word_pattern(length) + "|" +
                       self.whole_word_pattern(1) + "+")
        else:
            raise Exception("For some reason, random.randrange() did not"
                            "return a number within the given range")

        chars = self.unique_chars(pattern.count("{}"))
        while pattern.count("{}") > 0:
            pattern = pattern.replace("{}", chars[0], 1)
            chars = chars[1:]
        return re.compile(pattern)


if __name__ == "__main__":
    x = RegexGenerator()
    print(map(lambda x: x.pattern, x.rows))
    print(map(lambda x: x.pattern, x.cols))
