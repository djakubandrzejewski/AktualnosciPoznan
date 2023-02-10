# AktualnosciPoznan
This is a script that scraps a website for new articles and accidents and posts them on Twitter using the tweepy library. It is using a file "config.ini" to store the Twitter API credentials, and is checking for new articles and accidents in a loop every second.

For new articles, it gets the title, date, and link from the website, and saves it to a file "articules/articules.txt". It then checks if the new article is different from the previous one and if so, posts it on Twitter with the title, date, and link. The same process is done for new accidents, but it is saving it to a different file, "failures/failures.txt".

The script also maintains a history of tweeted articles and accidents to avoid duplicates, using a file "tweet_history_file".
