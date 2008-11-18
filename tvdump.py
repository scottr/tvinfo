#!/usr/bin/env python
#
# tvdump.py
# 
# Dump series search results, mainly for testing.
#

import tvinfo
import sys

if len(sys.argv) < 2:
        print "usage: %s [options] <series_name>" % sys.argv[0]
        print "  options:"
        print "   --update   Force a full update, pull down episode list, etc."
        print "              You should only have to do this once for a series."
        print "   --show-overviews   Show the series and episode overviews."
        print "   --exact    Only show exact series name matches."
        sys.exit(1)

update = False
overviews = False
exact = False

for i in sys.argv:
        if i == "--update":
                update = True
        if i == "--show-overviews":
                overviews = True
        if i == "--exact":
                exact = True

series_title = sys.argv[-1]

tv = tvinfo.TVFactory("thetvdb", "13937A4BBADA99FC")

print "searching for: " + series_title

search_results = tv.series_search(series_title)

for result in search_results:
        if exact and result.get_title().strip().lower() != series_title.strip().lower():
                continue
        if update:
                tv.update_series(result)
        print "Series Title: " + result.get_title()
        if overviews:
                print "Series Overview: " + result.get_overview()
        for season in result.get_seasons():
                for episode in season.get_episodes():
                        print "    %02ix%02i: %s" % (season.get_season_number(),  \
                                                episode.get_episode_number(), \
                                                episode.get_title())  
                        if overviews:
                                print "      " + episode.get_overview()
        print



