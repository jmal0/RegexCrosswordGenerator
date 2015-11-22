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
    ALLOWED_CHARACTERS = ("ABCDEFGHIJKLMNOPQRSTUVWXYZ" +
                          "1234567890")

    def __init__(self, width=2, height=2, rows=None, cols=None, char_limit=10):
        self._used_chars = "".join(
            random.sample(self.ALLOWED_CHARACTERS, char_limit))
        if not (rows and cols):
            self._width = width
            self._height = height
            self._set_rows_and_cols(width, height, char_limit)
        else:
            self._rows = rows
            self._cols = cols
            chars_to_check = self._used_chars
            self._solution = self.posible_solution(chars_to_check)
            if not self._solution:
                raise Exception(
                    "No possible solution exists for this crossword")
            self._width = len(self._cols)
            self._height = len(self._rows)

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

    @property
    def solution(self):
        return self._solution

    def _set_rows_and_cols(self, width, height, char_limit):
        solution = None
        while not solution:
            self._used_chars = "".join(
                random.sample(self.ALLOWED_CHARACTERS, char_limit))
            self._rows = []
            self._cols = []
            chars_to_check = ""
            for i in xrange(height):
                row_to_add, chars_to_add = self._regex_from_pattern(width)
                self._rows.append(row_to_add)
                chars_to_check += chars_to_add
            for i in xrange(width):
                col_to_add, chars_to_add = self._regex_from_pattern(height)
                self._cols.append(col_to_add)
                chars_to_check += chars_to_add
            chars_to_check = "".join(set(chars_to_check))
            solution = self.posible_solution(chars_to_check)
        self._solution = solution

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
            rand_char = random.choice(self._used_chars)
            if rand_char not in chars:
                chars += rand_char
        return sorted(chars)

    def _substitute_chars(self, pattern):
        chars = self.unique_chars(pattern.count("{}"))
        while pattern.count("{}") > 0:
            pattern = pattern.replace("{}", chars[0], 1)
            chars = chars[1:]
        return pattern

    def _regex_from_pattern(self, length):
        i = random.randrange(4)
        if i == 0:
            pattern = (self.whole_word_pattern(length) + "|" +
                       self.whole_word_pattern(length) + "|" +
                       self.whole_word_pattern(length))
            pattern = self._substitute_chars(pattern)
            chars_to_check = filter(lambda x: x in self._used_chars,
                                    pattern)
        elif i == 1:
            pattern = self.bracket_pattern() + "+"
            pattern = self._substitute_chars(pattern)
            chars_to_check = filter(lambda x: x in self._used_chars,
                                    pattern)
        elif i == 2:
            pattern = self.not_bracket_pattern() + "+"
            pattern = self._substitute_chars(pattern)
            chars_to_check = filter(lambda x: x not in pattern,
                                    self._used_chars)
        elif i == 3:
            pattern = (self.whole_word_pattern(length) + "|" +
                       self.whole_word_pattern(length) + "|" +
                       self.whole_word_pattern(1) + "+")
            pattern = self._substitute_chars(pattern)
            chars_to_check = filter(lambda x: x in self._used_chars,
                                    pattern)
        else:
            raise Exception("For some reason, random.randrange() did not"
                            "return a number within the given range")

        return re.compile(pattern), chars_to_check

    def _solution_from_grid(self, grid, chars_to_check):
        return map(
            lambda row: "".join(map(lambda i: chars_to_check[i], row)), grid)

    def posible_solution(self, chars_to_check):
        """
        Get a possible solution for the regex crossword generated.
        The solution will just be a list of strings.
        """
        char_count = len(chars_to_check)
        grid = [[0] * self._width for i in xrange(self._height)]
        solution = self._solution_from_grid(grid, chars_to_check)
        x, y = 0, 0
        while not self.apply_solution(solution):
            grid[y][x] += 1
            while grid[y][x] >= char_count:
                grid[y][x] = 0
                x += 1
                if x >= self._width:
                    x = 0
                    y += 1
                    if y >= self._height:
                        return None
                grid[y][x] += 1
            x = 0
            y = 0
            solution = self._solution_from_grid(grid, chars_to_check)

        return solution

    def apply_solution(self, solution):
        """
        Test a possible solution.
        """
        for i in xrange(len(self._rows)):
            m = self._rows[i].match(solution[i])
            if not m or len(m.group(0)) != self._width:
                return False

        for i in xrange(len(self._cols)):
            m = self._cols[i].match(
                reduce(lambda x, y: x + y[i], solution, ""))
            if not m or len(m.group(0)) != self._height:
                return False

        return True


if __name__ == "__main__":
    # x = RegexGenerator(
    #     rows=[re.compile("HE|LL|O+"), re.compile("[PLEASE]+")],
    #     cols=[re.compile("[^SPEAK]+"), re.compile("EP|IP|EF")]
    # )
    x = RegexGenerator()
    print("Rows", map(lambda x: x.pattern, x.rows))
    print("Cols", map(lambda x: x.pattern, x.cols))
    print("Solution", x.solution or "No solution")
