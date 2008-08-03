#
# thetvdb.py
#
# Functions to grab data from thetvdb.com
#
# (C) 2008 Scott Raynel <scottraynel@gmail.com>
#

import urllib
import urllib2
import urlparse
from xml.etree import ElementTree

def download_series(seriesid, apikey, language = "en"):
        """ Download full series information from thetvdb.com.

            Returns a tuple ( seriesinfo, episodelist )
        """
        url = urlparse.urlunparse(["http",
                                   "www.thetvdb.com",
                                   "/api/" + apikey + "/series/" + seriesid + "/all/" + language + ".xml", 
                                   "", "", ""])
        f = urllib2.urlopen(url)
        tree = ElementTree.ElementTree(file=f)

        # Extract the base series information
        element = tree.find("Series")
        series = ElementTree.ElementTree(element)
        seriesinfo = {}
        for s in series.getiterator():
                if s.text is None:
                        continue
                seriesinfo[s.tag.strip()] = s.text.strip()

        # Extract information for each episode 
        episodelist = []
        for element in tree.getiterator("Episode"):
                episode = ElementTree.ElementTree(element)
                d = {}
                for e in episode.getiterator():
                        if e.text is None:
                                continue
                        d[e.tag.strip()] = e.text.strip()
                episodelist.append(d)

        f.close()
        return (seriesinfo, episodelist)
        
def series_search(series):
        """ Search thetvdb.com for a series and return a list of possible results.

            From this list, select a series id that matches the series which
            can be used later to lookup more info for the specific series.
        """
        query = urllib.urlencode( { "seriesname" : series } )
        url = urlparse.urlunparse(["http",
                                  "www.thetvdb.com",
                                  "/api/GetSeries.php",
                                  "", query, ""])
        f = urllib2.urlopen(url)
        results = ElementTree.ElementTree(file=f)
        r = []
        for element in results.getiterator("Series"):
                series = ElementTree.ElementTree(element)
                d = {}
                for s in series.getiterator():
                        d[s.tag.strip()] = s.text.strip()
                r.append(d)
        f.close()
        return r
