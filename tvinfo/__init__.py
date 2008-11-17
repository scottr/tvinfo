#
# tvinfo
# (C) 2008 Scott Raynel
#
# Portions (C) 2007,2008 Perry Lorier.
#

""" TV information lookup.

This module provides an easy way to lookup information on TV shows from a
number of different web-services as well as a data model to use to describe
TV series', seasons and episodes.

Support for different web-services is abstracted behind the TVFactory class
which can be used to create model objects which represent data from different 
backends. A backend for thetvdb.com is provided and is the default if no 
backend is manually specified when creating the factory.

"""


import shelve
import os
import re

import backends

debug = False

__cachefile = os.path.join(os.path.expanduser("~"), ".tvcache")
_tv_series_cache = shelve.open(__cachefile, writeback=True)

class TVFactory:
        """ An abstract interface into different TV information web-services.

        Create a TVFactory by specifying a backend to use. 
        """

        def __init__(self, backend, apidata):
                """ Create a new TVFactory instance.

                Give the name of a backend (which can be got from the 
                get_backends() method) as well as any API keys, etc, that
                the backend requests.
                """
                self.__backend = backends.get_backend(backend).get_instance(apidata)
                self.__backend_name = backends.get_backend(backend).module_name

        def series_search(self, seriesname, use_cache=True):
                """ Search the web-service for series matching the seriesname.

                This function will search the web-service for series that match
                the given seriesname. It will return a list of Series objects
                that are possible matches. These will likely only have minimal
                information and will need to be updated with the
                update_series() method.

                The series data is cached locally so it is possible that a call
                to series_search() will result in cached data being returned.
                For example, a series may not have had data for a certain
                episode when the cache was last filled. In this case, the
                update_series() method should be called to force a lookup.

                To bypass the cache entirely, set use_cache to False.
                """
                results = []

                if use_cache:
                        for series in _tv_series_cache.get(self.__backend_name, {}).keys():
                                if seriesname.lower().strip() == series.lower().strip():
                                        if debug:
                                                print "tv: Cache hit: ", series
                                        results.append(_tv_series_cache[self.__backend_name][series])
                        if results:
                                return results

                results = self.__backend.series_search(seriesname)

                # Add the results to the local cache
                for r in results:
                        cache = _tv_series_cache.get(self.__backend_name, {})
                        if cache == {}:
                                _tv_series_cache[self.__backend_name] = cache
                        cache[r.get_title().lower().strip()] = r

                return results

        def update_series(self, series):
                """ Download the full information set for a Series object.

                This will ensure that the Series object contains all the
                information available from the web-service on a series.  This
                should be used after a series search once the actual series is
                determined.
                """
                self.__backend.update_series(series)

def get_backends():
        """ Return a list of dictionaries describing the available backends.
        """
        return backends.get_backends()

patterns=[
	# seasonseasonEepisodeepisode
	r'(.*?)[^A-Za-z0-9] *-? *[Ss]? *([0-9][0-9])[Eex]([0-9]+).*\.([^.]+)$', 
	# seasonEepisodeepisode
	r'(.*?)[^A-Za-z0-9] *-? *[Ss]? *([0-9])[Eex]([0-9]+).*\.([^.]+)$',
	# seasonseasonepisodeepisode
	r'(.*?)[^A-Za-z0-9] *-? *[Ss]? *([0-9][0-9])([0-9][0-9]).*\.([^.]+)$',
	# seasonepisodeepisode
	r'(.*?)[^A-Za-z0-9] *-? *[Ss]? *([0-9])([0-9][0-9]).*\.([^.]+)$',
	# seasonseason.episodeepisode
	r'(.*?)[^A-Za-z0-9] *-? *[Ss]? *([0-9][0-9])\.([0-9][0-9]).*\.([^.]+)$',
	# season.episodeepisode
	r'(.*?)[^A-Za-z0-9] *-? *[Ss]? *([0-9])\.([0-9][0-9]).*\.([^.]+)$',
	# Sseasonseason episodeepisode
	r'(.*?)[^A-Za-z0-9] *-? *[Ss]([0-9]+) ?[Ee]([0-9]+).*\.([^.]+)$',
	# Sseasonseason.Eepisodeepisode
	r'(.*?)[^A-Za-z0-9] *-? *[Ss]([0-9]+).[Ee]([0-9]+).*\.([^.]+)$',
	# Sseasonseason-episodeepisode
	r'(.*?)[^A-Za-z0-9] *-? *[Ss]([0-9]+)-([0-9]+).*\.([^.]+)$',
]

def parse_filename(fname):
        """ Try to figure out the series, season and episode of a filename.

        This uses a bunch of regular expressions to figure out the series name,
        season number and episode number from a filename. If successfull it
        returns a tuple of the form:
                (seriesname,seasonnum,episodenum,ext).
        If parse_filename() fails, None is returned.
        """
	# remove things that look like dates
	fname=re.sub(r'[-/]20[0-9]','',fname)
	fname=re.sub(r'[-/]19[789][0-9]','',fname)
	# Now match it against known patterns
	for i in patterns:
		a=re.match(i,fname)
		if a: 
			name,season,episode,ext=a.groups()
			if debug:
				print "DEBUG: filename:",`fname`
				print "DEBUG: pattern:",`i`
				print "DEBUG: parsed as:",a.groups()
				print "DEBUG: Name:",`name`
				print "DEBUG: Season:",`season`
				print "DEBUG: Episode:",`episode`
				print "DEBUG: Extension:",`ext`
			if re.match(r"^the[^a-z]",name.lower()):
				if debug:
					print "DEBUG: stripping 'the' prefix"
				name=name[3:]
			if name.lower().endswith(", the"):
				if debug:
					print "DEBUG: stripping ', the' suffix"
				name=name[:-5]
			if debug:
				print "DEBUG: final name:",`name`
			return (
				re.sub(r"[^A-Za-z0-9]"," ",name),
				int(season),
				int(episode),
				ext)
	# The filename follows no known pattern.
	return None

