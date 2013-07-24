Karzetek
=============
Reuben Castelino - projectdelphai@gmail.com

Description
-------------
Karzetek is an anglicized name of [Karze\u0142ek](https://en.wikipedia.org/wiki/Karze%C5%82ek), a Polish myth about diminutive dwarfs who live in mines, protect miners, and guard precious jewels.

Karzetek is a python API that searches through a feed or url for external hyperlinks. It finds any rss feeds associated with those hyperlinks and returns them as a json string. The logic behind karzetek is that if A likes B enough to link to it and you like A then you might like B as well.

Installation
----------------
If you want to install this service for personal use:

 1. pip install feedparser beautifulsoup4 Flask
 1. git clone https://github.com/projectdelphai/karzetek.git
 1. python index.py

It is recommended that you install this all under a virtualenv folder.

Usage
-----------------
The API itself is hosted on karzetek.heroku.com. To get recommendations, the format is as follows:

    karzetek.heroku.com?feed=FEED_URL

The feed url should not contain the http:// prefix and should not be enclosed in quotes.

The process is currently pretty slow and you should recieve the json in about 15 seconds.

Helping Out
----------------
To help out:
 1. Fork repo
 1. Make changes
 1. Change documentation to reflect your changes
 1. Make a pull request

TODO
----------------
More help is always welcome. Here are some outlined goals:
 1. More documentation - Always needed
 1. Speed up searching - Always, database caching may help here
 1. Tests - I don't know how to do this personally.
 1. Database caching - Working on it now
 1. Maybe a wiki? - Not a big enough project yet though.
 1. Integrate with Tiny Tiny RSS - longer term goal

Version
----------------
0.0.1
 * Initial Commit
