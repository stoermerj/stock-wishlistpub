import stock_data
import define_plots
import send_gmail

import pandas as pd
import os

STOCK_INPUT = ['GM', 'ads.de', 'alv.de', 'bas.de', 'bei.de', 'bmw.de', 'BNP.PA', 'BA', 'dpw.de', 'dte.de', 'gis.de', 'hen.de', 'H2X3.MU', 'intc', 'jnj', 'b4b.de', 'msft', 'nvda', 'pep', 'pg', 'pum.de', 'sap.de', 'khc', 'wmt', 'wbd']
PERIOD_INPUT = ['monthly'] #input is weekly or monthly

def main():
    token = os.environ.get("SOME_SECRET")
    if not token:
        raise RuntimeError("SOME_SECRET env var is not set")

    """Combines the global STOCK_INPUT and PERIOD_INPUT and turns it into different lists
    Input is the period and stocks taken from the globals
    Output are lists within a list with a maximum of 4 stocks per list and the period in the first position"""
    def create_input(period, stock):
        stock_list = []
        sub_lists = len(stock)/4
        if sub_lists > 1:
            while sub_lists >= 1:
                five_stocks = stock[:4]
                stock_list.append(period+five_stocks)
                del(stock[:4])
                sub_lists = len(stock)/4
        
        if sub_lists > 0 and sub_lists < 1:
            stock_list.append(period+stock)
        return stock_list

    """Creates a list of dataframes from the stocks by using the stock_data module
    Input is the stock list from the create_input function
    Output is a list with two different types of dfs from the module stock_data"""
    def create_dataframes(stock_lists):
        df_list = []
        for index, stocks in enumerate(stock_lists):
            calc_caller = str(index) + '_calc_df'
            calc_caller = stock_data.executer_calculation_dataframe(*stocks)
            df_list.append(calc_caller)
            
            stock_caller = str(index) + '_stock_df'
            stock_caller = stock_data.executer_stock_dataframe(*stocks)
            df_list.append(stock_caller)
        return df_list

    """Creates the plots and saves figures of them
    Input are the list of dfs from the create_dataframes function
    Output is a saved file(s) found under plots. The files are dated in the name"""
    def create_plots(df_lists):
        calc_and_stock_df = df_lists[:2]
        while len(df_lists) != 0:
            calc_and_stock_df = df_lists[:2]
            del(df_lists[:2])
            plot = define_plots.create_axis(*calc_and_stock_df)

    """Makes the important calculations from the stock_data ready to be send via HTML per mail
    Input is the calculation df from the create_dataframes function
    Output is a HTML file"""
    def create_e_mail_data(df_list):
        df_list = [df for index, df in enumerate(df_list) if (index % 2) == 0]
        calc_df = []
        for df in df_list:
            calc_values = [calc for calc in df.columns if "date" not in calc]
            calc_df_values = df[calc_values]
            calc_df.append(calc_df_values)
        calc_df = pd.concat(calc_df, axis=0, ignore_index=True)
        print(calc_df)
        calc_df = calc_df.to_html() #turn df to html
        html_text = '<!DOCTYPE html><html><body><p>' + calc_df +'</p></body></html>' #organize html for e-mail format
        return html_text

    dataframe_for_plot = create_dataframes(create_input(PERIOD_INPUT, STOCK_INPUT))
    dataframe_for_email = dataframe_for_plot.copy()
    
    create_plots(dataframe_for_plot) #execute for updated graphs
    send_gmail.send(create_e_mail_data(dataframe_for_email)) #execute for email

if __name__ == '__main__':
  main()
  
'''
Improvements
TODO: Beautiful interactive graphics
TODO: add single day call of stocks and send an e-mail if value is above or below 10% 
TODO: Delete CSV if older then 2 months
TODO: Find tickers of companies
TODO: Add exception for stocks that are only in index for less than a year
TODO: Show error messages in mail for stocks
'''

