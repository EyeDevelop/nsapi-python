import datetime

from bs4 import BeautifulSoup
from requests import Session

from modules.urls import urlmap, form_url, create_get_request


def _verify_date(date: str):
    if len(date) != 8:
        return False

    d = date[:2]
    m = date[2:4]
    y = date[4:8]

    d, m, y = map(int, [d, m, y])
    try:
        datetime.datetime(y, m, d)

        return True
    except ValueError:
        return False


def get_pricing_f(s: Session, from_station: str, to_station: str, via_station: str = None, date: str = None):
    options = {
        "from": from_station,
        "to": to_station
    }
    if via_station:
        options["via"]: via_station
    if date:
        if _verify_date(date):
            options["dateTime"] = date

    r = s.get(form_url(urlmap["pricing"], create_get_request(options)))
    b = BeautifulSoup(r.text, 'xml')

    prices = {}
    for price_o in b.find_all("VervoerderKeuze"):
        price = {
            "carrier": price_o["naam"],
            "price_units": price_o.find("Tariefeenheden").text,
            "return": {
                "first-class": {
                    "full": float(price_o.find("ReisType", {"name": "Retour"}).find("ReisKlasse", {"klasse": "1"}).find("Kortingsprijs", {"name": "vol tarief"})["prijs"]),
                    "20-off": float(price_o.find("ReisType", {"name": "Retour"}).find("ReisKlasse", {"klasse": "1"}).find("Kortingsprijs", {"name": "20% korting"})["prijs"]),
                    "40-off": float(price_o.find("ReisType", {"name": "Retour"}).find("ReisKlasse", {"klasse": "1"}).find("Kortingsprijs", {"name": "40% korting"})["prijs"])
                },
                "standard-class": {
                    "full": float(price_o.find("ReisType", {"name": "Retour"}).find("ReisKlasse", {"klasse": "2"}).find("Kortingsprijs", {"name": "vol tarief"})["prijs"]),
                    "20-off": float(price_o.find("ReisType", {"name": "Retour"}).find("ReisKlasse", {"klasse": "2"}).find("Kortingsprijs", {"name": "20% korting"})["prijs"]),
                    "40-off": float(price_o.find("ReisType", {"name": "Retour"}).find("ReisKlasse", {"klasse": "2"}).find("Kortingsprijs", {"name": "40% korting"})["prijs"])
                },
            },
            "one-way": {
                "first-class": {
                    "full": float(price_o.find("ReisType", {"name": "Enkele reis"}).find("ReisKlasse", {"klasse": "1"}).find("Kortingsprijs", {"name": "vol tarief"})["prijs"]),
                    "20-off": float(price_o.find("ReisType", {"name": "Enkele reis"}).find("ReisKlasse", {"klasse": "1"}).find("Kortingsprijs", {"name": "20% korting"})["prijs"]),
                    "40-off": float(price_o.find("ReisType", {"name": "Enkele reis"}).find("ReisKlasse", {"klasse": "1"}).find("Kortingsprijs", {"name": "40% korting"})["prijs"])
                },
                "standard-class": {
                    "full": float(price_o.find("ReisType", {"name": "Enkele reis"}).find("ReisKlasse", {"klasse": "2"}).find("Kortingsprijs", {"name": "vol tarief"})["prijs"]),
                    "20-off": float(price_o.find("ReisType", {"name": "Enkele reis"}).find("ReisKlasse", {"klasse": "2"}).find("Kortingsprijs", {"name": "20% korting"})["prijs"]),
                    "40-off": float(price_o.find("ReisType", {"name": "Enkele reis"}).find("ReisKlasse", {"klasse": "2"}).find("Kortingsprijs", {"name": "40% korting"})["prijs"])
                }
            }
        }

        prices[price["carrier"]] = price

    return prices
