from bs4 import BeautifulSoup
from requests import Session

from modules.urls import urlmap


def get_stations_f(s: Session):
    r = s.get(urlmap["stations"])
    b = BeautifulSoup(r.text, 'xml')

    stations = {}
    for station_o in b.find("Stations").find_all("Station"):
        station = {
            "code": station_o.find("Code").text,
            "type": station_o.find("Type").text,
            "name": {
                "short": station_o.find("Namen").find("Kort").text,
                "middle": station_o.find("Namen").find("Middel").text,
                "full": station_o.find("Namen").find("Lang").text,
            },
            "country": station_o.find("Land").text,
            "uic": station_o.find("UICCode").text,
            "lat": station_o.find("Lat").text,
            "lon": station_o.find("Lon").text,
            "synonyms": []
        }

        for synonym_o in station_o.find_all("Synoniem"):
            station["synonyms"].append(synonym_o.text)

        stations[station["code"]] = station

    return stations
