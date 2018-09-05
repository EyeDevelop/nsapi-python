def create_get_request(options: dict):
    """
    Creates a GET request url from an options dictionary.

    :param options: A dictionary of GET options.
    :return: The url
    :rtype: str
    """

    url = "?"
    to_add = []

    for key, value in options.items():
        to_add.append([str(key), str(value)])

    url += "&".join(["=".join(x) for x in to_add])
    return url


def form_url(*args, separate_char: str = ""):
    return separate_char.join(args)


__base_url = "https://webservices.ns.nl/ns-api"
urlmap = {
    "generic": __base_url,
    "departures": f"{__base_url}-avt",
    "stations": f"{__base_url}-stations-v2"
}
