import requests
from requests.auth import HTTPBasicAuth

from modules.exceptions.login import IncorrectAuthException
from modules.login import verify_login
from modules.departures import get_departures_f
from modules.pricing import get_pricing_f
from modules.stations import get_stations_f


class NSApi:
    def __init__(self, username: str, password: str):
        """
        Creates an NSApi object to handle further API processing.

        :param username: Username for the NS Api.
        :param password: Password for the NS Api.
        """

        self.r = requests.Session()
        self.r.auth = HTTPBasicAuth(username, password)

        self._check_logged_in()

    def _check_logged_in(self):
        """
        Throws an exception if the object is not logged in.

        :return: Nothing.
        """

        if not verify_login(self.r):
            raise IncorrectAuthException("Incorrect username or password!")

    def get_departures(self, station: str):
        """
        Gets the departures from a station as a dictionary.
        The dictionary keys are the train ids as strings.

        A single train object as k = v:
        train_id = {
            "journey":          str: The train ID,
            "departure_time":   datetime: The train's departure time.
            "destination":      str: The train's destination.
            "train_type":       str: The type of train.
            "carrier":          str: The company which handles the train.
            "departs_from": {
                "platform":     str: The platform from which it leaves.
                "changed":      bool: Whether the platform has changed or not.
            },
            "comments":         list: A list of comments left by NS.

            --- The extra data, may not always be in the dict ---
            "delay":            str: The delay of the train, if there is a delay.
            "delay_text":       str: The reason for the delay, if any.
            "route":            str: The stations the train passes on its way.
            "tip":              str: A tip left by NS, if any.
        }

        :param station: The station of which to get the departures.
        :return: A dictionary with train information.
        :rtype: dict
        """

        self._check_logged_in()

        return get_departures_f(self.r, station)

    def get_stations(self):
        """
        Gets all the stations as a dictionary.
        The dictionary keys are the station codes as strings.

        A single station object as k = v:
        station_id = {
            "code":             str: The station code.
            "type":             str: The type of station.
            "name": {
                "short":        str: The station name shortened the most.
                "middle":       str: The station name shortened a little.
                "full":         str: The station name not shortened.
            },
            "country":          str: The country code for the station.
            "uic":              str: The UIC (Union Internationale de Chemins de fer, ID of the International Railway Union).
            "lat":              str: The latitude of the station.
            "lon":              str: The longitude of the station.
            "synonyms":         list: A list of other names for the station.
        }

        :return: A dictionary with station information.
        :rtype: dict
        """

        self._check_logged_in()

        return get_stations_f(self.r)

    def get_price(self, from_station, to_station, via_station=None, date=None):
        """
        Gets all the fares for one station to another.
        The dictionary keys are the names of the carrier.

        A single price object as k = v:
        carrier_name = {
            "carrier":          str: The name of the carrier.
            "price_units":      str: Prices are calculated (on the NS side of things) with these price units.
            "return": {         dict: Fares for a return journey.
                "first-class": {            dict: Fares for a first-class return journey.
                    "full":                 float: Full fare.
                    "20-off":               float: Fare with 20% off.
                    "40-off":               float: Fare with 40% off.
                },
                "standard-class": {         dict: Fares for a standard-class return journey.
                },
            },
            "one-way": {        dict: Fares for a one-way journey.
                "first-class": {            dict: Fares for a first-class one-way journey.
                },
                "standard-class": {         dict: Fares for a standard-class one-way journey.
                }
            }
        }

        :param from_station: The station code of the departure station.
        :param to_station: The station code of the arrival station.
        :param via_station: A station in between these (optional).
        :param date: The date of departure (optional).
        :return: A dictionary with pricing information.
        :rtype: dict
        """

        self._check_logged_in()

        return get_pricing_f(self.r, from_station, to_station, via_station, date)
