#!/usr/bin/env python3

import pickle
from numpy import mean, sqrt, square, subtract

#The cache with the answers to check for {int:{int:int}}
ANSWERS_CACHE = pickle.load(open("/u/downing/cs/netflix-caches/amm6364-answer.p", "rb"))
#The cache with the average customer ratings {int:float}
CUSTOMER_RATINGS = pickle.load(open("/u/downing/cs/netflix-caches/amm6364-averageCustomerRating.p", "rb"))
#The cache with the average movie ratings {int:float}
MOVIE_RATINGS = pickle.load(open("/u/downing/cs/netflix-caches/amm6364-averageMovieRating.p", "rb"))

ANSWERS_LIST = []
RATINGS_LIST = []


def netflix_predict(movie_id, cust_id, writer):
	"""
	movie_id, {int} id for individual movie
	cust_id, {int} id for individual customer
	writer, writer to write to output
	"""
	global ANSWERS_LIST
	global RATINGS_LIST

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
