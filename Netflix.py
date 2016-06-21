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
    "http://www.cs.utexas.edu/users/downing/netflix-caches/" +
    "amm6364-averageCustomerRating.p",
    "http://www.cs.utexas.edu/users/downing/netflix-caches/amm6364" +
    "-averageMovieRating.p",
    "http://www.cs.utexas.edu/users/downing/netflix-caches/bdd465-movieYear.p",
    "http://www.cs.utexas.edu/users/downing/netflix-caches/" +
    "sy6955-avgUserFiveYears.p",
]

# Checks to see if it is locally or on Travis, loads the 5 caches from there
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

# ----
# netflix_year_average
# ----


def netflix_year_average(movie_id, cust_id):
    """
    movie_id, {int} id for individual movie to get year of
    cust_id, {int} id for individual customer to look up avg
    """
    # Gets the date of the movie to use as a key
    movie_date = MOVIE_YEAR.get(movie_id)
    # If its null return the average of all the NULLS
    if movie_date == "NULL":
        return YEAR_AVERAGE.get(cust_id).get("NULL")
    # else return the average for that 5 years
    else:
        movie_date = (int(movie_date) // 5) * 5
        return YEAR_AVERAGE.get(cust_id).get(movie_date)

# ----
# netflix_predict
# ----


def netflix_predict(movie_id, cust_id, writer):
    """
    movie_id, {int} id for individual movie
    cust_id, {int} id for individual customer
    writer the output of the program to write to
    """
    # make sure the customer ID and Movie ID are valid
    assert 1 <= cust_id <= 2649429
    assert 1 <= movie_id <= 17770
    # Get the averages for the customer, movie and year
    customer_avg = CUSTOMER_RATINGS.get(cust_id)
    movie_avg = MOVIE_RATINGS.get(movie_id)
    year_avg = netflix_year_average(movie_id, cust_id)
    # average all of those together
    total_avg = round((customer_avg + movie_avg + year_avg) / 3, 1)
    # make sure the average is valid
    assert 1 <= total_avg <= 5
    # Append both the answer and the computed averages to lists to be used
    # later
    RATINGS_LIST.append(total_avg)
    ANSWERS_LIST.append(ANSWERS_CACHE.get(movie_id).get(cust_id))
    # make sure they are both the same length
    assert len(RATINGS_LIST) == len(ANSWERS_LIST)
    # Write to the output
    writer.write(str(total_avg) + "\n")


# ----
# netflix_solve
# ----
def netflix_solve(reader, writer):
    """
    reader, reader to get input from
    writer, writer to write to output
    """
    movie_id = 0
    # Loops through all lines
    for line in reader:
        # Checks to see if the ID is a movie
        if ":" in line:
            # Update the movie ID
            movie_id = int(''.join(c for c in line if c.isdigit()))
            # Write the line to the output
            writer.write("".join(line.split()) + "\n")
        else:
            # Get the average for the customer and movie
            netflix_predict(movie_id, int(line), writer)
    # Calculate teh Root mean square
    rsme = netflix_rsme()
    # Write the Root mean square to the output
    writer.write("RMSE: " + str(round(rsme, 2)) + "\n")

# ----
# netflix_rmse
# ----


def netflix_rsme():
    '''
    Calculates the root mean square for the answers
    '''
    return sqrt(mean(square(subtract(ANSWERS_LIST, RATINGS_LIST))))
