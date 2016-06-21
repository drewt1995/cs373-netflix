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
import os
import pickle
from urllib.request import urlopen

from Netflix import netflix_year_average, netflix_solve, netflix_predict
from Netflix import ANSWERS_LIST, RATINGS_LIST, netflix_rsme

FILEPATHS = [
    "/u/downing/cs/netflix-caches/bis266-probeAns.p",
    "/u/downing/cs/netflix-caches/amm6364-averageCustomerRating.p",
    "/u/downing/cs/netflix-caches/amm6364-averageMovieRating.p",
    "/u/downing/cs/netflix-caches/bdd465-movieYear.p",
    "/u/downing/cs/netflix-caches/sy6955-avgUserFiveYears.p"
]

URLPATHS = [
    "http://www.cs.utexas.edu/users/downing/netflix-caches/bis266-probeAns.p",
    "http://www.cs.utexas.edu/users/downing/netflix-caches/" +
    "amm6364-averageCustomerRating.p",
    "http://www.cs.utexas.edu/users/downing/netflix-caches/amm6364" +
    "-averageMovieRating.p",
    "http://www.cs.utexas.edu/users/downing/netflix-caches/bdd465-movieYear.p",
    "http://www.cs.utexas.edu/users/downing/netflix-caches/" +
    "sy6955-avgUserFiveYears.p",
]


if os.path.isfile(FILEPATHS[0]):
    ANSWERS_CACHE = pickle.load(open(FILEPATHS[0], "rb"))
    CUSTOMER_RATINGS = pickle.load(open(FILEPATHS[1], "rb"))
    MOVIE_RATINGS = pickle.load(open(FILEPATHS[2], "rb"))
    MOVIE_YEAR = pickle.load(open(FILEPATHS[3], "rb"))
    YEAR_AVERAGE = pickle.load(open(FILEPATHS[4], "rb"))
else:
    CACHE_READ = urlopen(URLPATHS[0]).read()
    ANSWERS_CACHE = pickle.loads(CACHE_READ)
    CACHE_READ = urlopen(URLPATHS[1]).read()
    CUSTOMER_RATINGS = pickle.loads(CACHE_READ)
    CACHE_READ = urlopen(URLPATHS[2]).read()
    MOVIE_RATINGS = pickle.loads(CACHE_READ)
    CACHE_READ = urlopen(URLPATHS[3]).read()
    MOVIE_YEAR = pickle.loads(CACHE_READ)
    CACHE_READ = urlopen(URLPATHS[4]).read()
    YEAR_AVERAGE = pickle.loads(CACHE_READ)


# -----------
# TestNetflix
# -----------
class TestNetflix (TestCase):
    # ----
    # netflix_year_average
    # ----

    def test_netflix_year_average_1(self):
        ANSWERS_LIST[:] = []
        RATINGS_LIST[:] = []

        movie_id = 1
        cust_id = 30878

        out = netflix_year_average(movie_id, cust_id)
        self.assertEqual(out, 3.5590361445783132)

    def test_netflix_year_average_2(self):
        ANSWERS_LIST[:] = []
        RATINGS_LIST[:] = []

        movie_id = 1
        cust_id = 2647871

        out = netflix_year_average(movie_id, cust_id)
        self.assertEqual(out, 2.9221105527638191)

    def test_netflix_year_average_3(self):
        ANSWERS_LIST[:] = []
        RATINGS_LIST[:] = []

        movie_id = 1
        cust_id = 1283744

        out = netflix_year_average(movie_id, cust_id)
        self.assertEqual(out, 3.7692307692307692)

    # ----
    # netflix_predict
    # ----
    def test_netflix_predict_1(self):
        ANSWERS_LIST[:] = []
        RATINGS_LIST[:] = []

        movie_id = 1
        cust_id = 30878

        write = StringIO()
        netflix_predict(movie_id, cust_id, write)
        out = write.getvalue()
        self.assertEqual(out, "3.6\n")

    def test_netflix_predict_2(self):
        ANSWERS_LIST[:] = []
        RATINGS_LIST[:] = []

        movie_id = 1
        cust_id = 2647871

        write = StringIO()
        netflix_predict(movie_id, cust_id, write)
        out = write.getvalue()
        self.assertEqual(out, "3.3\n")

    def test_netflix_predict_3(self):
        ANSWERS_LIST[:] = []
        RATINGS_LIST[:] = []

        movie_id = 1
        cust_id = 1283744

        write = StringIO()
        netflix_predict(movie_id, cust_id, write)
        out = write.getvalue()
        self.assertEqual(out, "3.7\n")

    # ----
    # netflix_solve
    # ----
    def test_netflix_solve_1(self):
        ANSWERS_LIST[:] = []
        RATINGS_LIST[:] = []
        file_in = StringIO("1:\n30878\n2647871\n1283744\n2488120\n")

        write = StringIO()
        netflix_solve(file_in, write)
        out = write.getvalue()
        self.assertEqual(out, "1:\n3.6\n3.3\n3.7\n4.4\nRMSE: 0.61\n")

    def test_netflix_solve_2(self):
        ANSWERS_LIST[:] = []
        RATINGS_LIST[:] = []
        file_in = StringIO("1000:\n2326571\n977808\n1010534\n1861759\n")

        write = StringIO()
        netflix_solve(file_in, write)
        out = write.getvalue()
        self.assertEqual(out, "1000:\n3.5\n3.3\n2.8\n4.4\nRMSE: 0.58\n")

    def test_netflix_solve_3(self):
        ANSWERS_LIST[:] = []
        RATINGS_LIST[:] = []
        file_in = StringIO("10002:\n1450941\n1213181\n308502\n2581993" +
                           "\n10003:\n1515111\n10004:\n1737087\n1270334\n1262711\n")

        write = StringIO()
        netflix_solve(file_in, write)
        out = write.getvalue()
        self.assertEqual(out, "10002:\n4.3\n3.8\n4.5\n4.2\n10003:" +
                         "\n3.2\n10004:\n4.5\n4.0\n3.8\nRMSE: 0.65\n")

    # ----
    # netflix_rsme
    # ----

    def test_netflix_rsme_1(self):

        ANSWERS_LIST[:] = []
        RATINGS_LIST[:] = []

        ANSWERS_LIST.extend([1, 3, 2, 4, 5])
        RATINGS_LIST.extend([2, 2, 3, 1, 3])

        rsme = round(netflix_rsme(), 2)
        self.assertEqual(rsme, 1.79)

    def test_netflix_rsme_2(self):

        ANSWERS_LIST[:] = []
        RATINGS_LIST[:] = []

        ANSWERS_LIST.extend([1000, 2000, 1500, 1000, 1200])
        RATINGS_LIST.extend([1500, 1500, 3000, 1000, 1800])

        rsme = round(netflix_rsme(), 2)
        self.assertEqual(rsme, 788.67)

    def test_netflix_rsme_3(self):

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
