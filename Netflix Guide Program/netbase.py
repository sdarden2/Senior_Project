#Python database managment for netflix project
#netbase.py
#Author: Sam Darden
"""
	netbase.py handles all of the database operations used. Used to connect to the database `movie_db` and populate it.
	
"""
"""
	Database credentials below
"""
#Network host of database
DB_HOST = 'localhost'
#Username of database
DB_USER = 'root'
#Database password
DB_PASS = 'cheese'
#Name of specific database
DB_NAME = 'movie_db'

from pymysql import *
from DataStructure import *
import sys


"""
MovieDatabase: Represents a MariaDB database which holds movies, actors, and directors
	Uses MySQL to issue database commands. Makes connection to database on instantiation of MovieDatabase object
params:
			db_host: host name of server
			db_name: name of the database to connect to
			db_user: username to use for databse	
			db_pass: password for database
"""
class MovieDatabase:
	def __init__(self,db_host=DB_HOST,db_name=DB_NAME,db_user=DB_USER,db_pass=DB_PASS):
		self.db_user = db_user
		self.db_host = db_host
		self.db_pass = db_pass
		self.db_name = db_name
		
		reload(sys)
		sys.setdefaultencoding('utf-8')
		
		self.connection = self.db_connect()
		self.cursor = self.db_cursor(self.connection)
		
		
		
	#db_connect connects to databse and returns connection object to that database on success
	"""
		params: None
			Makes connection to database
		returns:
			con: database connection object
	"""
	def db_connect(self):	
		try:
			con = Connection(host=self.db_host,user=self.db_user,password=self.db_pass,database=self.db_name) 
		except:
			print "Error: Couldn't connect to %s database on %s" %(self.db_name,self.db_host)
			return None
		
		return con
		
		
	#simple function to take a connection and return a databse cursor
	"""
		params:
			db_connection: database connection object
		returns:
			database cursor object
	"""
	def db_cursor(self,db_connection):
		return db_connection.cursor()
	
	"""
		Adds Movie object to database
		params: 
			movie: Movie object defined in rnetflix.py
		returns:
			None
		Adds Movie object to connected database
	"""
	def db_add_movie(self,movie):
		if not self.in_db(movie):
			rating = movie.get_imdb_rating()
			if rating != None:
				rating = movie.get_meta_rating_f()
				
			m_rating = movie.get_meta_rating()
			
			if m_rating != None:
				m_rating = movie.get_meta_rating_f()
				
			r_rating = movie.get_rotten_rating()
			
			if r_rating != None:
				r_rating = movie.get_rotten_rating_f()
				
			avg_rating = movie.calc_avg_rating()
			poster = movie.get_poster_link()
			
			#Add movie to database if it's not already in there
			sql = "INSERT INTO `movies` (`Title`,`Year`,`Imdb_Rating`,`Rt_Rating`,`Meta_Rating`,`Avg_Rating`,`Poster_Link`,`Imdb_Url`,`Plot`,`Genre`) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
			self.cursor.execute(sql,(movie.title,movie.year,rating,r_rating,m_rating,avg_rating,poster,movie.get_imdb_url(),movie.get_plot(),movie.get_genre()))
			
			#Get movie ID property from database
			sql = "SELECT `Movie_ID` FROM `movies` WHERE `Title`=%s" if movie.year == None else "SELECT `Movie_ID` FROM `movies` WHERE `Title`=%s AND `Year`=%s"
			args = movie.title if movie.year == None else (movie.title,movie.year)
			res = self.cursor.execute(sql,args)
			
			if res != 1:
				print "Error: Returned %d" %res
				
			movie_id = self.cursor.fetchone()[0]
			
			#Add actors associated with the movie
			actors = movie.get_actors()
			
			for a in actors:
				sql = "SELECT * FROM `Actors` WHERE `Actor_Name`=%s"
				a_name = a.strip()
				args = a_name
				
				if self.cursor.execute(sql,args) == 0: #Actor not found
					sql = "INSERT INTO `Actors` (`Actor_Name`) VALUES(%s)"
					self.cursor.execute(sql,args)
				#Regardless if actor is there or not, we need to add item to the actor_movies table
				
				actor_id = self.get_actor_id(a_name)
				
				#Now update the actor_movies table
				#Vars actor_id, movie_id
				sql = "INSERT INTO `Actor_Movies`(`Movie_Id`,`Actor_ID`) VALUES(%s,%s)"
				args = (movie_id,actor_id)
				self.cursor.execute(sql,args)
			
			#Add directors associated withe movie
			directors = movie.get_directors()
			
			for d in directors:
				sql = "SELECT * FROM `Directors` WHERE `Director_Name`=%s"
				d_name = d.strip()
				args = d_name
				
				if self.cursor.execute(sql,args) == 0: #Director isn't in database
					sql = "INSERT INTO `Directors`(`Director_Name`) VALUES(%s)"
					self.cursor.execute(sql,args)
				
				#Add to Director_Movies table
				director_id = self.get_director_id(d_name)
				
				sql = "INSERT INTO `Director_Movies`(`Movie_ID`,`Director_ID`) VALUES(%s,%s)"
				args = (movie_id,director_id)
				
				self.cursor.execute(sql,args)
				
				
	"""
		Updates the movie in the database with movie object. Used if movie information is incomplete
		params:
			movie: Movie object with information to update
		returns:
			None
	"""
	def db_update_movie(self,movie):
		#Check if movie is in database
		sql = "SELECT `Movie_ID` FROM `movies` WHERE `Title`=%s" if movie.year==None else "SELECT `Movie_ID` FROM `movies` WHERE `Title`=%s AND `Year`=%s"
		args = movie.title if movie.year == None else (movie.title,movie.year)
		
		if self.cursor.execute(sql,args) == 0: #No movie in db
			self.db_add_movie(movie)
			return
			
		movie_id = self.cursor.fetchone()[0]
		
		#Update movie first
		sql = "UPDATE `movies` SET `Title`=%s,`Year`=%s,`Imdb_Rating`=%s,`Rt_Rating`=%s,`Meta_Rating`=%s,`Avg_Rating`=%s,`Rated`=%s,`Poster_Link`=%s, `Imdb_Url`=%s, `Plot`=%s,`Genre`=%s WHERE `Movie_ID`=%s"
		args=(movie.title,movie.year,movie.get_imdb_rating_f(),movie.get_rotten_rating_f(),movie.get_meta_rating_f(),movie.calc_avg_rating(),movie.rated,movie.get_poster_link(),movie.get_imdb_url(),movie.get_plot(),movie.get_genre(),movie_id)
		self.cursor.execute(sql,args)
		
		#Update actors associated with the movie
		actors = movie.get_actors()
		
		if actors:	
			for a in actors:
				sql = "SELECT * FROM `Actors` WHERE `Actor_Name`=%s"
				a_name = a.strip()
				args = a_name
				
				if self.cursor.execute(sql,args) == 0: #Actor not found
					sql = "INSERT INTO `Actors` (`Actor_Name`) VALUES(%s)"
					self.cursor.execute(sql,args)
					actor_id = self.get_actor_id(a_name)
				#Regardless if actor is there or not, we need to add item to the actor_movies table
				else:
					actor_id = self.get_actor_id(a_name)
					
					sql = "UPDATE `Actors` SET `Actor_Name`=%s WHERE `Actor_ID`=%s"
					args = (a_name,actor_id)
					
					self.cursor.execute(sql,args)
				
				#Now update the actor_movies table
				#Vars actor_id, movie_id
				sql = "SELECT * FROM `Actor_Movies` WHERE `Movie_ID`=%s AND `Actor_ID`=%s"
				args = (movie_id,actor_id)
				
				if self.cursor.execute(sql,args) == 0: #Actor movie combo not found
					sql = "INSERT INTO `Actor_Movies`(`Movie_Id`,`Actor_ID`) VALUES(%s,%s)"
					args = (movie_id,actor_id)
				else:
					sql= "UPDATE `Actor_Movies` SET `Movie_ID`=%s, `Actor_ID`=%s WHERE `Movie_ID`=%s"
					args = (movie_id,actor_id,movie_id)
					
				self.cursor.execute(sql,args)
				
		#Update director_movies
		directors = movie.get_directors()
		
		if directors:	
			for d in directors:
				sql = "SELECT * FROM `Directors` WHERE `Director_Name`=%s"
				d_name = d.strip()
				print "[DEBUG] Looking at %s director" %d_name
				args = d_name
				
				if self.cursor.execute(sql,args) == 0: #Director isn't in database
					sql = "INSERT INTO `Directors`(`Director_Name`) VALUES(%s)"
					self.cursor.execute(sql,args)
					print "\t[DEBUG] Inserted %s" %d_name
					
				#Add to Director_Movies table
				director_id = self.get_director_id(d_name)
				sql = "SELECT * FROM `Director_Movies` WHERE `Movie_ID`=%s AND `Director_ID`=%s"
				args =(movie_id, director_id)
				
				if self.cursor.execute(sql,args) == 0:
					sql = "INSERT INTO `Director_Movies`(`Movie_ID`,`Director_ID`) VALUES(%s,%s)"
					args = (movie_id,director_id)
					self.cursor.execute(sql,args)
			
	"""*** "Private" helper functions internal to MovieDatabase***"""
	"""
		Gets Director_ID given Actor_Name
		params:
			director_name: string name of director
		returns:
			director_id: unique ID which identifies director in database
	"""
	def get_director_id(self,director_name):
		sql = "SELECT `Director_ID` FROM `Directors` WHERE `Director_Name`=%s"
		args = director_name
		
		if self.cursor.execute(sql,args) == 0:
			return None
		return self.cursor.fetchone()[0]
		
	"""
		Gets Actor_ID from actor_name	
		params:
			actor_name: string name of actor
		returns:
			actor_id: unique ID which identifies actor in database
	"""	
	def get_actor_id(self,actor_name):
		sql = "SELECT `Actor_ID` FROM `Actors` WHERE `Actor_Name`=%s"
		args = actor_name
		
		if self.cursor.execute(sql,args) == 0:
			return None
		return self.cursor.fetchone()[0]
		
	"""
		Gets actor name from actor_id
		params:	
			actor_id: Unique actor ID value from database
		returns:
			actor_name: string value of actors name
	"""
	def get_actor_name(self,actor_id):	
		sql = "SELECT `Actor_Name` FROM `Actors` WHERE `Actor_ID`=%s"
		args = actor_id
		
		if self.cursor.execute(sql,args) == 0:
			return None
		return self.cursor.fetchone()[0]
		
	"""	
		Gets director name from director_id
		params:
			director_id: Unique director ID value from database
		returns:
			director_name: string value of director name
	"""
	def get_director_name(self,director_id):
		sql = "SELECT `Director_Name` FROM `Directors` WHERE `Director_ID`=%s"
		args = director_id
		
		if self.cursor.execute(sql,args) == 0:
			return None
		return self.cursor.fetchone()[0]
		
		
	"""
		Checks if the movie is already in the database. Uses the title of the movie and, if present, the year
		params:
			movie: Movie object (only title needs to be present in Movie object)
		returns:
			True if movie title is found in the database. False if movie is not in the database.
	"""
	def in_db(self,movie): #Checks whether the movie (by title) is in the database
		title = movie.title.strip()
		year = movie.year.strip()
		sql = "SELECT * FROM `movies` WHERE `Title`=%s AND `Year`=%s" if year else "SELECT * FROM `movies` WHERE `Title`=%s"
		args = (title,year) if year else title
		
		if self.cursor.execute(sql,args) == 0: #No movie entry found
			return False
		else:
			return True
			
	"""
		Executes MySQL command and returns all results
		params:
			sql_command: MySQL string -- command to execute in database
			args_tuple: tuple of arguments to pass to command. Used in the case of string formatting the command
		returns:
			res: list of returned results from the query
	"""
	def command(self,sql_command,args_tuple=None):
		try:
			self.cursor.execute(sql_command,args_tuple)
		except:
			"Error in sql statement"
			return None
			
		res = self.cursor.fetchall()
		return res
	"""
		Commits changes to the database
		params:
			None
		returns:
			None
	"""
	def commit(self):
		self.connection.commit()
		
	"""
		Closes connection to the database
		params:
			None
		returns:
			None
	"""
	def close(self):
		self.connection.close()
		
	"""
		Object destructor. Closes the connection and deletes the object
		params:
			None
		returns:
			None
	"""
	def __del__(self):
		self.connection.close()
