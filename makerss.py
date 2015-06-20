#!/usr/bin/python

# Author : Dave Levy  Date : 16 June 2015   Version 1.3
#
# This program consumes an ello .json file and writes a poor rss file.
# The file name is defined on the command line, the output file is stdout
#
# V1.3 20 June 2015 - default file bug removed
# V1.2 19 June 2015 - cli options added
#

import json, re, sys, getopt, os.path
from pprint import pprint
from datetime import datetime

def parseargs(argv):
	inputfile = '' 
	helpmsg = ' makerss.py -i <inputfile>'
	try:
		opts, args = getopt.getopt(argv, "hi:",["ifile="])
	except getopt.GetoptError:
		print helpmsg
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print helpmsg
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
	return inputfile

# this could just as well sit in the function
if os.path.isfile(parseargs(sys.argv[1:])):
	inputjson = parseargs(sys.argv[1:])
else:
	# needs a stderr message
	inputjson='ello.json' # setting a default

with open(inputjson) as data_file:
	myfeed = json.load(data_file)

print '<?xml version="1.0" encoding="UTF-8" ?>'
print '<rss version="2.0">'
print '<channel>'

def printline(tag,content):
	return "    <" + tag + ">" + content + "</" + tag + ">"

def striptags(istr):
	return re.sub('<[^>]*>', '',istr)

ofmt='%a, %d %b %Y %H:%M:%S +0000' 
pubdate=datetime.strftime(datetime.now(), ofmt)

print printline('title','ello.co/davelevy.rss')
print printline('description','dave levy\'s posts at ello.co')
print printline('link','http://ello.co/davelevy')
print printline('lastBuildDate',pubdate)
print printline('pubDate',pubdate)

def chompw(words,limit=12):
	space=" " ; i=""    # constants
	# procedure
	L=words.split()
	for word in L[0:limit]:
		i = i + space + word
	return i[1:]

def stripbr(s):
	return s.strip('<br>')

maps = { 'update_url': 'link', 'created_at': 'pubDate', 'body': 'title'}
emaps = { 'update_url': '/link', 'created_at': '/pubDate', 'body': '/title'}
#
# it would be nice to do a link item, but ello aren't documemnt the api
#
#attributes = ['update_url', 'created_at', 'body']
attributes = ['created_at', 'body']

# extract the posts, myposts is a list
myposts = myfeed[u'posts']

# These are for format effector to create the indenting

def padline(n):
	# is this really necessary
	return " " * n

for element in myposts:
	print padline(8) + '<item>'
	for property in attributes:
		if property == 'body':
			for item in element['body']:
				# generate title & description
				if item['kind'] == 'text':
					S=item['data']
					d=striptags(S)
					T=d.strip('<br>')
					# also needs to ensure that break is not in the middle of a tag pair
					O={'title': chompw(T), 'desc': T[0:256]}
					# next line needs an error trap
					print ' ' * 12  + '    <%s>%s<%s>' % ( 'title', O['title'], '/title' )
					print padline(12)  + '    <%s>%s<%s>' % ( 'description', O['desc'], '/description' )
		else:
			print padline(12)  + '    <%s>%s<%s>' % (maps[property], element[property], emaps[property])
	print padline(8) + '</item>'

print '</channel>'


