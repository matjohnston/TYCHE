from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from requests.models import Response

import pandas as pd
import os
import numpy as np

from datetime import date

with open('reports.json') as f:
  reports = json.load(f)

def main():
    captureMarketCapData();


def captureMarketCapData():
    for coinApi in reports:
        reportPath = init(coinApi['name'])
        for attribute, value in coinApi['parameters'].items():
            fetchMarketCap(attribute, reportPath, coinApi)

def init(report):
    d1 = (date.today()).strftime("%m-%d-%Y")

    current_directory = os.getcwd()

    base_directory = os.path.join(current_directory, 'reports')
    if not os.path.exists(base_directory):
        os.makedirs(base_directory)

    report_directory = os.path.join(base_directory, report)
    if not os.path.exists(report_directory):
        os.makedirs(report_directory)


    date_directory = os.path.join(report_directory, d1)
    if not os.path.exists(date_directory):
        os.makedirs(date_directory)

    return os.path.join(base_directory, report, d1)

def fetchMarketCap(capType, reportPath, coinApi):
    params = coinApi['parameters'][capType]
    urlHeaders = coinApi['headers']
    url = coinApi['url']
    data = fetchGetResponseFromApi(params, urlHeaders, url)
    if data['status']['error_code'] == 0:
        postProcessData(data, coinApi['name'], capType, coinApi)
        filePath = os.path.join(reportPath, capType + '.csv')
        saveCsv(data['data'], filePath)
    else:
        raise ConnectionError('Unable to process request. Exiting')

def postProcessData(data, name, capType, coinApi):
    if name == 'coinMarketCap':
        print(capType, 'from',name, len(data['data']), 'results found')
        keepCoins = []
        for index, coin in enumerate(data['data']):
            result = fetchGetResponseFromApi({},{},'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/market-pairs/latest?id=' + str(coin['id']))
            data['data'][index]['marketPairs'] = result['data']['marketPairs']
            #filterstep
            keepCoin = False
            for marketPairs in result['data']['marketPairs']:
                for acceptableExchange in coinApi['approvedExchanges']:
                    if marketPairs['exchangeName'] == acceptableExchange:
                        keepCoin = True
                        break
            if keepCoin == True:
                keepCoins.append(coin)
        data['data'] = keepCoins
        print(capType, 'from',name, len(data['data']), 'results found post filter')

def saveCsv(data, fileName):
    try:
        df = pd.json_normalize(data)
        df.to_csv(fileName)
        print(fileName, 'saved')
    except (PermissionError) as e:
        print('Unable to save', fileName, 'Excel document might be open. Please close and run again')

def fetchGetResponseFromApi(parameters, headers, url):
    session = Session()
    session.headers.update(headers)

    try:
        data = {
                'status':{
                    'error_code':'500'
                }
            }
        retryCount = 0
        while str(data['status']['error_code']) != '0':
            result = session.get(url, params=parameters)
            data = json.loads(result.text)
            if str(data['status']['error_code']) != '0':
                retryCount = retryCount + 1
                print('error_message: ',data['status']['error_message'],'error_code: ',data['status']['error_code'], 'Retry count: ', retryCount)

            if retryCount > 10: 
                break

        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

def fetchCoinMarketCapDetailsForCoin(id):
    print('notImplementedYet')

main()