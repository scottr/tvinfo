
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

                If a backend other than thetvdb.com is required, provide one
                here.
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
