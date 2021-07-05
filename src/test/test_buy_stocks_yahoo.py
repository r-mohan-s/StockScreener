from src.test.tests import sma_crossing_current
from datetime import date
from src.test.mail_utils import send_mail_with_attachment
from src.test.yahoo_api import get_quote_data
from src.test.utils import read_from_file, write_to_file
import os

today = date.today()
path_current = os.path.dirname(os.getcwd())
os.chdir(path_current)
PROJECT_ROOT = os.getcwd()

file_red_to_green_hourly = PROJECT_ROOT+"/output/red_to_green_stocks_hourly_"+str(today)+".csv"
file_red_to_green_daily = PROJECT_ROOT+"/output/red_to_green_stocks_daily_"+str(today)+".csv"

#file_to_read_usa = PROJECT_ROOT+"/StockScreener/src/testData/NASDAQ.csv"
file_to_read_usa = "/testData/NASDAQ.csv"
stocks_to_check = read_from_file(file_to_read_usa)
for stocks in stocks_to_check:
    try:
        print(f"Checking for {stocks}")
        stock_details_daily = get_quote_data(stocks, '100d', '1d')
        volume_daily = stock_details_daily[4]

        stock_details = get_quote_data(stocks)
        volume = stock_details[4]
        if(volume_daily[0] >=750000):
            is_cross_hour, is_red_to_green_hour = sma_crossing_current(stock_details[0:4])
            if is_cross_hour:
                write_to_file(f"{stock_details[0]} cross", file_red_to_green_hourly)
            if is_red_to_green_hour:
                write_to_file(
                f"{stock_details[0]} red_to_green", file_red_to_green_hourly)
            is_cross_daily, is_red_to_green_daily = sma_crossing_current(stock_details_daily[0:4])
            if is_cross_daily:
                write_to_file(f"{stock_details[0]} cross", file_red_to_green_daily)
            if is_red_to_green_daily:
                write_to_file(
                f"{stock_details[0]} red_to_green", file_red_to_green_daily)

        else:
            print(f"Skipped {stocks} as the volume is less")
    except:
        print(f"Failed getting data for {stocks}")
        pass




send_mail_with_attachment(file_red_to_green_hourly)
