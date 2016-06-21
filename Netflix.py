#!/usr/bin/env python3

import os
import pickle
from urllib.request import urlopen
from numpy import mean, sqrt, square, subtract

FILEPATHS = [
    "/u/downing/cs/netflix-caches/bis266-probeAns.p",
    "/u/downing/cs/netflix-caches/amm6364-averageCustomerRating.p",
    "/u/downing/cs/netflix-caches/amm6364-averageMovieRating.p",
    "/u/downing/cs/netflix-caches/bdd465-movieYear.p",
    "/u/downing/cs/netflix-caches/sy6955-avgUserFiveYears.p"
    ]

URLPATHS = [
    "http://www.cs.utexas.edu/users/downing/netflix-caches/bis266-probeAns.p",
    "http://www.cs.utexas.edu/users/downing/netflix-caches/"+
    "amm6364-averageCustomerRating.p",
    "http://www.cs.utexas.edu/users/downing/netflix-caches/amm6364"+
    "-averageMovieRating.p",
    "http://www.cs.utexas.edu/users/downing/netflix-caches/bdd465-movieYear.p",
    "http://www.cs.utexas.edu/users/downing/netflix-caches/"+
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

ANSWERS_LIST = []
RATINGS_LIST = []


def netflix_year_average(movie_id, cust_id):
    """
    movie_id, {int} id for individual movie to get year of
    cust_id, {int} id for individual customer to look up avg
    """
    movie_date = MOVIE_YEAR.get(movie_id)

    if movie_date == "NULL":
        return YEAR_AVERAGE.get(cust_id).get("NULL")
    else:
        movie_date = (int(movie_date) // 5) * 5
        return YEAR_AVERAGE.get(cust_id).get(movie_date)


def netflix_predict(movie_id, cust_id, writer):
    """
    movie_id, {int} id for individual movie
    cust_id, {int} id for individual customer
    writer the output of the program to write to
    """
    assert  1 <= cust_id <= 2649429
    assert 1 <= movie_id <= 17770

    customer_avg = CUSTOMER_RATINGS.get(cust_id)
    movie_avg = MOVIE_RATINGS.get(movie_id)
    year_avg = netflix_year_average(movie_id, cust_id)
    total_avg = round((customer_avg + movie_avg + year_avg) / 3, 1)

    assert 1 <= total_avg <= 5

    RATINGS_LIST.append(total_avg)
    ANSWERS_LIST.append(ANSWERS_CACHE.get(movie_id).get(cust_id))

    assert len(RATINGS_LIST) == len(ANSWERS_LIST)

    writer.write(str(total_avg) + "\n")



def netflix_solve(reader, writer):
    """
    reader, reader to get input from
    writer, writer to write to output
    """
    movie_id = 0
    for line in reader:
        if ":" in line:
            movie_id = int(''.join(c for c in line if c.isdigit()))
            writer.write("".join(line.split()) + "\n")
        else:
            netflix_predict(movie_id, int(line), writer)

    rsme = netflix_rsme()
    writer.write("RMSE: " + str(round(rsme, 2)) + "\n")

def netflix_rsme():
    return sqrt(mean(square(subtract(ANSWERS_LIST, RATINGS_LIST))))
