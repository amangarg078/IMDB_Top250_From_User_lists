# IMDB_Top250_From_User_lists

This is a Django appliction that lists top 250 most popular movies based on the user lists.

Edit the Scraping.py file to include the settings of your postgres server.
Also edit the settings.py in the IMDBTop250_From_User_lists/IMDB/IMDB/ folder to include the details of the postgres server.

First run the Scrapig.py to start scraping imdb website and store the data in postgres.

The run the django app. Even if scraping is not complete, Django app will still run and show the data stored so far.

The criteria for choosing the popular movies is simple. The movies appearing in many user lists is obviously very popular. Secondary sorting is done based on the number of user-reviews that the movie got.


