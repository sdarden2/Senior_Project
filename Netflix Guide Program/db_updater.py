"""
	db_updater.py
	Used to update every movie currently in the database. Used if information has changed about
	the movie or if information is incomplete about the movie.
"""
from DataStructure import *
from netbase import *
from imdb import *

"""
	Updates all movies in database
	params:
		None
	returns:
		None
"""
def main():
		#Updates every movie in the database
		mdb = MovieDatabase()
		
		sql = "SELECT `Title`,`Year` FROM `movies`"
		res = mdb.command(sql)
		
		for pair in res:
			title = pair[0].strip()
			year = pair[1].strip()
			
			movie = get_imdb(title,year=year)
			mdb.db_add_movie(movie)
		mdb.commit()
		
if __name__ == "__main__":
	main()