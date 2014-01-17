#! /usr/bin/python

from flask import Flask
from flask import request
from karzetek import Karzetek

app = Flask(__name__)

@app.route('/')
def index():
  input = request.args.get('feed', '')
  if len(input) < 1:
    return "No Input. Refresh this page with '?feed=<feedURL>' appended at the end"
  else:
    recommended_feeds = Karzetek().feed_recommendations(input)
    return str(recommended_feeds)

if __name__ == '__main__':
  app.debug = True
  app.run()
