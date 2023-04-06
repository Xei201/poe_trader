import logging
from os import path
from pprint import pprint
from urllib.parse import urlencode

import requests
from django.db import transaction

from poe import settings
from .models import Category, Item

logger = logging.getLogger(__name__)


@transaction.atomic
def pars_type():
    categorys = Category.objects.filter(name__in=["UniqueJewels", "UniqueAccessorys"])
    for category in categorys:
        params = {"league": settings.LEAGUE,
                  "type": category.name[:-1],
                  "language": "en"}
        url = path.join(settings.POE_API, settings.LIST_ITEM) + "?" + urlencode(params)
        r = requests.get(url)
        print(url)
        if r.status_code == 200:
            try:
                list_item = []
                items = r.json()
                for item in items["lines"]:
                    list_item.append(Item(
                        name=item["name"],
                        item_id=item["id"],
                        details_id=item["detailsId"],
                        type=category
                    ))
                Item.objects.bulk_create(list_item)

            except Exception as e:
                logger.warning(f"Всё упало при выгрузке {category.name} по причине {str(e)}")
        else:
            logger.info(f"Реквест к {category.name} вернул {r.status_code}")

