
from django.contrib import admin
from django.urls import path
from . import views
from .webapi import trade_list_api
urlpatterns = [
    path('', views.strategy),
    path('position_order/', trade_list_api.trade_position_list),
    path('position_order/upload/', views.position_upload)
]
