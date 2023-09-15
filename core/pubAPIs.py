import requests
from django.http import JsonResponse
from datetime import date
from datetime import timedelta
import time
import json
import os

BASE_URL = "https://rest.coinapi.io/v1/"
HEADERS = {"X-CoinAPI-Key": "024A3B66-3F53-4525-83A8-26F8B3EC835C"}


def configRequestURL(currency1, currency2, timePeriod, dateTime1, dateTime2):

    fstrURL = (
        f"""ohlcv/BINANCE_SPOT_{currency1}_{currency2}/history?period_id={timePeriod}{'&time_start=' if dateTime1 else ''}{dateTime1}{'&time_end=' if dateTime2 else ''}{dateTime2}"""
                )
    
    endpoint = BASE_URL+fstrURL
    print('\n=================',endpoint,'=================\n')
    return endpoint


def getCandle(currency1='ETH', currency2='BTC', dateTime1='2022-01-01T00:00:00', dateTime2='', timeFrame='10MIN'):

    endpoint = configRequestURL(currency1, currency2, timeFrame, dateTime1, dateTime2)
    print(HEADERS)
    response = requests.get(endpoint, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()        
        return data
    else:
        print(response.status_code, '\n', response)
        return response.status_code
    

def getAllPeriods():
    endpoint = BASE_URL+'ohlcv/periods'
    response = requests.get(endpoint, headers=HEADERS)

    periodList = []

    if response.status_code == 200:
        response_data = response.json()
        for item in response_data[:50]:
            periodId = item["period_id"]
            displayName = item["display_name"]
            periodsDict = {
                'period_name': displayName,
                'period_id': periodId,
            }
            periodList.append(periodsDict)
    else:
        print('response error', response, response.headers)
    

    

    return periodList


def getAllAssests():
    endpoint = BASE_URL+'assets'
    response = requests.get(endpoint, headers=HEADERS)

    assetsList = []

    if response.status_code == 200:
        response_data = response.json()
        for i in range(len(response_data[:30])):
            if response_data[i]['type_is_crypto']  == 1:

                assetName = (response_data[i]['name'])
                assetId = (response_data[i]['asset_id'])
                asset_is_crypto = (response_data[i]['type_is_crypto'])

                assetDict = {
                    'asset_name': assetName,
                    'asset_id': assetId,
                    'is_crypto': asset_is_crypto,
                }
                assetsList.append(assetDict)
            else:
                continue
    else:
        print('response error', response.headers)
       
    print(len(assetsList))
    return assetsList
