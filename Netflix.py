#!/usr/bin/env python3
import sys
import os
import pickle
from urllib.request import urlopen
from numpy import mean, sqrt, square, subtract

filepaths = [
    "/u/downing/cs/netflix-caches/amm6364-answer.p",
    "/u/downing/cs/netflix-caches/amm6364-averageCustomerRating.p",
    "/u/downing/cs/netflix-caches/amm6364-averageMovieRating.p"
    ]

urlpaths = [
    "http://www.cs.utexas.edu/users/downing/netflix-caches/amm6364-answer.p",
    "http://www.cs.utexas.edu/users/downing/netflix-caches/amm6364-averageCustomerRating.p",
    "http://www.cs.utexas.edu/users/downing/netflix-caches/amm6364-averageMovieRating.p"
    ]


if os.path.isfile(filepaths[0]):
    ANSWERS_CACHE = pickle.load(open(filepaths[0], "rb"))
    CUSTOMER_RATINGS = pickle.load(open(filepaths[1], "rb"))
    MOVIE_RATINGS = pickle.load(open(filepaths[2], "rb"))
else:
    cache_read_from_url = urlopen(urlpaths[0]).read()
    ANSWERS_CACHE = pickle.loads(cache_read_from_url)
    cache_read_from_url = urlopen(urlpaths[1]).read()
    CUSTOMER_RATINGS = pickle.loads(cache_read_from_url)
    cache_read_from_url = urlopen(urlpaths[2]).read()
    MOVIE_RATINGS = pickle.loads(cache_read_from_url)

ANSWERS_LIST = []
RATINGS_LIST = []


def netflix_predict(movie_id, cust_id, writer):
    customer_avg = CUSTOMER_RATINGS.get(cust_id)
    movie_avg = MOVIE_RATINGS.get(movie_id)
    total_avg = round((customer_avg + movie_avg) / 2, 1)

    RATINGS_LIST.append(total_avg)
    ANSWERS_LIST.append(ANSWERS_CACHE.get(movie_id).get(cust_id))
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
