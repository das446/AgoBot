import urllib2
import re
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup as bs
import facebook

token = open(os.path.join("files","fb_key.txt")).read()

graph = facebook.GraphAPI.(access_token=token, version="5.0")


