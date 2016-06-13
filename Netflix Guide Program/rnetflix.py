"""
rnetflix.py -- the web scraper for the application. Uses Selenium (http://www.seleniumhq.org/) to automate a browser for web scraping.

"""
#imports
import urllib
import urllib2 as url
import time
import sys
from base64 import b64encode, b64decode
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from imdb import Rating, get_imdb
from requests import *
from netbase import MovieDatabase
from DataStructure import *


"""
	Presents a loading screen for t_sec on the command line. Used to wait for the browser to render the page.
	
	params:
		t_sec: amount of time in seconds to wait
"""
def load_time(t_sec):
	l = len(str(t_sec))
	print "Loading in %d seconds...%d" %(t_sec,t_sec),
	for i in range(t_sec,-1,-1):
		print "\b"*(l + 1) + " "*(l + 1) + "\b"*(l + 2),
		print "%d" %i,
		l = len(str(i))
		time.sleep(1)
	print "\n"

"""
	Usage: rnetflix.py <netflix e-mail><password>. Logins into user's account with e-mail and password, scrapes the instant queue, makes the API calls from 
			imdb.py and adds new movies to the database
"""	
def main():
	if len(sys.argv) < 3:
		print "Usage: <netflix e-mail> <netflix password> ==> Print Queue and Ratings"
		exit(0)
	email = sys.argv[1]
	password = sys.argv[2]
	
	#initilaize movie database for storing movies and webdriver for opening the page and scraping
	
	mdb = MovieDatabase()
	
	movies = []
	#initilaize webdriver
	driver = webdriver.Firefox()
	
	driver.get("https://www.netflix.com/Login")
	
	#Login procedure
	e_email = driver.find_element_by_name("email")
	e_button_submit = driver.find_element_by_class_name("login-button")
	
	e_email.send_keys(email)
	e_remember = driver.find_element_by_name("rememberMe")
	e_remember.click()
	e_button_submit.click()
	
	e_password = driver.find_element_by_name("password")
	e_password.send_keys(password)
	
	e_button_submit = driver.find_element_by_class_name("login-button")
	print "[+] Signing in..."
	e_button_submit.click()


	load_time(4)
	
	#click the right profile
	profile = driver.find_elements_by_class_name("profile-icon")
	
	
	profile = profile[2]
	profile.click()
	load_time(2)
	driver.get("http://www.netflix.com/browse/my-list")
	print "[+] Waiting for movie data...\n\n"
	load_time(15)
	
	#Find movies by tag in my-list
	temp = driver.find_elements_by_class_name("video-artwork")
	print "Titles found: " + str(len(temp))
	
	for i in temp:
		print temp
		
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
			
	driver.close()
	
	#Iterate through list of movie titles in netflix list, get informatino about them from the API,
	#and add them to the database
	
	for i in range(len(titles)):
		title = titles[i]
		t = title.encode('utf-8','replace')
		y = years[i].encode('utf-8','replace')
		rating = get_imdb(t,year=y)
		m = Movie(t,y,rating)
		mdb.db_update_movie(m)
		mdb.commit()
		movies.append(m)
		m.print_movie()
		
	print "[+] %d movies found in instant queue" %(len(movies))
	#for m in movies:
	#	m.print_movie()
	#print "dumping titles list"
	#print titles
	del mdb
		
if __name__ == "__main__":
	main()