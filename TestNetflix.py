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
import os
import pickle
from urllib.request import urlopen

from Netflix import netflix_solve, netflix_predict, netflix_rsme, ANSWERS_LIST, RATINGS_LIST


FILEPATHS = [
    "/u/downing/cs/netflix-caches/bis266-probeAns.p",
    "/u/downing/cs/netflix-caches/amm6364-averageCustomerRating.p",
    "/u/downing/cs/netflix-caches/amm6364-averageMovieRating.p"
    ]

URLPATHS = [
    "http://www.cs.utexas.edu/users/downing/netflix-caches/bis266-probeAns.p",
    "http://www.cs.utexas.edu/users/downing/netflix-caches/"+
    "amm6364-averageCustomerRating.p",
    "http://www.cs.utexas.edu/users/downing/netflix-caches/amm6364"+
    "-averageMovieRating.p"
    ]


if os.path.isfile(FILEPATHS[0]):
    ANSWERS_CACHE = pickle.load(open(FILEPATHS[0], "rb"))
    CUSTOMER_RATINGS = pickle.load(open(FILEPATHS[1], "rb"))
    MOVIE_RATINGS = pickle.load(open(FILEPATHS[2], "rb"))
else:
    CACHE_READ = urlopen(URLPATHS[0]).read()
    ANSWERS_CACHE = pickle.loads(CACHE_READ)
    CACHE_READ = urlopen(URLPATHS[1]).read()
    CUSTOMER_RATINGS = pickle.loads(CACHE_READ)
    CACHE_READ = urlopen(URLPATHS[2]).read()
    MOVIE_RATINGS = pickle.loads(CACHE_READ)
# -----------
# TestNetflix
# -----------
class TestNetflix (TestCase):
    # ----
    # netflix_predict
    # ----
    

    # def test_netflix_predict_1(self):
    #     global ANSWERS_LIST
    #     global RATINGS_LIST
    #     ANSWERS_LIST[:] = []
    #     RATINGS_LIST[:] = []

    #     rsme = round(netflix_rsme(), 2)
    #     self.assertEqual(rsme, 1.79)   

    # def test_netflix_predict_2(self):
    #     global ANSWERS_LIST
    #     global RATINGS_LIST
    #     ANSWERS_LIST[:] = []
    #     RATINGS_LIST[:] = []

    #     rsme = round(netflix_rsme(), 2)
    #     self.assertEqual(rsme, 1.79)    

    # def test_netflix_predict_3(self):
    #     global ANSWERS_LIST
    #     global RATINGS_LIST
    #     ANSWERS_LIST[:] = []
    #     RATINGS_LIST[:] = []

    #     rsme = round(netflix_rsme(), 2)
    #     self.assertEqual(rsme, 1.79)     


    # ----
    # netflix_solve
    # ----
    

    def test_netflix_solve_1(self):
        global ANSWERS_LIST
        global RATINGS_LIST
        ANSWERS_LIST[:] = []
        RATINGS_LIST[:] = []
        file_in = StringIO("1:\n30878\n2647871\n1283744\n2488120\n")

        write = StringIO()
        netflix_solve(file_in, write)
        out = write.getvalue()
        self.assertEqual(out, "1:\n3.7\n3.5\n3.6\n4.2\nRMSE: 0.58\n")

    # def test_netflix_solve_2(self):
    #     global ANSWERS_LIST
    #     global RATINGS_LIST
    #     ANSWERS_LIST[:] = []
    #     RATINGS_LIST[:] = []

    #     rsme = round(netflix_rsme(), 2)
    #     self.assertEqual(rsme, 1.79)

    # def test_netflix_solve_3(self):
    #     global ANSWERS_LIST
    #     global RATINGS_LIST
    #     ANSWERS_LIST[:] = []
    #     RATINGS_LIST[:] = []


    #     rsme = round(netflix_rsme(), 2)
    #     self.assertEqual(rsme, 1.79)

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
