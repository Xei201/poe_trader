import logging
from datetime import datetime, timedelta
from os import path
from pprint import pprint
from urllib.parse import urlencode

import requests
from django.db import transaction

from poe import settings
from .models import Category, Item, DataPoint

logger = logging.getLogger(__name__)


@transaction.atomic
def pars_type_normal():
    categorys = Category.objects.exclude(name__in=["Currencys", "Fragments"])
    for category in categorys:
        params = {"league": settings.LEAGUE,
                  "type": category.name[:-1],
                  "language": "en"}
        url = path.join(settings.POE_API, settings.ITEM_LIST) + "?" + urlencode(params)
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


@transaction.atomic
def pars_type_currency():
    categorys = Category.objects.filter(name__in=["Currencys", "Fragments"])
    for category in categorys:
        params = {"league": settings.LEAGUE,
                  "type": category.name[:-1],
                  "language": "en"}
        url = path.join(settings.POE_API, settings.CURRENCY_LIST) + "?" + urlencode(params)
        r = requests.get(url)
        print(url)
        if r.status_code == 200:
            try:
                list_item = []
                items = r.json()
                for item in items["lines"]:
                    list_item.append(Item(
                        name=item["currencyTypeName"],
                        item_id=item["receive"]["get_currency_id"],
                        details_id=item["detailsId"],
                        type=category
                    ))
                Item.objects.bulk_create(list_item)

            except Exception as e:
                logger.warning(f"Всё упало при выгрузке {category.name} по причине {str(e)}")
        else:
            logger.info(f"Реквест к {category.name} вернул {r.status_code}")


def pars_data_pont():
    categorys = Category.objects.exclude(name__in=["Currencys", "Fragments"])
    amount_categorys = categorys.count()

    for count_category, category in enumerate(categorys):
        items = category.item_set.all()
        amount_items = items.count()
        for count_item, item in enumerate(items):
            params = {"league": settings.LEAGUE,
                      "type": category.name[:-1],
                      "itemId": item.item_id}
            url = path.join(settings.POE_API, settings.ITEM_PRISE) + "?" + urlencode(params)
            r = requests.get(url)
            print(f"Upload category {count_category}/{amount_categorys} for item {count_item}/{amount_items}")
            if r.status_code == 200:
                try:
                    list_point = []
                    points = r.json()
                    for point in points:
                        list_point.append(DataPoint(
                            value=point["value"],
                            data_date=datetime.today().date() - timedelta(point["daysAgo"]),
                            amount=point["count"],
                            item=item
                        ))
                    DataPoint.objects.bulk_create(list_point)

                except Exception as e:
                    logger.warning(f"Всё упало при выгрузке {item.name} по причине {str(e)}")
            else:
                logger.info(f"Реквест к {item.name} вернул {r.status_code}")


@transaction.atomic
def pars_data_currency():
    categorys = Category.objects.filter(name__in=["Currencys", "Fragments"])
    amount_categorys = categorys.count()

    for count_category, category in enumerate(categorys):
        items = category.item_set.all()
        amount_items = items.count()
        for count_item, item in enumerate(items):
            params = {"league": settings.LEAGUE,
                      "type": category.name[:-1],
                      "currencyId": item.item_id}
            url = path.join(settings.POE_API, settings.CURRENCY_PRICE) + "?" + urlencode(params)
            r = requests.get(url)
            print(f"Upload category {count_category}/{amount_categorys} for item {count_item}/{amount_items}")
            if r.status_code == 200:
                try:
                    list_point = []
                    points = r.json()
                    point_position = "receiveCurrencyGraphData"
                    for point in points[point_position]:
                        list_point.append(DataPoint(
                            value=point["value"],
                            data_date=datetime.today().date() - timedelta(point["daysAgo"]),
                            amount=point["count"],
                            item=item
                        ))
                    DataPoint.objects.bulk_create(list_point)

                except Exception as e:
                    logger.warning(f"Всё упало при выгрузке {item.name} по причине {str(e)}")
            else:
                logger.info(f"Реквест к {item.name} вернул {r.status_code}")