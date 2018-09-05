import datetime

from bs4 import BeautifulSoup
from requests import Session

from modules.urls import urlmap, form_url, create_get_request


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
            "id": disruption_o.find("id").text,
            "trajectory": disruption_o.find("Traject").text,
            "period": disruption_o.find("Periode").text,
            "reason": disruption_o.find("Reden").text,
            "advice": disruption_o.find("Advies").text,
            "message": disruption_o.find("Bericht").text
        }

        expected[disruption["id"]] = disruption

    unexpected = {}
    for disruption_o in b.find("Storingen").find("Ongepland").find_all("Storing"):
        disruption = {
            "id": disruption_o.find("id").text,
            "trajectory": disruption_o.find("Traject").text,
            "reason": disruption_o.find("Reden").text,
            "message": disruption_o.find("Bericht").text,
            "date": disruption_o.find("Datum").text
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
