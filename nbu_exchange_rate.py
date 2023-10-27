from datetime import date, datetime
import requests
import json

def get_from_api(update_from, update_to):
    #formating date types into strings in format "yyyymmdd" for API url
    update_from = update_from.strftime('%Y%m%d')
    update_to = update_to.strftime('%Y%m%d')
    payload = {
        'start': update_from, 
        'end': update_to, 
        'valcode': 'usd', 
        'sort' :'exchangedate', 
        'order':'desc',
        'json': ''
    }
    response = requests.get('https://bank.gov.ua/NBU_Exchange/exchange_site', params=payload)
    response_json = response.json()

    response_array = []
    # fill in headers from key dictionaries NBU API we want
    headers = ['exchangedate', 'cc', 'rate_per_unit']
    response_array.append(headers)
    #look through each object (day) of json file:
    for day in response_json:
        #create empty list for nedeed values of each day:
        list_values_day = []
        #add value only if key is in the headers list:
        for header in headers:
            list_values_day.append(day[header])
        response_array.append(list_values_day)
    return response_array

    ## for upload all stuff in nbu api
    # is_header_added = False
    # for day in response_json:
    #     if is_header_added == False:
    #         response_array.append(list(day.keys()))
    #         is_header_added = True
    #     response_array.append(list(day.values()))
    #return response_array

# For testing module:
# from datetime import timedelta
# value_1 = date.today() - timedelta(1) 
# value_2 = datetime.now()
# print(get_from_api(value_1, value_2))