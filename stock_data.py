import api_caller

import pandas as pd
import os

from datetime import datetime, timedelta

TODAYS_DATE = pd.to_datetime(datetime.today().strftime('%Y-%m-%d')) #todays_date as pandas class

"""Checks if the data from the API should be called or if it is available as CSV
Input is the period (weekly or monthly)
Output is the stock type (e.g. BP"""
def api_csv_check(period, stock): #function to check if data is available. Output is False if file does not exist or old
    stock = stock.replace('.','') #to avoid any save issues
    stock = stock.replace('/','')
    file_name = 'stock_data/'+stock+'-'+period+'.csv'
    file_exists = os.path.isfile(file_name)
    if file_exists == True:
        df = pd.read_csv(file_name)
        df = df.rename(columns = {'Unnamed: 0': ''})
        df = df.set_index('')
        df['date']= pd.to_datetime(df['date'], format='%Y-%m-%d')
        input_last_entry = df.iloc[0,0] #get last date of stock's value
        day_delta = TODAYS_DATE - input_last_entry
        if day_delta < timedelta(days=7) and period == 'weekly':
            print('CSVUSED')
            return df
        elif day_delta < timedelta(days=31) and period == 'monthly':
            print('CSVUSED')
            return df
        else: 
            return False
    elif file_exists == False: #if file does not exist
        return False

"""Builds a pandas dataframe out of the raw JSON data if API is called
Input is the raw API json data, the period (weekly or monhtly) as well as the stock (e.g. BP)
Output is a pandas dataframe with the data as well as the closing value on that date"""
def build_dataframe(data, period, stock):
    try:
        df = pd.DataFrame.from_dict(data)
        df = df.iloc[4: , 1: , ] #ignore first 4 rows and take relevant time series column
        close = [item['4. close'] for item in df.iloc[:, 0]] #only take out the end of day value from dictionary
        df['close'] = close #add close as new column to dataframe 
        df['close'] = df['close'].astype(float) #change type of close to float
        df = df.iloc[:, 1: , ] #remove dict from df 
        df = df.reset_index() #do not use dates as index
        df = df.rename(columns={'index':'date'}) #rename original index
        df['date']= pd.to_datetime(df['date'], format='%Y-%m-%d') #date change to datetime object
        stock = stock.replace('.','') #to avoid any save issues with foreign stocks
        df.to_csv('stock_data/'+stock+'-'+period+'.csv')#+' '+str((TODAYS_DATE).replace(':',"-"))+'.csv') #personalized name for csv after stock and period used
        return df
    except ValueError:
        print(data)
        print('VALUE ERROR PROBLEM in build_dataframe function')

"""Merges all the API calls for the different stocks into one dataframe
Input is the period as well as all the stocks
Output is one dataframe with the data as well as the closing dates of all the stocks"""
def executer_stock_dataframe(period, *arg): #arg can be any number of stocks
    df = []
    for index, stock in enumerate(arg):
        stock_data = api_csv_check(period, stock)
        if isinstance(stock_data, bool): #check if stock_data is a boolean. If yes, call api
            stock_data = api_caller.define_api_type(period, stock)
            stock_data = api_caller.call_stock_api(stock_data)
            if stock_data == None: #check to see if input is a valid stock
                continue
            stock_data= build_dataframe(stock_data, period, stock) #build df
        stock_data = stock_data.rename(columns = {'close': stock})
        if index == 0: #use first stock df 
            stock_data['difference '+ stock] = stock_data[stock].diff(-1)
            df.append(stock_data) #set the first stock index as primary 
        if index != 0 and len(df) == 0: #used as an error handler if first stock value throws an error
            stock_data['difference '+ stock] = stock_data[stock].diff(-1)
            df.append(stock_data)
        if index != 0:
            stock_data['difference '+ stock] = stock_data[stock].diff(-1)
            df[0] = pd.merge(df[0], stock_data, on='date', how='left') #merge the two dfs
    df = df[0].set_index('date')
    return df

"""Calculates various KPIs, e.g. difference to last month/YTD
Input is the period (weekly or monthly) as well as the stocks (e.g. BP)
Output is a pandas dataframe with the calculations for all the stocks"""
def executer_calculation_dataframe(period, *arg):
    df = {'stocks' : [], period +' difference' : [],  'previous year date' : [], 'previous year difference': [], 'ytd date': [], 'ytd difference': []}
    for stock in arg:
        stock_data = api_csv_check(period, stock)
        if isinstance(stock_data, bool): #check if stock_data is a boolean. If yes, call api
            stock_data = api_caller.define_api_type(period, stock)
            stock_data = api_caller.call_stock_api(stock_data)
            if stock_data == None: #check to see if input is a valid stock
                continue
            stock_data= build_dataframe(stock_data, period, stock) #build df
        stock_data = stock_data.rename(columns = {'close': stock})

        #setup calculations
        date_last_entry = stock_data.iloc[0,0]
        date_previous_year = date_last_entry - timedelta(days=365)
        
        #find weekly or monthly difference 
        difference_previous_period_stock_value = stock_data.iloc[0, 1] - stock_data.iloc[1, 1]
        difference_previous_period_stock_value_percentage = round((difference_previous_period_stock_value / stock_data.iloc[0, 1]) * 100) #find percent difference between pervious two weeks/months    
    
        #find previous year's value 
        same_year_month = [date for date in stock_data['date'] if date.year == TODAYS_DATE.year-1 and date.month == TODAYS_DATE.month]
        previous_year_date_index = pd.Index(same_year_month).get_indexer([date_previous_year], method='nearest')
        previous_year_date_value = same_year_month[previous_year_date_index[0]]
        previous_year_stock_index = stock_data[stock_data['date'] == previous_year_date_value].index
        previous_year_stock_value = stock_data.iloc[previous_year_stock_index[0],1]
        difference_previous_year_stock_value = stock_data.iloc[0,1] - previous_year_stock_value
        difference_previous_year_stock_value_percentage = round((difference_previous_year_stock_value / stock_data.iloc[0, 1]) * 100)

        #find ytd value 
        january_dates = [date for date in stock_data['date'] if date.month == 1 and date.year == TODAYS_DATE.year]
        january_first_date_value = january_dates.pop()
        january_first_date_index = stock_data[stock_data['date'] == january_first_date_value].index
        january_first_stock_value = stock_data.iloc[january_first_date_index[0],1]
        difference_ytd_stock_value = stock_data.iloc[0,1] - january_first_stock_value
        difference_ytd_stock_value_percentage = round((difference_ytd_stock_value / stock_data.iloc[0, 1]) * 100)
                
        #add calculations and stocks to df
        df['stocks'].append(stock)
        df[period + ' difference'].append(difference_previous_period_stock_value_percentage)
        df['previous year date'].append(previous_year_date_value)
        df['previous year difference'].append(difference_previous_year_stock_value_percentage)
        df['ytd date'].append(january_first_date_value)
        df['ytd difference'].append(difference_ytd_stock_value_percentage)
    df = pd.DataFrame(df)
    return df