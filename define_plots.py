import stock_data

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_axis(calc_df, stock_df):
    
    #setup dataframes for plots
    stock_values = [stock for stock in stock_df.columns if "difference" not in stock]
    stock_differences = [stock for stock in stock_df.columns if "difference" in stock]
    stock_df_values = stock_df[stock_values]
    stock_df_differences = stock_df[stock_differences]
    stock_calculations = [calc for calc in calc_df.columns if "date" not in calc]
    stock_df_calculations = calc_df[stock_calculations]
    stock_df_calculations_columns = list(stock_df_calculations.columns.values)
    stock_df_calculations_columns.pop(0)
    
    #define axes names
    df_row_length = len(calc_df.index)
    axes_names = [[i+"_1", i+"_2", i+"_3"] for i in["ax_"+calc_df.iloc[i,0] for i in range(df_row_length)]]
    axes_names_cleaned = []
    for x in axes_names:
        for y in x:
            axes_names_cleaned.append(y)
    
    #create canvas for figure depending on number of stocks
    fig = plt.figure()
    gs = fig.add_gridspec(len(axes_names)+4,3)
    fig.set_figheight(25)
    fig.set_figwidth(25)
    
    font = {'family' : 'Arial',
            'weight' : 'bold',
        'size'   : 8}
    plt.rc('font', **font)

    ax1 = fig.add_subplot(gs[:2, :])
    sns.lineplot(data=stock_df_values, ax = ax1)
    ax1.legend(loc='upper left', fontsize = '8')
    ax1.set_ylabel('Currency', fontsize = '8')
    
    ax2 = fig.add_subplot(gs[2:4, :])
    sns.lineplot(data=stock_df_differences, ax = ax2)
    ax2.legend(loc='upper left', fontsize = '8')
    ax2.set_ylabel('Currency', fontsize = '8')
    
    range_row = range(4, df_row_length+4)
    stock_number = 0  #used to choose the right stock
    for row in range_row: #define row
        
        #calculations for axes
        individual_stock_df_values = stock_df_values[[stock_df_values.columns[stock_number]]]
        individual_stock_df_values_previous_year = individual_stock_df_values.loc[: calc_df.iloc[stock_number,2]]
        individual_stock_df_values_previous_year.index = individual_stock_df_values_previous_year.index.strftime('%Y-%m')
        individual_stock_df_differences = stock_df_differences[[stock_df_differences.columns[stock_number]]]
        individual_stock_df_differences_previous_year = individual_stock_df_differences.loc[: calc_df.iloc[stock_number,2]]
        individual_stock_df_differences_previous_year.index = individual_stock_df_differences_previous_year.index.strftime('%Y-%m')
        individual_calculation_df_values = pd.DataFrame(stock_df_calculations.iloc[stock_number, 1:4])
        
        for count, axis_name in enumerate(axes_names_cleaned): #define name after stock

            for column_number in [0,1,2]: #define column
                axis_name = fig.add_subplot(gs[row,column_number], autoscale_on = True)
                axis_name.spines['top'].set_visible(False)
                axis_name.spines['right'].set_visible(False)
                
                
                
                if column_number == 0:
                    sns.lineplot(data = individual_stock_df_values_previous_year, ax = axis_name, markers = True)
                    axis_name.set_xlabel('', fontsize = '1')
                    axis_name.set_ylabel('Currency', fontsize = '8')
                    axis_name.tick_params(axis='x', labelrotation=90)
                    axis_name.legend(loc='upper left', fontsize = '8')
                    if row != range_row[-1]:   
                        axis_name.get_xaxis().set_ticks([])

                if column_number == 1:
                    sns.barplot(data = individual_stock_df_differences_previous_year, ax = axis_name, y = individual_stock_df_differences_previous_year[individual_stock_df_differences_previous_year.columns.values[0]], x = individual_stock_df_differences_previous_year.index)
                    axis_name.set_xlabel('', fontsize = '1')
                    axis_name.set_ylabel('Percent Diff.', fontsize = '8')
                    axis_name.tick_params(axis='x', labelrotation=90)
                    axis_name.bar_label(axis_name.containers[0], padding = 2)
                    axis_name.set_yticks([i for i in range(-100, 101, 40)])
                    if row != range_row[-1]:   
                        axis_name.get_xaxis().set_ticks([])
                        
                if column_number == 2:
                    sns.barplot(data = individual_calculation_df_values, ax = axis_name, y = individual_calculation_df_values[individual_calculation_df_values.columns[0]], x = individual_calculation_df_values.index)
                    #axis_name.tick_params(axis='x', labelrotation=90)
                    axis_name.set_xlabel('', fontsize = '1')
                    axis_name.set_ylabel('Percent Diff.', fontsize = '8')
                    axis_name.bar_label(axis_name.containers[0], padding = 2)
                    axis_name.set_yticks([i for i in range(-100, 101, 40)])                    
                    if row != range_row[-1]:   
                        axis_name.get_xaxis().set_ticks([])

        if df_row_length > stock_number + 1:
            stock_number = stock_number + 1
    
    png_path = 'plots/'+str(stock_values).replace("'", "")+'-' + str(stock_data.TODAYS_DATE.strftime('%Y-%m-%d')).replace(':',"-") +'.png'
    if os.path.exists(png_path) is True:
        os.remove(png_path)
    plt.savefig(png_path)