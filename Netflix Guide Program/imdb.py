"""
	Uses the OMDB API (http://omdbapi.com/) to request information about a movie given a title.
	Response is returned in JSON format, parsed, and loaded into Movie objects.
"""
#returns imdb API response
#plot can be "short" or "long"
#Datatype to return r can be "json" or "xml"
#include rotten tomatoes: "true" or "false"
import urllib
import urllib2
import json
from DataStructure import *

site = "http://www.omdbapi.com/?"



"""
	The main function of imdb.py, it handles the API calls and rolls the responsed into Movie objects

	params:
		movie_title: Title of the movie. Cannot be None
		year: year the movie was released
		plot: defaults to "short". Options are "short"|"long"
		type: defaults to "json". Options are "json"|"xml"
		include_rt: defaults to True. Specifies whether to include rotten tomatoes rating in the response. Options are True|False
		timeout: timeout in seconds until program give up on connection
		
	returns:
		Movie object on success. None on failure.
"""
def get_imdb(movie_title,year=None,plot="short",type="json",include_rt=True,timeout=6):
	params={'t':movie_title,
			'y':year,'r':type,
			'tomatoes':'true' if include_rt else 'false'}
			
	params = dict(i for i in params.items() if i[1])
	query = urllib.urlencode(params)
	
	#Set all initial values to 0
	imdb_rating = rotten_rating = tomato_rotten = tomato_fresh = rotten_rating = metascore_rating = actors = \
	rated =  poster_link = director = data_year = imdb_id = plot = genre = r = None
	
	try:	
		json_str = urllib2.urlopen(site + query,timeout=timeout)
	except:
		return Movie(None,None)
		
	data = json.loads(json_str.read())
	
	if data.has_key("imdbRating"):
		imdb_rating = data["imdbRating"]
	else:
		imdb_rating = None
		
	if include_rt:
		if data.has_key("tomatoRating"):
			rotten_rating = data["tomatoRating"]
		else:
			rotten_rating = None
		if data.has_key("tomatoFresh"):
			tomato_fresh = data["tomatoFresh"]
		else:
			tomato_fresh = None
		if data.has_key("tomatoRotten"):
			tomato_rotten = data["tomatoRotten"]
		else:
			tomato_rotten = None
			
			
	if data.has_key("Metascore"):
		metascore_rating = data["Metascore"]
		
	if data.has_key("Actors"):
		actors = data["Actors"].encode('latin-1','ignore').split(',')
		if actors == "N/A" or actors == "N\\A":
			actors = None
			
			
	if data.has_key("Rated"):
		rated = data["Rated"].encode('latin-1','ignore')
		
		
	if data.has_key("Poster"):
		poster_link = data["Poster"]
		
		
	if data.has_key("Director"):
		director = data["Director"].encode('latin-1','ignore')
		if director == "N/A" or director == "N\\A":
			director = None
		
		
	if data.has_key("Year"):
		data_year = data["Year"]

		
	if data.has_key("imdbID"):
		imdb_id = data["imdbID"]

		
	if data.has_key("Plot"):
		plot = data["Plot"]

		
	if data.has_key("Genre"):
		genre = data["Genre"]

		
	if include_rt:
		r =  Rating(imdb_rating,rotten_rating,tomato_fresh,tomato_rotten,metascore_rating)
	else:
		if metascore_rating:
			r =  Rating(imdb_rating,meta=metascore_rating)
		else:
			r =  Rating(imdb_rating)

			
	if data_year != None:
		#data_year = data_year.decode('utf-8')
		data_year = data_year.encode('latin-1','replace')
		if '?' in data_year:
			data_year = data_year.split('?')[0]
		if ',' in data_year:
			data_year = data_year.split(',')[0]
		yr = data_year
	else:
		yr = year

		
	return Movie(movie_title,yr,rating=r,actors=actors,director=director,poster=poster_link,rated=rated,imdb_id=imdb_id,plot=plot,genre=genre)
