from src.test.tests import sma_crossing_current
from src.utils.mail_utils import send_mail_with_attachment
from src.utils.utils import read_from_file,write_to_file
from src.test.tests import get_stock_price_and_sma
import os
from datetime import datetime


today = datetime.today()
path_current = os.path.dirname(os.getcwd())
os.chdir(path_current)
PROJECT_ROOT = os.getcwd()

file_red_to_green_daily = PROJECT_ROOT+"/output/red_to_green_stocks_daily_"+str(today)+".csv"
file_to_read_usa = PROJECT_ROOT+"/testData/NASDAQ.csv"
stocks_to_check = read_from_file(file_to_read_usa)

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Start Time =", current_time)

for stocks in stocks_to_check:
    try:
        print(f"Checking for {stocks}")
        stock_details = get_stock_price_and_sma(stocks)
        is_cross, is_red_to_green = sma_crossing_current(stock_details[0:4])
        if is_cross:
            write_to_file(f"{stock_details[0]} cross", file_red_to_green_daily)
        if is_red_to_green:
            write_to_file(f"{stock_details[0]} red_to_green", file_red_to_green_daily)
    except:
        print(f"Failed getting data for {stocks}")
        pass

send_mail_with_attachment(file_red_to_green_daily)
