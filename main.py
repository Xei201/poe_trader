from pprint import pprint

import requests


def test(url):
    r = requests.get(url)
    return r.json()


if __name__ == '__main__':
    url = "https://poe.ninja/api/data/itemoverview?league=Sanctum&type=DivinationCard&language=en"
    result = test(url)
    pprint(result["lines"][0]["artFilename"])

