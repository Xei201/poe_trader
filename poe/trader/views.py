from urllib.parse import urlencode
import datetime

from django.db.models import Max
from django.urls import reverse
from django.views import generic

from .forms import ParamsItem
from .core import pars_data_pont, pars_data_currency, pars_type_currency, FindTrend
from .models import Category, DataPoint


class ParsCategory(generic.ListView):
    template_name = 'pars/success_pars.html'
    paginate_by = 10
    model = Category
    context_object_name = "datas"

    def get(self, request, *args, **kwargs):
        pass


class FindMaxTrend(generic.FormView):
    """Форма указания параметров поиска итемов"""

    template_name = 'item/get_item.html'
    form_class = ParamsItem
    permission_required = ("API.can_request",)

    def form_valid(self, form):
        self.form = form
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        control_date = DataPoint.objects.aggregate(max_date=Max("data_date"))
        initial["date_min"] = control_date["max_date"] - datetime.timedelta(days=2)
        initial["date_max"] = control_date["max_date"]
        return initial

    def get_success_url(self):
        params = {
            "value": self.form.cleaned_data["min_differenc_value"],
            "amount": self.form.cleaned_data["min_amount"],
            "date_min": self.form.cleaned_data["date_min"],
            "date_max": self.form.cleaned_data["date_max"],
        }
        return reverse("list-find-item") + '?' + urlencode(params)


class ListItem(generic.TemplateView):
    """Список итемов по параметрам"""

    template_name = 'item/list_item.html'
    paginate_by = 20
    # context_object_name = "items"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        find_item = FindTrend(self.request)
        context_data = find_item.get_item()
        context['items'] = context_data

        params_search = (FindTrend.get_params(self.request))
        context['params_search'] = params_search

        return context


