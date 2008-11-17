#!/usr/bin/python
#
# tvinfo
#
# Parse the IMDB episode listing for a specfic TV Show and extract information
# about each episode
#
# (C) 2007 Scott Raynel <scottraynel@gmail.com>
#
# $Id$

IMDB_PREFIX = "http://www.imdb.com/title"
EPGUIDES_PREFIX = "http://www.epguides.com"

import sys
import os
import re
import urllib
from HTMLParser import HTMLParser

class IMDBEpisodesParser(HTMLParser):

	def __init__(self):
		self.episodes = []
		self.episode = None
		self.expecting = ""
		HTMLParser.__init__(self)

	def handle_starttag(self, tag, attrs):
		if tag == "b":
			if self.episode is None:
				return
			self.expecting = "air_date"

		elif tag == "a":
			if len(attrs) != 1:
				return
			(k,v) = attrs[0]
			if k == "name":
				if v.startswith("year-") == False:
					return
				if self.episode != None:
					self.episodes.append(self.episode)
				self.episode = {}
				return
			elif k == "href":
				if self.episode is None:
					return
				self.episode['imdb_link'] = IMDB_PREFIX + v
				self.expecting = "title"
		elif tag == "h4":
			if self.episode is None:
				return
			self.expecting = "number"
		elif tag == "br":
			if self.episode is None:
				return
			if self.expecting == "air_date":
				self.expecting = "plot"
			else:
				self.expecting = ""
		else:
			self.expecting = ""
			

	def handle_data(self, data):
		if self.episode is None:
			return

		if self.expecting == "":
			return
		elif self.expecting == "number":
			parts = data.split(" ")
			self.episode['season'] = int(parts[1].replace(',',''))
			self.episode['episode'] = int(parts[3].replace(':',''))
		elif self.expecting == "air_date":
			parts = data.split(":")
			if len(parts) != 4:
				return
			self.episode['air_date'] = parts[1].strip()
		else:
			self.episode[self.expecting] = data

def get_episodes_for_show(name):
        """ Given a show name, e.g. "Dexter", return the episode information.
        This first goes out to epguides.com to find the appropriate IMDB URL
        and then parses the IMDB episodes guide for the show, returning the
        episodes as a list of dictionaries.
        Returns None if the show cannot be found.
        """
        url = get_imdb_link_for_show(name)
        if (url == None):
                return None
        return parse_imdb_url(url)

r = re.compile("\"http.*\"")

def get_imdb_link_for_show(name):
        """ Check epguides.com for the show "name" and return its IMDB URL
        """
        (filename, headers) = urllib.urlretrieve(EPGUIDES_PREFIX + "/" + name)
        if (filename == None):
                return None
        f = open(filename, 'r')
        for line in f.readlines():
                if (line.find("<h1>") != -1):
                        s = r.search(line)
                        if s == None:
                                continue
                        f.close()
                        return line[s.start():s.end()].strip("\"") + "/episodes"
        f.close()
        return None

def parse_imdb_url(url):
        """ Takes an URL to an IMDB episodes list, e.g.
        "http://www.imdb.com/title/tt773262/episodes" and returns the episode
        information.  
        """
        (filename, headers) = urllib.urlretrieve(url)
        if (filename == None):
                return None
        p = IMDBEpisodesParser()
        f = open(filename, 'r')
        for line in f.readlines():
                p.feed(line)
        f.close()
        p.close()
        return p.episodes
            
def print_usage():
        print "Usage: " + sys.argv[0] + " [imdb_id|show_name]"

imdb_id_re = re.compile("tt[0-9]*$")
if __name__ == "__main__":
        if len(sys.argv) != 2:
                print_usage()
                sys.exit(1)

        input = sys.argv[1]
        if (imdb_id_re.match(input) != None):
                print "Looking up episodes for IMDB ID " + input + "..."
                print parse_imdb_url(IMDB_PREFIX + "/" + input + "/episodes")
        else:
                print "Looking up episodes for show " + input + "..."
                print get_episodes_for_show(input)


