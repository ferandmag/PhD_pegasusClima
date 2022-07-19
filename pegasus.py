# CreatedBy: Fernando Maglia, 2022-07-18

# import libraries
import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from matplotlib.backends.backend_pdf import PdfPages


# process function
def process(dataset, startline=6,  encoding='cp1252'):
    """
    Args:
        dataset (_type_): csv file
        startline (int, optional): Defaults to 6
        encoding (str, optional): Defaults to 'cp1252'
    """

    # open the dataframe and select interest data
    df = pd.read_csv(dataset, encoding=encoding)
    df = df.iloc[startline:,]
    
    # rename columns
    df = df.rename(columns={df.columns.values[0]: 'date',
                            df.columns.values[1]:'value'})
    
    # transform column 'date' str to datetime
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y %H:%M')

    # set 'date' as index
    df = df.set_index(df['date'])

    # transform column 'value' str to float
    df['value'] = pd.to_numeric(df['value'])

    # create a dataframe with max, min and mean per day
    export = df.resample('D').min()
    export = export.rename(columns={'value':'min_day'})
    export = export.assign(max_day=((df.resample('D').max()).value))
    export = export.assign(mean_day=((df.resample('D').mean()).value))
        
    # create a dataframe with mean and std per month
    stats = df.resample('M').mean()
    stats = stats.rename(columns={'value':'mean_month'})
    stats = stats.assign(std_month=((df.resample('M').std()).value))

    return(export, stats)


# main function
def graph(dataset, variable, startline=6, encoding='cp1252'):
    """
    Args:
        dataset (_type_): csv file
        variable(str): 'temperature' or 'humidity'
        startline (int, optional): Defaults to 6
        encoding (str, optional): Defaults to 'cp1252'
    """

    # calling process function
    export, stats = process(dataset, startline=6, encoding='cp1252')
    
    if variable == 'temperature':
        yunit = '°C'
    if variable == 'humidity':
        yunit = '%'
        
    # line plots days {variable} (min, max and mean)
    line_plot3 = plt.figure(figsize=(8, 6), dpi=80)
    plt.plot(export.loc[:, 'min_day'],
            color='blue',
            linewidth=1,
            label='min_day')
    plt.plot(export.loc[:, 'max_day'],
            color='red',
            linewidth=1,
            label='max_day')
    plt.plot(export.loc[:, 'mean_day'],
            color='green',
            linewidth=.5,
            label='mean_day')

    plt.grid(linewidth=0.3)
    plt.legend(loc='lower right')
    plt.title(f'Min, Max and Mean {variable}')
    plt.xticks(rotation=90)
    plt.xlabel('Date [days]')
    plt.ylabel(f'{variable} [{yunit}]')
    plt.tight_layout()
    
    # line plots days {variable} (min and max)
    line_plot2 = plt.figure(figsize=(8, 6), dpi=80)
    plt.plot(export.loc[:, 'min_day'],
            color='blue',
            linewidth=1,
            label='min_day')
    plt.plot(export.loc[:, 'max_day'],
            color='red',
            linewidth=1,
            label='max_day')

    plt.grid(linewidth=0.3)
    plt.legend(loc='lower right')
    plt.title(f'Min and Max {variable}')
    plt.xticks(rotation=90)
    plt.xlabel('Date [days]')
    plt.ylabel(f'{variable} [{yunit}]')
    plt.tight_layout()

    # boxplots min, max and mean {variable}
    boxplot = plt.figure(figsize=(8, 6), dpi=80)
    sns.boxplot(data=export[['min_day', 'mean_day', 'max_day']],
                palette=['blue', 'green', 'red'])
    plt.grid(linewidth=0.3)
    plt.xticks(np.arange(3), ['Min', 'Mean', 'Max'])
    plt.title(f'Boxplots min, max and mean {variable}')
    plt.ylabel(f'{variable} [{yunit}]')
    plt.tight_layout()

    # folder creation
    current_str = datetime.datetime.strftime(datetime.datetime.today(),
                                                "%Y-%m-%d , %H-%M-%S")
    folder = f'./Analysis {current_str} , {dataset}'
    os.mkdir(folder)

    # csvs creation
    export.to_csv(f'{folder}/days_values.csv')
    stats.to_csv(f'{folder}/stats.csv')

    # pdfs plots creation
    with PdfPages(f'{folder}/figures.pdf') as pdf:
        pdf.savefig(line_plot2)
        pdf.savefig(line_plot3)
        pdf.savefig(boxplot)


def main(args):
    if len(args) == 3:
        graph(args[1], args[2])
    if len(args) == 4:
        graph(args[1], args[2], startline=args[3])
    if len(args) == 5:
        graph(args[1], args[2], startline=args[3], encoding=args[4])


if __name__ == "__main__":
    main(sys.argv)
