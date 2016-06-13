#Classes used to represent movies and ratings

"""
	class: Movie
	A class used to represent a Movie and all relevant characteristics about it
	
	params: 
		title: Title of the movie
		year: Year the movie was released 
		rating: Rating object that represents the movie
		actors: list of actors who acted in the movie
		director: director of the movie (str type, if multiple separated by a comma, director is transformed into a list)
		rated: MPAA Rating of the movie
		poster: URL which links to an image of the movie poster
		imdb_id: alphanumeric digit which links to the imdb.com website of the movie
		plot: string containing a short plot of the movie
		genre: comma separated list of genres of the movie
	
	Returns:
		 Movie object
			
"""
class Movie:
	def __init__(self,title,year,rating=None,actors=None,director=None,rated=None,poster=None,imdb_id=None,plot=None,genre=None):
		self.title = title.strip() if title else None
		self.year = str(year).strip() if year else None
		self.rating = rating
		self.actors = actors
		self.rated = rated
		self.poster = poster
		self.imdb_id = imdb_id
		self.plot = plot
		self.genre = genre
		
		self.director = director.split(',') if director else None
		#self.avg_rating is the average of all the ratings, computed by self.calc_avg_rating()
		self.avg_rating = None
		
		
	"""	
		prints a string containing information about the Movie object
		params:
			None
		returns:
			None
	"""	
	def print_movie(self):
		print "%s %s\tIMDB: %s\tRT: %s\tMETA:%s" %(self.title,self.year,self.rating.imdb_rating,self.rating.rotten_rating,self.rating.metascore_rating)
		
		
	"""
		returns IMDB rating of the movie
		returns:
			imdb_rating as float type
	"""
	def get_imdb_rating(self):
		try:
			f = float(self.rating.imdb_rating)
		except:
			return None
		return f
		
		
	"""
		returns Rotten Tomatoes rating of the movie	
		returns:
			rotten_rating as float
	"""
	def get_rotten_rating(self):
		try:
			f = float(self.rating.rotten_rating)
		except:
			return None
		return f
		
		
	"""
		returns Metacritic rating of the movie
		returns:
			metascore_rating as float type (Note: returns raw metascore rating out of 100 instead of 10)
	"""
	def get_meta_rating(self):
		try:
			f = float(self.rating.metascore_rating)
		except:
			return None
		return f
		
		
	"""
		returns Metascore rating of the movie (out of 10) and properly formatted
		returns:
			metascore_rating as float type out of 10
	"""
	def get_meta_rating_f(self):
		f = self.get_meta_rating()
		if f:
			f = str(f/10.0)
			f = f.split('.')
			f = f[0] + '.' +f[1][0]
			return f
		return None
		
		
	"""
		returns IMDB rating of the movie, properly formatted
		returns:
			imdb_rating as float type
	"""
	def get_imdb_rating_f(self):
		f = self.get_imdb_rating()
		if f:
			f = str(f)
			f= f.split('.')
			f = f[0] + '.'+f[1][0]
			return f
		return None
		
		
	"""
		returns Rotten Tomatoes rating of the movie properly formatted
		returns:
			rotten_rating as float type
	"""
	def get_rotten_rating_f(self):
		f = self.get_rotten_rating()
		if f:
			f = str(f)
			f = f.split('.')
			f = f[0] + '.' + f[1][0]
			return f
		return None
		
		
	"""
		returns URL of IMDB website for the movie	
		returns:
			url
	"""
	def get_imdb_url(self):
		if self.imdb_id:
			url = "http://www.imdb.com/title/"+self.imdb_id
			return url
		return None
		
		
	"""
		returns:
			imdb_id
	"""
	def get_imdb_id(self):
		return self.imdb_id
		
		
	"""
		returns:
			plot
	"""
	def get_plot(self):
		return self.plot
		
		
	"""
		returns:
			genre
	"""
	def get_genre(self):
		return self.genre
		
		
	"""
		gets all of the ratings inside of the movie object
		returns:
			tuple of (imdb_rating,rotten_rating,meta_rating)
	"""
	def get_all_ratings(self):
		return (self.get_imdb_rating,self.get_rotten_rating,self.get_meta_rating)
		
		
	"""
		returns the poster link of the movie
		returns:
			poster
	"""
	def get_poster_link(self):
		return self.poster
		
		
	"""
		returns MPAA rating of the movie
		returns:
			rated
	"""
	def get_mpaa_rating(self):
		return self.rated
		
		
	"""
		returns a list of actors
		returns:
			actors
	"""
	def get_actors(self):
		return self.actors
		
		
	"""
		returns a list of directors
		returns:
			director
	"""
	def get_directors(self):
		return self.director
		
		
	"""
		calculates the average rating of all 3 ratings for the movie
		returns:
			avg
	"""
	def calc_avg_rating(self):
		r_imdb = self.get_imdb_rating_f()
		r_rt = self.get_rotten_rating_f()
		r_meta = self.get_meta_rating_f()
		
		l = [r_imdb,r_rt,r_meta]
		for i in range(l.count(None)):
			l.remove(None)
		if len(l) == 0:
			return None
		l = [float(i) for i in l]
		avg = float(sum(l))/float(len(l))
		self.avg_rating = avg
		return avg
		
	
"""
	class: Rating
		A class which holds 3 ratings (imdb rating, rotten tomatoes rating, and metacritic rating)
		
		params:
			imdb_rating: IMDB rating of the movie out of 10
			rotten_rating: Rotten Tomatoes rating of the movie out of 10
			meta: Metascore rating of the movie (API does this out of 100)
		returns:
			Rating object which contains all the ratings for the movie
		
"""		
class Rating:
	def __init__(self,imdb_rating=None,rotten_rating=None,meta=None):
		self.imdb_rating = imdb_rating
		self.rotten_rating = rotten_rating
		self.metascore_rating = meta
		
