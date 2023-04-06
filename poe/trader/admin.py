from django_admin_inline_paginator.admin import TabularInlinePaginated


from django.contrib import admin

from .models import Item, DataPoint, Category


class ItemInline(TabularInlinePaginated):
    model = Item
    per_page = 50


class DataPointInLine(TabularInlinePaginated):
    model = DataPoint
    per_page = 50


@admin.register(Category)
class TypeAdmin(admin.ModelAdmin):
    list_display = ("name", )
    list_filter = ("name", )
    inlines = [ItemInline]
    search_fields = ("name", )


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "item_id", "date_update", "details_id", "type")
    list_filter = ("name", "item_id", "date_update")
    list_per_page = 50
    inlines = [DataPointInLine]
    search_fields = ("item_id", )


@admin.register(DataPoint)
class PriceAdmin(admin.ModelAdmin):
    list_display = ("value", "data_date", "item", "amount")
    list_filter = ("value", "data_date")
    list_per_page = 50

