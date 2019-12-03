# this program prints HTML

from HTMLParser import HTMLParser

s='&pound;682m'
h=HTMLParser()

print(h.unescape(s))
