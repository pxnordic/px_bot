import MetaTrader5
from dataclasses import dataclass
from log import log
import random
import datetime
from datetime import timedelta
import numpy as np
import pandas as pd


@dataclass
class mt5_fetch:

    def __post_init__(self):
        self.logger = log.mylog(__name__)

    def gen_randomdate(self):
        end_date = datetime.datetime(2022, 12, 31)
        delta_days = np.round(random.random()*10*365)
        random_date = end_date - timedelta(days=delta_days)
        random_date = random_date - timedelta(days=random_date.weekday())
        return random_date

    def fetch_rates(self, symbol, timeframe, date_from, num_bars):
        return MetaTrader5.copy_rates_from(symbol, timeframe, date_from, num_bars)

    def fetch_rates_min_random(self, mt5_inst):
        symbol = mt5_inst.symbols[0]
        timeframe = mt5_inst.set_query_timeframe('M1')
        num_bars = 60*24*5

        while True:
            date_from = self.gen_randomdate()
            bars = self.fetch_rates(symbol=symbol, timeframe=timeframe,
                                    date_from=date_from, num_bars=num_bars)
            bars = pd.DataFrame(bars)
            if len(bars) == num_bars:
                break

        return bars

