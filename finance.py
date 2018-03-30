import mpl_finance
import sqlite3
import time
import random
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web


style.use('ggplot')
conn = sqlite3.connect('stock_price.db')
c = conn.cursor()


def create_database():
    df = pd.read_csv('tesla.csv', parse_dates=True, index_col=0)
    df.to_sql('stock_price.db', conn, if_exists='replace', index=False)
    conn.commit()


def read_from_db():
    df = pd.read_sql_query("SELECT * from 'stock_price.db'", conn)
    print(df.head())





def graph_data1():
    df = pd.read_sql_query("SELECT * from 'stock_price.db'", conn)
    df['100ma'] = df['Close'].rolling(window=100, min_periods=0).mean()
    df['200ma'] = df['Close'].rolling(window=200, min_periods=0).mean()
    df['50ma'] = df['Close'].rolling(window=50, min_periods=0).mean()
    ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
    ax1.plot(df.index, df['Close'])
    ax1.plot(df.index, df['200ma'])
    ax1.plot(df.index, df['100ma'])
    ax1.plot(df.index, df['50ma'])
    ax2.bar(df.index, df['Volume'])
    plt.show()

def graph_data2():
    df = pd.read_csv('tesla.csv', parse_dates=True, index_col=0)

    df_ohlc = df['Close'].resample('10D').ohlc()
    df_volume = df['Volume'].resample('10D').sum()

    df_ohlc.reset_index(inplace=True)

    df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

    ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
    ax1.xaxis_date()

    candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
    df.plot()
    plt.show()


#create_database()
#read_from_db()
graph_data2()
c.close()
conn.close()
