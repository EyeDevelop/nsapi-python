from requests import Session

from modules.urls import urlmap


def verify_login(s: Session):
    r = s.get(urlmap["departures"])

    if r.status_code == 200:
        return True
    else:
        return False
