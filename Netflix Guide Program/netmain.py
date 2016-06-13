"""
	netmain.py
	Author: Sam Darden
	
"""
#Python login to netflix and update Database
#This is the main program which logs into user netflix account and updates the database with all movies in the user's list
#Steps:
	#1. Login using user's netflix e-mail and password
	#2. Search user's movie list on netflix
	#3. Scrape movies from user's movie list
	#4. Make API calls to get information and ratings for movies
	#5. Update the database for each movie

from DataStructure import *
from imdb import *
from rnetflix import *
from netbase import *

"""
	Usage: netmain.py <e-mail><password>. Adds user's netflix movie list to the movie database
"""
def main():
	if len(sys.argv) < 3:
			print "Usage: <netflix e-mail> <netflix password> ==> Print Queue and Ratings"
			exit(0)
			
	email = sys.argv[1]
	password = sys.argv[2]
	
	
	mdb = MovieDatabase() #movie_db to update/pull from
	
	movies = []
	#create webdriver for web scraping
	driver = webdriver.Firefox()
	driver.get("https://www.netflix.com/Login")
	
	#Locate html elements for loggin in 
	e_email = driver.find_element_by_name("email")
	e_password = driver.find_element_by_name("password")
	e_button_submit = driver.find_element_by_id("login-form-contBtn")
	print "[+] Entering credentials..."
	
	e_email.send_keys(email)
	e_password.send_keys(password)

	print "[+] Signing in..."
	e_button_submit.click()


	
	driver.get("http://www.netflix.com/browse/my-list")
	print "[+] Waiting for movie data...\n\n"
	#wait for full page load
	load_time(15)
	
	temp = driver.find_elements_by_tag_name("a")
	years = driver.find_elements_by_class_name("year")
	
	years = [i.text for i in years]
	
	if len(temp) > 0:
		print "[+] Movie tags found..."

	titles =[]
	print "[+] Waiting to clean and print..."
	
	for i in temp:
		if i.get_attribute("type") == "title":
			titles.append(i.text)
	
	#Close web driver. No longer needed.
	driver.close()
	
	#Create Movie objects from titles and years, then add them to the database
	for i in range(len(titles)):
		title = titles[i]
		t = title.encode('utf-8','replace')
		y = years[i].encode('utf-8','replace')
		
		m = Movie(t,y)
		
		movies.append(m)
		
	print "[+] %d movies found in instant queue" %(len(movies))

	f = open("Queue.list",'w')
	for i in movies:
		f.write("%s:%s\n" %(i.title if i.title else None ,i.year if i.year else None))
	f.close()
	
	#Remove all movies from the list that are already in the database
	in_db_movies = []
	
	for mov in movies:
		if mdb.in_db(mov):
			in_db_movies.append(mov)
			movies.remove(mov)
	
	#Call movie API to fill in movie informatino and add movies to database	
	for mov in movies:
		m = get_imdb(mov.title,year=mov.year)
		mdb.db_add_movie(m)

	mdb.commit()

	
	
if __name__ == "__main__":
	main()