import requests
import pandas as pd
import arrow
import datetime

def get_quote_data(symbol , data_range='20d', data_interval='1h'):
    res = requests.get('https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={data_range}&interval={data_interval}'.format(**locals()))
    data = res.json()
    body = data['chart']['result'][0]
    dt = datetime.datetime
    dt = pd.Series(map(lambda x: arrow.get(x).to('US/Pacific').datetime.replace(tzinfo=None), body['timestamp']), name='Datetime')
    df = pd.DataFrame(body['indicators']['quote'][0], index=dt)
    dg = pd.DataFrame(body['timestamp'])
    df = df.loc[:, ('open', 'high', 'low', 'close', 'volume')]
    df.dropna(inplace=True)
    df.columns = ['OPEN', 'HIGH','LOW','CLOSE','VOLUME']
    #return df

    # Calculate SMA
    data_close = df.iloc[:,3]
    data_close['SMA50'] = data_close.rolling(50).mean()
    sma_value = data_close['SMA50'].tail(20).values.tolist()

    # Get High and Low
    data_high = df.iloc[:, 1]
    price_high = data_high.tail(5).values.tolist()

    data_low = df.iloc[:, 2]
    price_low = data_low.tail(5).values.tolist()

    # Get Volume
    data_volume = df.iloc[:, 4]
    volume = data_volume.tail(5).values.tolist()
    return symbol,sma_value,price_high,price_low,volume


