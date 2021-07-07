from src.test.tests import sma_crossing_current
from datetime import date
from src.test.mail_utils import send_mail_with_attachment
from src.test.yahoo_api import get_quote_data
from src.test.utils import read_from_file, write_to_file
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('v1')
args = parser.parse_args()
today = date.today()
PROJECT_ROOT = "/home/ssm-user/myFolder/StockScreener"

for file in os.scandir(PROJECT_ROOT+"/output"):
    if file.name.endswith(".csv"):
        os.unlink(file.path)

market = args.v1

file_red_to_green = PROJECT_ROOT+"/output/red_to_green_stocks_daily_"+market+"_"+str(today)+".csv"
file_to_read_usa = PROJECT_ROOT+"/src/testData/"+market+".csv"
stocks_to_check = read_from_file(file_to_read_usa)
for stocks in stocks_to_check:
    try:
        print(f"Checking for {stocks}")
        stock_details = get_quote_data(stocks, '60d', '1d')
        volume_daily = stock_details[4]

        volume = stock_details[4]
        if volume_daily[0] >= 750000:
            is_cross, is_red_to_green = sma_crossing_current(stock_details[0:4])
            if is_cross:
                write_to_file(f"{stock_details[0]} cross", file_red_to_green)
            if is_red_to_green:
                write_to_file(f"{stock_details[0]} red_to_green", file_red_to_green)
        else:
            print(f"Skipped {stocks} as the volume is less")
    except:
        print(f"Failed getting data for {stocks}")
        pass

send_mail_with_attachment(file_red_to_green,market+"_"+str(today)+"_daily.csv",market+"_"+str(today)+"_daily")