from django.contrib import admin

from .models import Item, DataPoint, Category


class ItemInline(admin.TabularInline):
    model = Item


class DataPointInLine(admin.TabularInline):
    model = DataPoint


@admin.register(Category)
class TypeAdmin(admin.ModelAdmin):
    list_display = ("name", )
    list_filter = ("name", )
    inlines = [ItemInline]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "item_id", "date_update", "details_id", "type")
    list_filter = ("name", "item_id", "date_update")
    list_per_page = 50
    inlines = [DataPointInLine]


@admin.register(DataPoint)
class PriceAdmin(admin.ModelAdmin):
    list_display = ("values", "data_date", "item", "amount")
    list_filter = ("values", "data_date")
