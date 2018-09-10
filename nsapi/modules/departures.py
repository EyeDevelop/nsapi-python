import datetime

from bs4 import BeautifulSoup
from requests import Session

from nsapi.modules.urls import create_get_request, form_url, urlmap


def _get_text_if_exists(tag):
    if tag is not None:
        return tag.text


def get_departures_f(s: Session, station: str):
    r = s.get(form_url(urlmap["departures"], create_get_request({"station": station})))
    b = BeautifulSoup(r.content.decode("utf-8", "ignore"), "xml")

    trains = {}

    for train_o in b.find("ActueleVertrekTijden").find_all("VertrekkendeTrein"):
        train = {
            "journey": train_o.find("RitNummer").text,
            "departure_time": train_o.find("VertrekTijd").text,
            "destination": train_o.find("EindBestemming").text,
            "train_type": train_o.find("TreinSoort").text,
            "carrier": train_o.find("Vervoerder").text,
            "route": _get_text_if_exists(train_o.find("RouteTekst")),
            "tip": _get_text_if_exists(train_o.find("ReisTip")),
            "departs_from": {
                "platform": train_o.find("VertrekSpoor").text,
                "changed": train_o.find("VertrekSpoor")["wijziging"] == "true"
            },
            "delay": {
                "time": _get_text_if_exists(train_o.find("VertrekVertraging")),
                "reason": _get_text_if_exists(train_o.find("VertrekVertragingsTekst"))
            }
        }

        train["comments"] = []
        for comment_o in train_o.find_all("Comment"):
            train["comments"].append(comment_o.text)

        date, time = train["departure_time"].split("T")
        time, timezone = time.split("+")
        tzd, tzh, tzm, tzs = map(int, list(timezone))

        dy, dm, dd = map(int, date.split("-"))
        th, tm, ts = map(int, time.split(":"))
        train["departure_time"] = datetime.datetime(dy, dm, dd, th, tm, ts, tzinfo=datetime.timezone(datetime.timedelta(days=tzd, hours=tzh, minutes=tzm, seconds=tzs)))

        trains[train["journey"]] = train

    return trains
