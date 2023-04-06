from django.shortcuts import render
from django.views import generic

from .core import pars_data_pont, pars_data_currency, pars_type_currency
from .models import Category


class ParsCategory(generic.ListView):
    template_name = 'pars/success_pars.html'
    paginate_by = 10
    model = Category
    context_object_name = "datas"

    def get(self, request, *args, **kwargs):
        pars_data_currency()


class FindMaxTrend(generic.FormView):
    pass

