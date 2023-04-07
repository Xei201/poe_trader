import datetime

from django import forms
from django.db.models import Max
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .models import DataPoint


class ParamsItem(forms.Form):
    """Форма для ввода данных подборки итемов"""

    min_differenc_value = forms.DecimalField(
        label="Минимальное значение разницы",
        initial=1,
    )
    min_amount = forms.IntegerField(
        label="Минимальное число товара на рынке",
        initial=1,
    )
    date_min = forms.DateField(
        label="Стартовая дата",
        help_text="Стартовая дата",
    )
    date_max = forms.DateField(
        label="Конечная дата",
        help_text="Конечная дата",
    )

    # def clean_date_min(self):
    #     date_min = self.cleaned_data["date_min"]
    #
    #     if date_min > datetime.date.today():
    #         raise ValidationError(_("Дата не может быть из будущего"))
    #
    #     return date_min

    def clean_date_max(self):
        date_min = self.cleaned_data["date_min"]
        date_max = self.cleaned_data["date_max"]
        control_date = DataPoint.objects.aggregate(max_date=Max("data_date"))

        if date_min > date_max:
            raise ValidationError(_("Конечная дата должна быть позже начальной"))

        if date_max > datetime.date.today():
            raise ValidationError(_("Дата не может быть из будущего"))

        if date_max > control_date["max_date"]:
            raise ValidationError(_("Дата не может быть больше крайней даты из БД"))

        return date_max

    def clean_min_differenc_value(self):
        diff_value = self.cleaned_data["min_differenc_value"]

        if diff_value == 0:
            raise ValidationError(_("Разница цен не может быть нулевой"))

        return diff_value

    def clean_min_amount(self):
        amount = self.cleaned_data["min_amount"]

        if amount < 0:
            raise ValidationError(_("Количество товара не может быть меньше 0"))

        return amount