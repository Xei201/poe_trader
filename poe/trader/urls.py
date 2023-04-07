from django.urls import path

from . import views

urlpatterns = [
    path('', views.ParsCategory.as_view(), name="list-payment"),
    path('form', views.FindMaxTrend.as_view(), name="form-item"),
    path('form/list', views.ListItem.as_view(), name="list-find-item"),
]
