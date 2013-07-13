#! /usr/bin/python

from bs4 import BeautifulSoup
import urllib.request
import re
import feedparser

class Karzetek:
  def url_recommendations(self,url):
    rss_feeds=[]
    for link in self.get_hyperlinks(url):
      rss_feed = self.get_rss(link)
      if not rss_feed == None:
        rss_feeds.append(rss_feed)
    return rss_feeds
 
  def feed_recommendations(self,rss_link):
    feed = feedparser.parse(rss_link)
    recommendations=[]
    for entry in feed.entries[:1]:
      recommendations = recommendations + self.url_recommendations(entry.link)
    return recommendations
  
  def get_hyperlinks(self,url):
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "lxml")
    links=[]
    base_url = re.match('(http|https)://[^/]*', url).group(0)
    for a in soup.findAll('a'):
      try:
        link = a["href"]
      except:
        continue
      if not link.startswith(base_url) and link.startswith('http'):
        links.append(link)
    links = self.filter_for_dups(links)
    return links
  
  def filter_for_dups(self,array):
    filtered_array=[]
    for element in array:
      base_url = re.match('(http|https)://[^/]*', element).group(0)
      if base_url not in filtered_array:
        filtered_array.append(base_url)
    return filtered_array

  def get_rss(self,url):
    try:
      html = urllib.request.urlopen(url, timeout = 10)
    except:
      return
    soup = BeautifulSoup(html, "lxml")
    for a in soup.findAll('link'):
      if a.has_attr('rel') and a.has_attr('type') and a.has_attr('href'):
        if a['rel'] == ['alternate']:
          return { "title": ' '.join(soup.title.text.split()).encode('utf-8'), "site": url, "feed": a['href'] }
