import re
from pprint import pprint
from datetime import datetime, timedelta

import requests


def test(url):
    r = requests.get(url)
    return r.json()


if __name__ == '__main__':
    # url = "https://poe.ninja/api/data/currencyoverview?league=Sanctum&type=Currency&language=en"
    # result = test(url)
    # pprint(result["lines"][0])

    line = "UniqueArmours"
    print(re.sub(r'([a-z][A-Z])', r'-\1', line))
