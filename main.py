import log
from mt5_handler import mt5_handler
from mt5_fetch import mt5_fetch

from datetime import datetime
import pandas as pd
pd.set_option('display.max_columns', 500) # number of columns to be displayed
pd.set_option('display.width', 1500)      # max table width to display
# import pytz module for working with time zone
import pytz
import MetaTrader5
import pandas_ta as ta


# Main function
if __name__ == '__main__':
    mt5_handler_inst = mt5_handler.mt5_handle(mt5_json_file='example_settings.json')
    mt5_handler_inst.start_mt5()
    mt5_handler_inst.initialize_symbols()

    mt5_fetch_inst = mt5_fetch.mt5_fetch()
    bars = mt5_fetch_inst.fetch_rates_min_random(mt5_inst=mt5_handler_inst)

    timezone = pytz.timezone("Etc/UTC")
    # create 'datetime' object in UTC time zone to avoid the implementation of a local time zone offset
    utc_from = datetime(2020, 1, 10, tzinfo=timezone)
    # get 10 EURUSD H4 bars starting from 01.10.2020 in UTC time zone
    rates = MetaTrader5.copy_rates_from("USDJPY", MetaTrader5.TIMEFRAME_M12, utc_from, 10)

    print(len(bars))
    #print(rates)
    



