import urllib2
import re
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup as bs


def GetHtml():
    webContent = GetHtmlFromWeb()
    webContent = ExtractImportantHtml(webContent)
    return webContent

def GetHtmlFromFile():
    return open("out.html", "r").read()

def GetHtmlFromWeb():
    url = 'https://www.facebook.com/groups/DrexelAGO'

    response = urllib2.urlopen(url)
    webContent = response.read()
    return webContent

def ExtractImportantHtml(html):
    match = re.findall('<!--(.+)-->',html)
    for i, m in enumerate(match):
        if i==1:
            return m

def GetMostRecentPosts(html):
	posters = []
	tags =  bs.findAll("div", {"data-testid":"post_message"}

html = GetHtml()
print(html)
#posts = GetMostRecentPosts(html)
