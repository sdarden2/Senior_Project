#Get images for movies
"""
	Used to request and save all images locally for the movies currently in the database.
	Selects all movies from database and uses poster_link entry to request the poster image from the internet.
"""
from netbase import *
from DataStructure import *
from urllib import *
from urllib2 import *
import os

#Gets images from movies in database
#Saves images in current director/images/
PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),"images")

"""
	Creates a name for the image given the movie title and year.
	params:
		title: Title of the movie
		year: Year the movie was released
	returns:
		s: string which is the name to save image under
"""
def to_image_name(title,year):
	title = title.replace(" ","_").replace(":","_").replace("\"","\'")
	s = "%s_%s.jpg" %(title,year)
	return s
#main retrieves the movies from the database and then retrieves the images for those movies by the 
#poster_link property	
def main():
	d = os.path.dirname(os.path.abspath(__file__))
	dd = os.path.join(d,PATH)
	mdb = MovieDatabase()
	sql = "SELECT `Title`,`Year`,`Poster_Link` FROM `movies`"
	res = mdb.command(sql)
	for i in res:
		title = i[0]
		year = i[1]
		link = i[2]

		if link:
			if link == "N/A":
				pass
			else:
				loc = os.path.join(PATH,to_image_name(title,year))
				print loc
				print link
				if not os.path.isfile(loc):
					urlretrieve(link,loc)
			
		
if __name__ == "__main__":
	main()