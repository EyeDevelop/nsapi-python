import datetime

from bs4 import BeautifulSoup
from requests import Session

from nsapi.modules.urls import urlmap, form_url, create_get_request


def _get_text_if_exists(tag):
    if tag is not None:
        return tag.text


def get_disruptions_f(s: Session, actual: bool, station: str = None, unplanned: bool = None):
    options = {
        "actual": str(actual).lower(),
    }
    if station is not None:
        options["station"] = station
    if unplanned is not None:
        options["unplanned"] = str(unplanned).lower()

    r = s.get(form_url(urlmap["disruptions"], create_get_request(options)))
    b = BeautifulSoup(r.text, 'xml')

    expected = {}
    for disruption_o in b.find("Storingen").find("Gepland").find_all("Storing"):
        disruption = {
            "id": _get_text_if_exists(disruption_o.find("id")),
            "trajectory": _get_text_if_exists(disruption_o.find("Traject")),
            "period": _get_text_if_exists(disruption_o.find("Periode")),
            "reason": _get_text_if_exists(disruption_o.find("Reden")),
            "advice": _get_text_if_exists(disruption_o.find("Advies")),
            "message": _get_text_if_exists(disruption_o.find("Bericht")),
            "date": _get_text_if_exists(disruption_o.find("Datum"))
        }

        expected[disruption["id"]] = disruption

    unexpected = {}
    for disruption_o in b.find("Storingen").find("Ongepland").find_all("Storing"):
        disruption = {
            "id": _get_text_if_exists(disruption_o.find("id")),
            "trajectory": _get_text_if_exists(disruption_o.find("Traject")),
            "period": _get_text_if_exists(disruption_o.find("Periode")),
            "reason": _get_text_if_exists(disruption_o.find("Reden")),
            "advice": _get_text_if_exists(disruption_o.find("Advies")),
            "message": _get_text_if_exists(disruption_o.find("Bericht")),
            "date": _get_text_if_exists(disruption_o.find("Datum"))
        }
        date, time = disruption["date"].split("T")
        time, timezone = time.split("+")
        tzd, tzh, tzm, tzs = map(int, list(timezone))

        dy, dm, dd = map(int, date.split("-"))
        th, tm, ts = map(int, time.split(":"))
        disruption["date"] = datetime.datetime(dy, dm, dd, th, tm, ts, tzinfo=datetime.timezone(datetime.timedelta(days=tzd, hours=tzh, minutes=tzm, seconds=tzs)))

        unexpected[disruption["id"]] = disruption

    disruptions = {
        "expected": expected,
        "unexpected": unexpected
    }

    return disruptions
