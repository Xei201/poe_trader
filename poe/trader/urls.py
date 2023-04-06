from django.urls import path

from . import views

urlpatterns = [
    path('', views.ParsCategory.as_view(), name="list-payment"),
]