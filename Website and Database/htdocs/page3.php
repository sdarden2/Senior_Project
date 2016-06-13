<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<!-- Main webpage for The Netflix Guide. Written in PHP. Uses MariaDB for the database and MySQL for the query language. Uses bootstrap for some styling.
	Pulls movies from the database and lists them. Lists them sorted by IMDB rating, Rotten Tomatoes rating, Metacritic rating, or Average rating, whichever
	the user chooses. 
-->
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
	<meta content="text/html; charset=utf-8" http-equiv="Content-Type" />

	<title>Netflix Guide</title>

	<!-- Custom stylsheet for this page -->
	<link rel="stylesheet" href="css/design_css.css" type="text/css">
	<!-- Next 3 links and scripts are to import bootstrap -->
	 <!-- Latest compiled and minified CSS -->
	<link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">

	<!-- jQuery library -->
	<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>

	<!-- Latest compiled JavaScript -->
	<script type="text/javascript" src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
</head>

<body>

	<?php
		/*
			Handles how the movies are sorted. Options are Imdb Rating, Rotten Tomatoes Rating, Metacritic rating or
			Average rating. Always sorts from highest rated to lowest rated.
		*/
		if (isset($_POST['sort'])){
		$sort_by = $_POST['sort'];
		
		if ($sort_by == "imdb")
			{
				header("Location: ".$_SERVER['PHP_SELF']."?sort=imdb_desc");
			}
		if ($sort_by == "rt")
		{
			header("Location: ".$_SERVER['PHP_SELF']."?sort=rt_desc");
		}
		if ($sort_by == "meta")
		{	
			header("Location: ".$_SERVER['PHP_SELF']."?sort=meta_desc");
		}
		if ($sort_by == "avg")
		{
			header("Location: ".$_SERVER['PHP_SELF']."?sort=avg_desc");
		}
		}
	?>

	<div class="headers">
		<h2 style="color:#ECF2F2; text-align:center">Netflix Guide</h2>
		<a href="<?php echo $_SERVER['PHP_SELF'] ?>"><span class="hidden_span"></span></a> <!-- Clicking the main image returns to home page -->
	</div>

	<!-- Radio buttons to select how to sort the movies -->
	<div class="radios">
		<h2 class="sort_text">Sort By</h2>
		<form class="sort_form" method="post" action="page3.php">
			<input class="c1" onchange="this.form.submit();" type="radio" name="sort" value="imdb">Imdb Rating&nbsp&nbsp&nbsp
			<input class ="c1" onchange="this.form.submit();" type="radio" name="sort" value="rt">Rotten Tomatoes Rating&nbsp&nbsp&nbsp
			<input class ="c1" onchange="this.form.submit();" type="radio" name="sort" value="meta">Metacritic Rating&nbsp&nbsp&nbsp
			<input class="c1" onchange="this.form.submit();" type="radio" name="sort" value="avg">Average Rating&nbsp
		</form>
	</div>
	
	<!-- PHP script to connect to database and build page -->
	<?php
		/*Database credentials*/
		$hostname = 'localhost';
		$user = 'root';
		$pass = 'cheese';
		$db_name = 'movie_db';
		
		$con = new mysqli($hostname,$user,$pass,$db_name);
		if($con->connect_error)
		{
			die("Connection Error: ".$con->connect_error);
		}
		
		
		$query_str = "SELECT Title,Imdb_Rating,Rt_Rating,Meta_Rating,Avg_Rating,Poster_Link,Year,Imdb_Url,Movie_ID,Plot,Genre,Rated FROM movies";
		
		/*search_genre, search_actor, and search_director are search parameters. They allow the user to view movies grouped by specific actors, directors, or genres.
			Currently, there is not search function that implements these, however, they are implemented as tags on the web page. Example, if a user wants to find all movies
			currently on netflix directed by Quentin Tarantino, a user can find a movie by Quentin Tarantino and click on his name. Then all movies directed by that director
			will show up. The same works for Genre and Actors. A user can manually search for an actor, genre, or director by supplying the query strings ?search_genre=genre,
			?search_actor=actor,?search_director=director after the page name in the url.
			*/
		if (isset($_GET['search_genre']))
		{
			/*search by actor,director,genre, title*/
			$genre = $_GET['search_genre'];
			$query_str = "SELECT Title,Imdb_Rating,Rt_Rating,Meta_Rating,Avg_Rating,Poster_Link,Year,Imdb_Url,Movie_ID,Plot,Genre,Rated FROM movies WHERE Genre LIKE \"%".$genre."%\"";
					
		}
		if (isset($_GET['search_actor']))
		{	
			$actor_name = str_replace("_"," ",$_GET['search_actor']);
			$query_str = 'SELECT Title,Imdb_Rating,Rt_Rating,Meta_Rating,Avg_Rating,Poster_Link,Year,Imdb_Url,Movie_ID,Plot,Genre,Rated FROM movies WHERE 
			Movie_ID in (SELECT Movie_ID FROM Actor_Movies WHERE Actor_ID in (SELECT Actor_ID FROM Actors WHERE Actor_Name="'.$actor_name.'"))';
			
		}
		if (isset($_GET['search_director']))
		{
			$director_name = $_GET['search_director'];
			$director_name = str_replace("_"," ",$director_name);
			$query_str = 'SELECT Title,Imdb_Rating,Rt_Rating,Meta_Rating,Avg_Rating,Poster_Link,Year,Imdb_Url,Movie_ID,Plot,Genre,Rated FROM movies WHERE Movie_ID in (SELECT Movie_ID FROM Director_Movies 
			WHERE Director_ID IN (SELECT Director_ID FROM Directors WHERE Director_Name="'.$director_name.'"))';

		}
		/*
			sort parameters are just passed as php parameters in the form of ?sort=sort_type. Sort types are listed below in the if else statement under
			$sort_param
		*/
		if (!isset($_GET['sort']))
		{
			$query_str.=" ORDER BY Imdb_Rating DESC";
		}
		else
		{
			$sort_param = $_GET['sort'];
			if ($sort_param == "imdb_desc")
			{
				$query_str.=" ORDER BY Imdb_Rating DESC";
			}
			elseif ($sort_param == "imdb_asc")
			{
				$query_str.=" ORDER BY Imdb_Rating ASC";
			}
			elseif ($sort_param == "rt_desc")
			{
				$query_str.=" ORDER BY Rt_Rating DESC";
			}
			elseif ($sort_param == "rt_asc")
			{
				$query_str.=" ORDER BY Rt_Rating ASC";
			}
			elseif ($sort_param == "meta_desc")
			{
				$query_str.=" ORDER BY Meta_Rating DESC";
			}
			elseif ($sort_param == "meta_asc")
			{
				$query_str.=" ORDER BY Meta_Rating ASC";
			}
			elseif ($sort_param == "avg_desc")
			{
				$query_str.=" ORDER BY Avg_Rating DESC";
			}
			elseif ($sort_param == "avg_asc")
			{
				$query_str.=" ORDER BY Avg_Rating ASC";
			}
			
		}
		
		/*$res = $con->query("SELECT Title,Imdb_Rating,Rt_Rating,Meta_Rating,Avg_Rating,Poster_Link,Year,Movie_ID,Plot,Genre FROM movies where Avg_Rating >= 5.0 order by Avg_Rating DESC");*/
		$res = $con->query($query_str);
		$vals = $res->fetch_all();
		
		
		/*width < 150, height < 180*/
		$poster_width = 135;
		$poster_height = 175;
		
		/*Pull all the information from the query*/
		foreach($vals as $i)
		{
			$title = $i[0];
			$rating = $i[1];
			$rt_rating = $i[2];
			$meta_rating = $i[3];
			$avg_rating = $i[4];
			$poster_link = $i[5];
			$year = $i[6];
			$imdb_url = $i[7];
			$img_name = link_to_fname($title,$year);
			if (file_exists("./img/".$img_name))
			{
				$img = $img_name;
			}
			else
			{
				$img = "no_movie.png";
			}
			
			$movie_id = $i[8];
			$plot = $i[9];
			$genre = $i[10];
			$rated = $i[11];
			
			$actor_query = "SELECT Actor_Name FROM Actors WHERE Actor_ID in (SELECT Actor_ID from Actor_Movies WHERE Movie_ID=".$movie_id.")";
			$actors = $con->query($actor_query)->fetch_all();
			
			$director_query = "SELECT Director_Name FROM Directors WHERE Director_ID in (SELECT Director_ID FROM Director_Movies WHERE Movie_ID=".$movie_id.")";
			$director = $con->query($director_query)->fetch_all();
			/*create movie_item creates the contents of the page with the given movie information retrieved from the database*/
			create_movie_item($title,$year,$rating,$rt_rating,$meta_rating,$avg_rating,$img,$actors,$director,$genre,$plot,$rated,$imdb_url);
		}	
		
		/*Returns the filename to the movie poster given the title $t and year $y*/
		function link_to_fname($t,$y)
		{
			$tmp = trim($t," ");
			$tmp = str_replace(" ","_",$tmp);
			$tmp = str_replace(":","_",$tmp);
			$tmp = str_replace("\"","\'",$tmp);
			return $tmp."_".$y.".jpg";
		}
		
		/*This function creates the movie items for the page given the parameters
			params: (all params are strings)
				$title: movie title
				$year: movie year release
				$imdb_rating: Imdb rating
				$rt_rating: Rotten Tomatoes Rating
				$meta_rating: Metacritic rating
				$avg_rating: Average rating
				$img: local path to movie poster image file
				$actors: list of strings of actors
				$director: director name
				$genre: string which lists the generes of the movie
				$plot: short plot of the movie
				$rated: MPAA rating of the movie
				$imdb_url: URL of the IMDB page of the movie
			
			returns:
				NULL: creates the movie div on the page 
		*/
		function create_movie_item($title,$year,$imdb_rating,$rt_rating,$meta_rating,$avg_rating,$img,$actors,$director,$genre,$plot,$rated,$imdb_url)
		{
			/*Creates movie image part*/
			print("<div class=\"movie_box\"><div class=\"movie_poster\">");
			print("<img class=\"poster_pic\" src=/img/".$img." alt=".$title." width=\"130\" height=\"210\"></div>");
			print("<div class=\"info_box\"><h1 class=\"movie_title\" style=\"color:white\">".$title." (".$year.")</h1>");
			print("<div class=\"movie_info\">");
			print("<p>".$plot."</p>");
			print("<p>Genres: ");
			
			$genre = explode(",",$genre);
			$g_length = count($genre);
			
			for ($t = 0; $t<$g_length;$t++)
			{
				if ($t == $g_length-1)
					print(trim($genre[$t]));
				else
				{
					print(trim($genre[$t]).",");
				}
			}
			
			/*Adds movie rating*/
			print("</p>");
			print("<p>Rated: ".$rated."</p></div>");
			print("<div class=\"credits\">");
			print("<p class=\"name_item\">Director:</p>");
			
			$dir_name = $director[0][0];
			$dir_query_name = str_replace(" ","_",$dir_name);
			
			/*Adds director*/
			print("<p class=\"name_item\">&nbsp&nbsp<a href=\"?search_director=".$dir_query_name."\" data-toggle=\"tooltip\" title=\"Search movies directed by ".$dir_name."\">".$dir_name."</a></p>");
			print("<p class=\"name_item\">Actors: </p>");
			
			$a_length = count($actors);
			
			/*Adds actors*/
			for ($t=0;$t<$a_length;$t++)
			{
				$a_name = trim($actors[$t][0]);
				$query_a_name = str_replace(" ","_",$a_name);
				print("<p class=\"name_item\">&nbsp&nbsp<a href=\"?search_actor=".$query_a_name."\" data-toggle=\"tooltip\" title=\"Search movies with ".$a_name."\">".$a_name."</a></p>");
			}
			
			print("</div>");
			print("<div class=\"movie_ratings\">");
			
			if ($imdb_rating == NULL || strlen($imdb_rating) < 3)
				$imdb_rating = "N/A";
			
			if ($rt_rating == NULL || strlen($rt_rating) < 3)
				$rt_rating = "N/A";
			
			if ($meta_rating == NULL || strlen($meta_rating) < 3)
				$meta_rating = "N/A";
				
			if ($imdb_rating != "N/A")
				print("<p><img class=\"rating_img\" src=\"/img/imdb_img.png\" width=\"50\" height=\"50\"><a class=\"movie_rating_text\" href=\"".$imdb_url."\" target=\"_blank\">".$imdb_rating."</a></p>");
			else
				print("<p><img class=\"null_rating_img\" src=\"/img/imdb_img.png\" width=\"50\" height=\"50\"><a class=\"null_movie_rating_text\">".$imdb_rating."</a></p>");
			if ($rt_rating != "N/A")
				print("<p><img class=\"rating_img\" src=\"/img/rotten_t_img.png\" width=\"50\" height=\"50\"><a class=\"movie_rating_text\">".$rt_rating."</a></p>");
			else
				print("<p><img class=\"null_rating_img\" src=\"/img/rotten_t_img.png\" width=\"50\" height=\"50\"><a class=\"null_movie_rating_text\">".$rt_rating."</a></p>");
			if ($meta_rating != "N/A")
				print("<p><img class=\"rating_img\" src=\"/img/metacritic_black_reflection.png\" width=\"50\" height=\"50\"><a class=\"movie_rating_text\">".$meta_rating."</a></p>");
			else
				print("<p><img class=\"null_rating_img\" src=\"/img/metacritic_black_reflection.png\" width=\"50\" height=\"50\"><a class=\"null_movie_rating_text\">".$meta_rating."</a></p>");



			print("</div>");
			print("<div class=\"avg_rating_box\"><p class=\"avg_rating_text\">Average Rating</p>");
			print("<div class=\"avg_rating_div\"><p class=\"avg_rating_number\">".$avg_rating."</p>");
			print("</div></div></div></div>");

			
			

			


		}		
		?>

</body>

</html>
