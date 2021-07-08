from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.

def strategy(request):
    if request.method == "GET":
        strategy_list = StrategyInfo.objects.all().values()
        print(strategy_list)
        return render(request,'strategy/strategy.html',{"strategy_list":strategy_list})
    else:

        return HttpResponse('POST')


def position(request):
    if request.method == "GET":
        strategy_id = request.GET.get('id')
        date = request.GET.get('date')
        strategy_list = StrategyInfo.objects.all().values()
        return render(request,'strategy/strategy.html',{"strategy_list":strategy_list})
    else:
        return HttpResponse('POST')


def position_upload(request):
    if request.method == "GET":
        strategy_list = StrategyInfo.objects.all().values()
        return render(request, 'strategy/position_upload.html', {"strategy_list": strategy_list})
    else:
        strategy_id = request.POST.get('strategy_id')
        file = request.FILES.get('upload_file',None)
        # with open(r'C:\Users\Administrator.DESKTOP-E3H20V7\Desktop\test.txt', 'wb+') as destination:
        #     for chunk in file.chunks():
        #         destination.write(chunk)

        return HttpResponse(strategy_id)
