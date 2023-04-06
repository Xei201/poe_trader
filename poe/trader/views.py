from django.shortcuts import render
from django.views import generic

from .models import Category
from .core import pars_type


class ParsCategory(generic.ListView):
    template_name = 'pars/success_pars.html'
    paginate_by = 10
    model = Category
    context_object_name = "datas"

    def get(self, request, *args, **kwargs):
        pars_type()


