#!/usr/bin/envalue python3

# -------------------------------
# projects/Netflix/TestNetflix.py
# Copyright (C) 2016
# Glenn P. Downing
# -------------------------------

# https://docs.python.org/3.4/reference/simple_stmts.html#grammar-token-assert_stmt

# -------
# imports
# -------

from io import StringIO
from unittest import main, TestCase
import sys

from Netflix import netflix_rsme, ANSWERS_LIST, RATINGS_LIST

# -----------
# TestNetflix
# -----------
class TestNetflix (TestCase):


    # ----
    # netflix_rsme
    # ----
    

    def test_netflix_rsme_1(self):
        global ANSWERS_LIST
        global RATINGS_LIST

        ANSWERS_LIST[:] = []
        RATINGS_LIST[:] = []

        ANSWERS_LIST.extend([1, 3, 2, 4, 5])
        RATINGS_LIST.extend([2, 2, 3, 1, 3])

        rsme = round(netflix_rsme(), 2)
        self.assertEqual(rsme, 1.79)

    def test_netflix_rsme_2(self):
        global ANSWERS_LIST
        global RATINGS_LIST

        ANSWERS_LIST[:] = []
        RATINGS_LIST[:] = []

        ANSWERS_LIST.extend([1000, 2000, 1500, 1000, 1200])
        RATINGS_LIST.extend([1500, 1500, 3000, 1000, 1800])

        rsme = round(netflix_rsme(), 2)
        self.assertEqual(rsme, 788.67)

    def test_netflix_rsme_3(self):
        global ANSWERS_LIST
        global RATINGS_LIST

        ANSWERS_LIST[:] = []
        RATINGS_LIST[:] = []

        ANSWERS_LIST.extend([15, 11, 13, 18, 12])
        RATINGS_LIST.extend([11, 18, 14, 15, 11])

        rsme = round(netflix_rsme(), 2)
        self.assertEqual(rsme, 3.90)

# ----
# main
# ----

if __name__ == "__main__":
    main()

""" #pragma: no cover
% coverage3 run --branch TestNetFlix.py >  TestNetflix.out 2>&1



% coverage3 report -m                   >> TestNetflix.out

"""
