#!/usr/bin/env python3

import pickle

#The cache with the answers to check for {int:{int:int}}
ANSWERS_CACHE = pickle.load(open("/u/downing/cs/netflix-caches/amm6364-answer.p", "rb"))
#The cache with the average customer ratings {int:float}
CUSTOMER_RATINGS = pickle.load(open("/u/downing/cs/netflix-caches/amm6364-averageCustomerRating.p", "rb"))
#The cache with the average movie ratings {int:float}
MOVIE_RATINGS = pickle.load(open("/u/downing/cs/netflix-caches/amm6364-averageMovieRating.p", "rb"))




def netflix_predict(movie_id, cust_id):
	customer_avg = CUSTOMER_RATINGS.get(cust_id)
	movie_avg = MOVIE_RATINGS.get(movie_id)
	total_avg = (customer_avg + movie_avg) / 2
	print(round(total_avg, 1))

def netflix_solve(reader, writer):
	"""
	reader, reader to get input from
	writer, writer to write to output
	"""
	movie_id = 0
	for line in reader:
		if ":" in line:
			movie_id = int(''.join(c for c in line if c.isdigit()))
			print("".join(line.split()))
		else:
			netflix_predict(movie_id, int(line))
