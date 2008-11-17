#
# thetvdb.py
#
# Functions to grab data from thetvdb.com
#
# (C) 2008 Scott Raynel <scottraynel@gmail.com>
#

from tvinfo import model

import urllib
import urllib2
import urlparse
from xml.etree import ElementTree

debug = False

module_name = "thetvdb"
module_description = "Backend for thetvdb.com web-service"
module_api_desc = "Supply a single string with the API key"

def get_instance(api):
        return TheTVDBBackend(api)

class TheTVDBBackend:
        def __init__(self, api_auth):
                self.__apikey = api_auth

        def series_search(self, seriesname):
                results = self.__series_search(seriesname)
                retval = []
                for result in results:
                        series = model.Series()
                        self.__marshal(result, series)
                        retval.append(series)
                return retval

        def update_series(self, series):
                seriesid = series.get_backend_data("seriesid")
                (s, episodes) = self.__download_series(seriesid)

                # We may have already got some of this information but the 
                # full query will have returned much more information about the series
                # than the series search will have, so we update again.
                self.__marshal(s, series)
               
                for ep in episodes:
                        # Get the Season or create it if it doesn't exist.
                        snum = int(ep["SeasonNumber"])
                        season = series.get_season(snum)
                        if season == None:
                                season = model.Season()

                        season.set_season_number(snum)
                        series.set_season(snum, season)

                        # Get the Episode or create it if it doesn't exist.
                        enum = int(ep["EpisodeNumber"])
                        episode = season.get_episode(enum)
                        if episode == None:
                                episode = model.Episode()

                        episode.set_title(ep.get("EpisodeName", ""))
                        episode.set_overview(ep.get("Overview", ""))
                        episode.set_episode_number(enum)

                        season.set_episode(enum, episode)
                        
        def __marshal(self, tvdbinfo, series):
                """ Marshal raw tvdb info into the Series model object.
                """
                series.set_title(tvdbinfo["SeriesName"])

                series.set_backend_data("seriesid", tvdbinfo["id"])

                if tvdbinfo.has_key("language"):
                        series.set_language(tvdbinfo["language"])
                elif tvdbinfo.has_key("Language"):
                        series.set_language(tvdbinfo["Language"])

                if tvdbinfo.has_key("Actors"):
                        actors = tvdbinfo["Actors"].split("|")
                        series.set_actor_list([x for x in actors if x != ""])

                ##series.set_first_aired_date()
#
 #               if tvdbinfo.has_key("FirstAired"):
  #                      series.first_aired = tvdbinfo["FirstAired"]

                series.set_overview(tvdbinfo.get("Overview", ""))

                if tvdbinfo.has_key("banner"):
                        series.banner_uri = tvdbinfo["banner"]

       
        def __download_series(self, seriesid, language = "en"):
                """ Download full series information from thetvdb.com.
                    Returns a tuple ( seriesinfo, episodelist )
                """
                url = urlparse.urlunparse(["http",
                                           "www.thetvdb.com",
                                           "/api/" + self.__apikey + \
                                           "/series/" + seriesid + "/all/" \
                                           + language + ".xml", 
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
                        if s.tag.strip() == "banner":
                                s.text = urlparse.urljoin("http://www.thetvdb.com/banners/", s.text.strip())
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
                
        def __series_search(self, series):
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
                                if s.tag.strip() == "banner":
                                        s.text = urlparse.urljoin("http://www.thetvdb.com/banners/", s.text.strip())
                                d[s.tag.strip()] = s.text.strip()
                                if debug:
                                        print s.tag.strip(),"=",d[s.tag.strip()]
                        r.append(d)
                f.close()
                return r


