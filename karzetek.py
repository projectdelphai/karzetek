#! /usr/bin/python

from bs4 import BeautifulSoup, SoupStrainer
import urllib.request
import re
import feedparser
import time

class Karzetek:
  def url_recommendations(self,url):
    rss_feeds=[]
    links = self.get_hyperlinks(url)
    for link in links:
      rss_feed = self.get_rss(link)
      if not rss_feed == None:
        rss_feeds.append(rss_feed)
    return rss_feeds
 
  def feed_recommendations(self,rss_link):
    print(time.ctime())
    feed = feedparser.parse(rss_link)
    recommendations=[]
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
      return
    soup = BeautifulSoup(html, "lxml", parse_only=SoupStrainer('head'))
    for a in soup.findAll('link', {'rel' : 'alternate'}, href=True, type=True ):
      if a['rel'] == ['alternate'] and a['href'].startswith('http'):
        return { "title": ' '.join(soup.title.text.split()).encode('utf-8'), "site": url, "feed": a['href'] }
