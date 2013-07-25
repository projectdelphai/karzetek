#! /usr/bin/python

from bs4 import BeautifulSoup, SoupStrainer
import urllib.request
import re
import feedparser
import time
import os
import psycopg2
from urllib.parse import urlparse

class Karzetek:
  def db_connect(self):
    urllib.parse.uses_netloc.append("postgres")
    if "DATABASE_URL" not in os.environ:
      os.environ["DATABASE_URL"] = 'postgres://localhost/karzetek_development'
    url = urlparse(os.environ["DATABASE_URL"])
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
        )
    return conn

  def db_close(self,conn):
    conn.close()

  def db_add(self,conn,url,feed,title):
    cur = conn.cursor()
    SQL = "INSERT INTO feeds(url,feed,title) VALUES(%s,%s,%s);"
    data = (url,feed,title)
    cur.execute(SQL, data)
    conn.commit()

  def url_recommendations(self,url):
    rss_feeds=[]
    links = self.get_hyperlinks(url)
    print(time.ctime())
    conn = self.db_connect()
    cur = conn.cursor()
    for link in links:
      cur.execute("SELECT * FROM feeds WHERE url='%s'" % (link))
      response = cur.fetchall()
      if len(response) == 1:
        if not response[0][1] == None:
          rss_feed = { "url": response[0][1], "feed": response[0][2], "title": response[0][3] }
      else:
        rss_feed = self.get_rss(link)
        self.db_add(conn,rss_feed['url'],rss_feed['feed'],rss_feed['title'])
      if not rss_feed['feed'] == None:
        rss_feeds.append(rss_feed)
    self.db_close(conn)
    return rss_feeds
 
  def feed_recommendations(self,rss_link):
    print(time.ctime())
    recommendations=[]
    feed = feedparser.parse(rss_link)
    for entry in feed.entries[:1]:
      recommendations = recommendations + self.url_recommendations(entry.link)
    print(time.ctime())
    return recommendations
  
  def get_hyperlinks(self,url):
    soup = BeautifulSoup(urllib.request.urlopen(url), "lxml", parse_only=SoupStrainer('a'))
    links=[]
    base_url = re.match('(http|https)://[^/]*', url).group(0)
    for a in soup.findAll('a', href=True):
      if not a['href'].startswith(base_url) and a['href'].startswith('http'):
        link_base_url = re.match('(http|https)://[^/]*', a['href']).group(0)
        if link_base_url not in links:
          links.append(link_base_url)
    return links

  def get_rss(self,url):
    try:
      html = urllib.request.urlopen(url, timeout = 1)
    except:
      return { "title": None, "url": url, "feed": None }
    soup = BeautifulSoup(html, "lxml", parse_only=SoupStrainer('head'))
    for a in soup.findAll('link', {'rel' : 'alternate'}, href=True, type=True ):
      if a['rel'] == ['alternate'] and a['href'].startswith('http'):
        return { "title": ' '.join(soup.title.text.split()), "url": url, "feed": a['href'] }
    return { "title": None, "url": url, "feed": None }
