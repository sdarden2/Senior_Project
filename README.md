# Senior_Project
Kennesaw State Senior Project - Website to rank Netflix movies according to Imdb, Rotten Rotten Tomatoes, and Metacritic ratings

Admin Guide

Setup & Maintenance

1. Install XAMPP (https://www.apachefriends.org/index.html)

2. In the XAMPP directory, locate the htdocs folder. 

3. Copy the file page3.php into the htdocs folder.

4. In htdocs, create a folder named css and a folder named img. Css contains the Css files and img contains all the image files for the website.

5. Copy style.css into the htdocs/css folder. 

6. Copy images (if applicable) to the htdocs/img folder

7. In the XAMPP directory, navigate to mysql  -> data

8. In htdocs/mysql/data create  folder named movie_db

9. Copy all database files to htdocs/mysql/data/movie_db

10. In the project folder, run netmain.py <e-mail> <password> to scrape the information and update the database

11. Start XAMPP console and start the services: Apache and MySQL. The website should now be ready.

12. At intervals, the admin should routinely run netmain.py and db_updater.py to update the database with new information.


