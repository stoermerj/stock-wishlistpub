import requests
import credentials

import time

COUNTING = 0

"""Defines the type of API to be called.
Input is the period as well as the type of stock
Ouput is the URL to be called"""
def define_api_type(period, stock):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_'+ period + '_ADJUSTED' + '&symbol='+ stock +'&apikey='+ credentials.API_KEY_STOCK
    return url

"""Calls and retrieves the API
Input is the URL to be called
Output is the raw data"""
def call_stock_api(url):
    global COUNTING
    if COUNTING == 5:
            print('TIMEOUT FUNCTION')
            time.sleep(60) #basic version of API only allows 5 calls per minute
            COUNTING = 0
    try:
        r = requests.get(url)
    except requests.exceptions.Timeout:
        print('Timeout')
        return None
    except requests.exceptions.HTTPError:
        print('HTTP ERROR')
        return None
    except:
        print('General Problem')
        return None
    data = r.json()
    if 'Error Message' in data and r.status_code == 200: #check if API returns 200 return but with it an error
        print('Wrong User Input')
        COUNTING = COUNTING + 1
        return None
    if 'Note' in data and r.status_code == 200:
        print("""Too many API Calls. 
              Take a break""", 
              data)
        COUNTING = COUNTING + 1
        return None
    print('API CALLED')
    COUNTING = COUNTING + 1
    print(COUNTING)
    return data