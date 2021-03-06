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
    conn = psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
    return conn

  def db_add(self,data):
    conn = self.db_connect()
    cur = conn.cursor()
    SQL = "INSERT INTO feeds(url,feed,title) VALUES(%s,%s,%s);"
    data = (data['url'],data['feed'],data['title'])
    cur.execute(SQL, data)
    conn.commit()
    conn.close()

  def db_check(self,url):
    conn = self.db_connect()
    cur = conn.cursor()
    cur.execute("SELECT url,feed,title FROM feeds WHERE url='%s'" % (url))
    response = cur.fetchall()
    conn.close()
    return response

  def url_recommendations(self,url,retrieved_urls):
    rss_feeds=[]
    links = self.get_hyperlinks(url)
    for link in links:
      if link not in retrieved_urls:
        response = self.db_check(link)
        if len(response) == 1:
          rss_feed = { "url": response[0][0], "feed": response[0][1], "title": response[0][2] }
        else:
          rss_feed = self.get_rss(link)
          self.db_add(rss_feed)
        if not rss_feed['feed'] == None:
          rss_feeds.append(rss_feed)
    return rss_feeds
 
  def feed_recommendations(self,rss_link):
    print(time.ctime())
    recommendations=[]
    feed = feedparser.parse(rss_link)
    for article in feed.entries[:5]:
      retrieved_urls = [ rss_dict['url'] for rss_dict in recommendations ]
      for dict in self.url_recommendations(article.link,retrieved_urls):
        recommendations.append(dict)
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
    print(url)
    dictionary = { "title": None, "url": url, "feed": None }
    try:
      html = urllib.request.urlopen(url, timeout = 1)
    except:
      return dictionary
    soup = BeautifulSoup(html, "lxml", parse_only=SoupStrainer('head'))
    for a in soup.findAll('link', {'rel' : 'alternate'}, href=True, type=True ):
      if a['rel'] == ['alternate'] and a['href'].startswith('http'):
          try:
              return { "title": str(soup.title.text), "url": url, "feed": a['href'] }
          except:
              return dictionary
    return dictionary
