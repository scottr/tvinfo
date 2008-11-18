""" Data model for TV series, seasons and episodes.

"""

class Series:
        """ A TV Series.

            Generally, this class is not instantiated directly, but instead is
            created by the series_search() method of the tvinfo module.
        """

        def __init__(self):
                self.__title = ""
                self.__overview = ""
                self.__language = ""
                self.__first_aired = ""
                self.__banner_uri = []
                self.__actors = []
                self.__seasons = {} 
                self.__backend_data = {}

        def get_title(self):
                """ Get the title of the series.
                """
                return self.__title

        def set_title(self, title):
                """ Set the title of the series.
                """
                self.__title = title

        def set_language(self, language):
                """ Set the language of the series.
                """
                self.__language = language

        def get_language(self):
                """ Get the language of the series.
                """
                return self.__language
        
        def get_overview(self):
                """ Get the overview/synopsis of the series.
                """
                return self.__overview

        def set_overview(self, overview):
                """ Set the overview/synopsis of the series.
                """
                self.__overview = overview

        def get_first_aired_date(self):
                """ Return the first aired date as a Python datetime.date object.
                """
                return self.__first_aired

        def set_first_aired_date(self, day, month, year):
                """ Set the first aired date.
                """
                self.__first_aired = datetime.date(year, month, day)

        def get_banner_uris(self):
                """ Get a list of URIs that describe "banners" for this series.
                """
                return self.__banner_uri

        def set_banner_uris(self, uris):
                """ Set a list of URIs that describe "banners" for this series.
                """
                self.__banner_uri = uris

        def get_actor_list(self):
                """ Get a list of actors in this series.
                """
                return self.__actors

        def set_actor_list(self, actors):
                """ Set the list of actors in this series.
                """
                self.__actors = actors

        def get_backend_data(self, key):
                """ Return an item from the backend's private data store. 

                For example, backends can use this to store season id's, etc.
                """
                return self.__backend_data.get(key, None)

        def set_backend_data(self, key, value):
                """ Sets a key/value pair in the backend private data store.
                """
                self.__backend_data[key] = value

        def get_episode(self, season, episode):
                """ Lookup an episode in this series.

                    Given a season and episode number, returns an Episode object 
                    describing the episode. If the episode is not found, None is
                    returned, indicating that the cache may need to be updated.
                """
                if self.__seasons == {}:
                        return None

                if self.__seasons.has_key(season) == False:
                        return None

                return self.__seasons[season].get_episode(episode)

        def get_season(self, season_number):
                """ Get the Season object for season_number.
                """
                return self.__seasons.get(season_number, None)

        def set_season(self, season_number, season):
                """ Set the Season object for season_number.
                """
                self.__seasons[season_number] = season

        def get_seasons(self):
                """ Return a sorted list of Season objects for this Series.

                """
                return [ s for snum, s in sorted(self.__seasons.items()) ]

class Season:
        """ Describes a TV season.
        """
        def __init__(self):
                self.__season_number = ""
                self.__banner_uris = []
                self.__episodes = {}

        def get_season_number(self):
                """ Return the season number of this season.
                """
                return self.__season_number

        def set_season_number(self, season_number):
                """ Set the season number of this season.
                """
                self.__season_number = season_number

        def get_banner_uris(self):
                """ Return a list of URIs describing banners for this season.
                """
                return self.__banner_uris

        def set_banner_uris(self, uris):
                """ Set the list of URIs describing banners for this season.
                """
                self.__banner_uris = uris

        def set_episode(self, episode_number, episode):
                """ Set the Episode object for episode_number.
                """
                self.__episodes[episode_number] = episode

        def get_episode(self, episode_number):
                """ Get an Episode by episode number.
                """
                return self.__episodes.get(episode_number, None)

        def get_episodes(self):
                """ Get the episodes for this season as a sorted list. 
                """
                return [ e for enum, e in sorted(self.__episodes.items()) ]

class Episode:
        """ Describes a single TV episode.
        """
        def __init__(self):
                self.__title = ""
                self.__overview = ""
                self.__episode_number = ""
                self.__banner_uris = []

        def get_title(self):
                """ Get the title of this episode.
                """
                return self.__title

        def set_title(self, title):
                """ Set the title of this episode.
                """
                self.__title = title

        def get_banner_uris(self):
                """ Get the list of URIs describing banners for this episode.
                """
                return self.__banner_uris

        def set_banner_uris(self, uris):
                """ Set the list of URIs describing banners for this episode.
                """
                self.__banner_uris = uris

        def get_overview(self):
                """ Get the overview/synopsis of this episode.
                """
                return self.__overview

        def set_overview(self, overview):
                """ Set the overview/synopsis of this episode.
                """
                self.__overview = overview

        def get_episode_number(self):
                """ Get the episode number of this episode.
                """
                return self.__epsiode_number
        
        def set_episode_number(self, episode_number):
                """ Set the episode number for this episode.
                """
                self.__episode_number = episode_number

