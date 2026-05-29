import requests

def TickerSearch(name: str):
    """
    Takes an entity or firm name as input and returns possible matching
    organizations with their ticker symbols.
    """

    r = requests.get(
        "https://query1.finance.yahoo.com/v1/finance/search",
        params={"q": name, "quotesCount": 10, "newsCount": 0},
        headers={"User-Agent": "Mozilla/5.0"}
    ).json()

    return [
        {
            "name": x.get("shortname"),
            "ticker": x.get("symbol")
        }
        for x in r.get("quotes", [])
        if x.get("symbol")
    ]=