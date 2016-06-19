#!/usr/bin/env python3





def netflix_predict(movie_id, cust_id):
	pass


def netflix_solve(reader, writer):
	"""
	reader, reader to get input from
	writer, writer to write to output
	"""
	movie_id = 0
	for line in reader:
		if ":" in line:
			movie_id = int(''.join(c for c in line if c.isdigit()))
		else:
			netflix_predict(movie_id, int(line))
