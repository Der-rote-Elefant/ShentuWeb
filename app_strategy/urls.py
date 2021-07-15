
from django.contrib import admin
from django.urls import path
from . import views
from .webapi import trade_list_api
urlpatterns = [
    path('', views.strategy),
    path('trade_page/',views.strategy_trade_option),
    path('position_order/', trade_list_api.trade_position_list),
]
