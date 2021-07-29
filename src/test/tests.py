import pandas as pd
import datetime as dt
import pandas_datareader as web
start = dt.datetime(2010, 6, 30)


def get_stock_price_and_sma(symbol):
    #df = web.DataReader(symbol, 'yahoo', start) for US
    # for India
    df = web.DataReader(symbol, 'yahoo', start)
    # Calculate SMA
    data_close = pd.DataFrame(df.Close)
    data_close['SMA50'] = data_close.rolling(50).mean()
    sma_value = data_close['SMA50'].tail(20).values.tolist()

    # Get High and Low
    data_high = pd.DataFrame(df.High).tail(5)
    data_high['SMA50'] = data_high
    price_high = data_high['SMA50'].tolist()

    data_low = pd.DataFrame(df.Low).tail(5)
    data_low['SMA50'] = data_low
    price_low = data_low['SMA50'].tolist()

    return symbol, sma_value, price_high, price_low


def stock_red_to_green(stock_with_prices):
    symbol, sma_value, price_high, price_low = stock_with_prices
    # Get SMA
    *others, sma3, sma2, sma1,  = sma_value

    # Screen for turning from Red to Green
    ans1 = sma1 > sma2
    ans2 = sma2 < sma3

    if ans1 and ans2:
        return True
    else:
        return False


def sma_crossing_current(stock_with_prices):
    symbol, sma_value, price_high, price_low = stock_with_prices
    # def screen_buystocks(symbol):

    # df = web.DataReader(symbol, 'yahoo', start)
    # Calculate SMA

    *others, sma10, sma9, sma8, sma7, sma6, sma5, sma4, sma3, sma2, sma1,  = sma_value

    # Get High and Low
    *others, high5, high4, high3, high2, high1 = price_high
    *others, low5, low4, low3, low2, low1 = price_low

    # Screen for SMA Crossing down the price
    ans1 = sma1 < sma2
    ans2 = sma2 < sma3
    ans3 = high1 > sma1 > low1

    # Screen for turning from Red to Green
    ans11 = sma1 > sma2
    ans12 = sma2 < sma3
    ans13 = sma1 < high1

    # Screen for recently turned buy
    ans21 = sma1 > sma2
    ans22 = sma2 > sma3
    ans23 = sma3 > sma4
    ans24 = sma4 > sma5
    ans25 = sma5 > sma6
    ans26 = sma6 > sma7
    ans27 = sma7 > sma8
    ans28 = sma8 > sma9
    ans29 = sma9 > sma10

    if ans1 and ans2 and ans3:
        is_cross = True
    else:
        is_cross = False
    if ans11 and ans12 and ans13:
        is_red_to_green = True
    else:
        is_red_to_green = False

    if ans21 and ans22 and not ans23:
        is_recent_buy = True

    if ans21 and ans22 and ans23 and not ans24:
        is_recent_buy = True

    if ans21 and ans22 and ans23 and ans24 and not ans25:
        is_recent_buy = True

    if ans21 and ans22 and ans23 and ans24 and ans25 and not ans26:
        is_recent_buy = True

    else: is_recent_buy = False

    return is_cross, is_red_to_green,is_recent_buy


def stock_green_to_red(stock_with_prices):
    symbol, sma_value, price_high, price_low = stock_with_prices
    # Get SMA
    *others, sma3, sma2, sma1,  = sma_value

    # Screen for turning from Red to Green
    ans1 = sma1 <= sma2

    if ans1:
        return True
    else:
        return False
