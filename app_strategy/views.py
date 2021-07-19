from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.

def strategy(request):
    if request.method == "GET":
        strategy_list = StrategyInfo.objects.all().values()
        return render(request,'strategy/strategy.html',{"strategy_list":strategy_list})
    else:
        strategy_name = request.POST.get("strategy_name")
        print(strategy_name)
        return HttpResponse('POST')


def position(request):
    if request.method == "GET":
        strategy_id = request.GET.get('id')
        date = request.GET.get('date')
        strategy_list = StrategyInfo.objects.all().values()
        return render(request,'strategy/strategy.html',{"strategy_list":strategy_list})
    else:
        return HttpResponse('POST')




def strategy_trade_option(request):
    if request.method == "GET":
        strategy_id = request.GET.get('strategy_id')
        #strategy_name = request.GET.get('strategy_name')
        strategy = StrategyInfo.objects.get(id=strategy_id)
        strategy_name = strategy.name
        return render(request, 'strategy/strategy_trade_option.html', {"strategy_id": strategy_id,"strategy_name":strategy_name})
