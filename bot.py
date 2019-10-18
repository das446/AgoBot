import urllib2

url = 'https://www.facebook.com/groups/DrexelAGO'

response = urllib2.urlopen(url)
webContent = response.read()

print(webContent)
