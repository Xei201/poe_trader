import logging
from datetime import datetime, timedelta
from decimal import Decimal
from os import path
from pprint import pprint
from urllib.parse import urlencode

import requests
from django.db import transaction
from django.db.models import Min, Max, Count

from poe import settings
from .models import Category, Item, DataPoint

logger = logging.getLogger(__name__)


# 4 функции ниже отвечают за парсинг, в них при тестировании используй @transaction.atomic
# как антипатерн, чтобы не заполнять БД лишними данными
def pars_type_normal():
    """Используется для парсинга итемов всех категорий кроме Currency"""
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


def pars_type_currency():
    """Парсит итемы Currency"""
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
    """Парсит все графы итемов всех категорий кроме Currency"""
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


def pars_data_currency():
    """Парсит все графы для итемов Currency"""
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


class FindTrend():
    """Производит выгрузку списка итемов по условиям поиса тенденции"""

    def __init__(self, request):
        self.date_min, self.date_max, self.value, self.amount, self.sorted_param = self.get_params(request)

    @classmethod
    def get_params(cls, request):
        date_min = request.GET.get("date_min", "")
        date_max = request.GET.get("date_max", "")
        value = Decimal(request.GET.get("value", ""))
        amount = int(request.GET.get("amount", ""))
        sorted_param = request.GET.get("sorted_param", "")

        return date_min, date_max, value, amount, sorted_param

    def get_item(self):
        list_item = []
        # Выборка всех ID item, подходящий по времени и числу единиц в продаже,
        # а также имеющих тендунцию больше или равную запрашиваемой

        list_item_id = DataPoint.objects.filter(
            data_date__in=[self.date_min, self.date_max],
            amount__gt=self.amount,
        ).values_list("item", flat=True).alias(
            cnt=Count('id'),
            dif_price=Max('value') - Min('value'),
        ).filter(cnt__gte=2, dif_price__gte=abs(self.value))

        # Загрузка Item по этим ID
        diff_data_point = DataPoint.objects.select_related("item").filter(
            item_id__in=list_item_id,
            data_date__in=[self.date_min, self.date_max],
        ).order_by("data_date", "item_id")

        # Поиск Item с возрастающей тенденцией и формирование из них списка кортежей
        # для загрузки на фронт
        gap_value = len(diff_data_point) // 2
        for index in range(gap_value):
            if diff_data_point[index].value < diff_data_point[index + gap_value].value and self.value > 0:
                list_item.append((
                    diff_data_point[index],
                    diff_data_point[index + gap_value],
                    diff_data_point[index + gap_value].value - diff_data_point[index].value,
                ))

        if self.sorted_param:
            list_item = self.sort_result(list_item)

        return list_item

    def sort_result(self, list_item):

        if self.sorted_param == "amount_start":
            return sorted(list_item, key=lambda x: x[0].amount)

        if self.sorted_param == "amount_end":
            return sorted(list_item, key=lambda x: x[1].amount)

        if self.sorted_param == "delta_prise":
            return sorted(list_item, key=lambda x: x[2])
