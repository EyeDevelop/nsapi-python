import datetime

from bs4 import BeautifulSoup
from requests import Session

from modules.urls import urlmap, create_get_request, form_url


def _convert_to_datetime(iso8601_datestr: str):
    date, time = iso8601_datestr.split("T")
    time, timezone = time.split("+")
    tzd, tzh, tzm, tzs = map(int, list(timezone))

    dy, dm, dd = map(int, date.split("-"))
    th, tm, ts = map(int, time.split(":"))
    return datetime.datetime(dy, dm, dd, th, tm, ts, tzinfo=datetime.timezone(datetime.timedelta(days=tzd, hours=tzh, minutes=tzm, seconds=tzs)))


def get_travel_recommendations_f(s: Session, from_station: str, to_station: str, via_station: str = None, previous_advices: int = None, next_advices: int = None, departure_time: datetime.datetime = None, arrival_time: datetime.datetime = None, highspeed_allowed: bool = None, has_year_card: bool = None):
    options = {
        "fromStation": from_station,
        "toStation": to_station
    }
    if via_station is not None:
        options["viaStation"] = via_station
    if previous_advices is not None:
        options["previousAdvices"] = previous_advices
    if next_advices is not None:
        options["nextAdvices"] = next_advices
    if departure_time is not None:
        options["Departure"] = "true"
        options["dateTime"] = departure_time.strftime("{}-{}-{}T{}:{}".format(
            departure_time.year,
            departure_time.month,
            departure_time.day,
            departure_time.hour,
            departure_time.minute
        ))
    elif arrival_time is not None:
        options["Departure"] = "false"
        options["dateTime"] = arrival_time.strftime("{}-{}-{}T{}:{}".format(
            departure_time.year,
            departure_time.month,
            departure_time.day,
            departure_time.hour,
            departure_time.minute
        ))
    if highspeed_allowed is not None:
        options["hslAllowed"] = str(highspeed_allowed).lower()
    if has_year_card is not None:
        options["yearCard"] = str(has_year_card).lower()

    r = s.get(form_url(urlmap["travel-recommendations"], create_get_request(options)))
    b = BeautifulSoup(r.text, 'xml')

    possibilities = []
    for possibility_o in b.find_all("ReisMogelijkheid"):
        possibility = {
            "transfers": possibility_o.find("AantalOverstappen").text,
            "optimal": possibility_o.find("Optimaal").text,
            "status": possibility_o.find("Status").text,
            "travel_time": {
                "planned": possibility_o.find("GeplandeReisTijd").text,
                "actual": possibility_o.find("ActueleReisTijd").text,
            },
            "departure_time": {
                "planned": _convert_to_datetime(possibility_o.find("GeplandeVertrekTijd").text),
                "actual": _convert_to_datetime(possibility_o.find("ActueleVertrekTijd").text),
            },
            "arrival_time": {
                "planned": _convert_to_datetime(possibility_o.find("GeplandeAankomstTijd").text),
                "actual": _convert_to_datetime(possibility_o.find("ActueleAankomstTijd").text),
            },
            "travel_info": {
                "type": possibility_o.find("ReisDeel")["reisSoort"],
                "carrier": possibility_o.find("ReisDeel").find("Vervoerder").text,
                "commute_type": possibility_o.find("ReisDeel").find("VervoerType").text,
                "ride_id": possibility_o.find("ReisDeel").find("RitNummer").text,
                "state": possibility_o.find("ReisDeel").find("Status").text,
                "details": [],
                "stops": []
            }
        }

        details = []
        for detail_o in possibility_o.find_all("Reisdetail"):
            details.append(detail_o.text)

        stops = []
        for stop_o in possibility_o.find_all("ReisStop"):
            stop = {
                "name": stop_o.find("Naam").text,
                "arrival_time": _convert_to_datetime(stop_o.find("Tijd").text)
            }

            stops.append(stop)

        possibility["travel_info"]["details"] = details
        possibility["travel_info"]["stops"] = stops

        possibilities.append(possibility)

    return possibilities
