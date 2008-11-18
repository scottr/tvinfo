### tvinfo ###

# tools for performing TV information lookup #

(c) 2008 Scott Raynel <scottraynel@gmail.com>
(c) 2007-2008 Perry Lorier

## Installation ##

You can either run tvrenamer3 directly from your clone, or you can
install tvrenamer3 and the tvinfo package using the included 
Python distutils setup script. Install to your system using:

 $ sudo python setup.py install

## More Info ##

The tvinfo module provides an interface for performing lookups
of TV episode information from various webservices. A default
backend for thetvdb.com is provided along with a TV data model
that describes series, seasons and episodes. 

The tvinfo module provides caching of episode information and
a way for different backends to be easily added.

The tvrenamer3 script is provided as part of the standard package
to help organise your time-shifted TV files. tvrenamer3 will attempt
to determine the series name, season and episode number from a
filename using a fairly comprehensive set of common patterns. The
series will then be looked up using the tvinfo module and if the
series, season and episode is found, the file will be renamed
accordingly. 
