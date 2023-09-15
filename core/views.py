from django.http import HttpResponse
from django.shortcuts import render
from core.pubAPIs import getCandle, getAllAssests, getAllPeriods
import pandas as pd
from core.models import Exchanges, TimePeriods, Assets
from django.db import transaction
from core.helpers import transform_time
from django.http import JsonResponse


def candleInfo(request):
    if request.method == 'POST':
        periods = request.POST['timeFrame']
        currency1 = request.POST['currency1']
        currency2 = request.POST['currency2']
        dateTime1 = transform_time(request.POST['dateTime1'])
        dateTime2 = transform_time(request.POST['dateTime2'])

        data = getCandle(currency1, currency2, dateTime1, dateTime2, periods)
        return JsonResponse(data, safe=False)
        
    elif request.method == 'GET':
        data = getCandle()

        return JsonResponse(data, safe=False)


def candlePage(request):
    allAssets = Assets.objects.all()
    allPlatforms = Exchanges.objects.all()
    allPeriods = TimePeriods.objects.all()

    context = {
        'assets': allAssets,
        'platforms': allPlatforms,
        'periods': allPeriods,
    }
    print(len(allAssets))
    return render(request, 'candles.html', context)


@transaction.atomic
def setDbValues(request):
    assetsList = getAllAssests()
    periodsList = getAllPeriods()

    Assets.objects.all().delete()
    TimePeriods.objects.all().delete()

    for dict in assetsList:
        Assets.objects.create(
            asset_name = dict['asset_name'],
            asset_id = dict['asset_id'],
            is_crypto = dict['is_crypto']
            )
        
    for dict in periodsList:
        TimePeriods.objects.create(
            period_name = dict['period_name'],
            period_id = dict['period_id']
        )

    return HttpResponse('operation successfull')