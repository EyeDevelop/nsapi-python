import requests
from requests.auth import HTTPBasicAuth

from modules.exceptions.login import IncorrectAuthException
from modules.login import verify_login
from modules.departures import get_departures_f


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

        A single object as k = v:
        train_id = {
            "journey":          str: The train ID,
            "departure_time":   datetime: The train's departure time,
            "destination":      str: The train's destination,
            "train_type":       str: The type of train,
            "carrier":          str: The company which handles the train,
            "departs_from": {
                "platform":     str: The platform from which it leaves,
                "changed":      bool: Whether the platform has changed or not.
            }
        }

        :param station: The station of which to get the departures.
        :return: A dictionary with train information.
        :rtype: dict
        """

        self._check_logged_in()

        return get_departures_f(self.r, station)
