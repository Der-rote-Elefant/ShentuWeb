from django.http import HttpResponse
from django.shortcuts import render

def trade_position_list(request):
    if request.method == "GET":

        return HttpResponse("get trade list")
    else:

        return HttpResponse("put trade list")
