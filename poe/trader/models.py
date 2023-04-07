import re
from os import path

from django.db import models

from poe import settings


class Category(models.Model):
    name = models.CharField(
        primary_key=True,
        max_length=255,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(
        verbose_name="Человеческое имя",
        max_length=255,
    )
    item_id = models.IntegerField()
    date_update = models.DateField(auto_now=True)
    details_id = models.CharField(
        verbose_name="Имя для API",
        max_length=255,
    )
    type = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        return path.join(settings.POE_ITEM_URL, re.sub(r'([a-z])([A-Z])', r'\1-\2', str(self.type)), self.details_id)

    def __str__(self):
        return self.name


class DataPoint(models.Model):
    value = models.DecimalField(
        max_digits=12,
        decimal_places=4,
    )
    data_date = models.DateField()
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField()

    class Meta:
        ordering = ["item", "data_date", "amount"]

    def __str__(self):
        return str(self.id)
