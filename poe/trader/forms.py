from django import forms


class ParamsItem(forms.Form):
    """Форма для ввода данных подборки итемов"""

    min_differenc_value = forms.DecimalField(
        label="Минимальное значение разницы",
        initial=1,
    )
    min_amount = forms.IntegerField()
    date_min = forms.DateField(
        label="Стартовая дата",
        help_text="Стартовая дата",
    )
    date_max = forms.DateField(
        label="Конечная дата",
        help_text="Конечная дата",
    )

