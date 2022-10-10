import os.path as path
import numpy as np
from common import *


class TimeframeData:

    def __init__(self, datasource_module, **kwargs):

        cash_folder = kwargs.get('timeframe_data_path')
        if cash_folder is None:
            self.cash_folder = path.join(TIMEFRAME_DATA_PATH, datasource_module.datasource_name())

        datasource_module.init()
        self.datasource_module = datasource_module

    def get_timeframe_day_data(self, symbol, timeframe, day_date):

        filename = self.filename_day_data(symbol, timeframe, day_date)
        if path.isfile(filename):
            day_data = self.load_from_cash(filename)
        else:
            day_data = self.datasource_module.timeframe_day_data(symbol, timeframe, day_date)
            self.save_to_cash(filename, day_data)

        self.check_day_data(day_data, symbol, timeframe, day_date)
        return day_data

    def check_day_data(self, day_data, symbol, timeframe, day_date):
        pass

    def get_timeframe_data(self, symbol, timeframe, date_begin, date_end):

        if date_begin is None:
            raise FTIException('No begin_date set')

        if date_end is None:
            raise FTIException('No end_date set')

        td_time, td_open, td_high, td_low, td_close, td_volume = [], [], [], [], [], []
        day_date = date_begin
        while day_date <= date_end:
            day_data = self.get_timeframe_day_data(symbol, timeframe, day_date)
            td_time.append(day_data.time)
            td_open.append(day_data.open)
            td_high.append(day_data.high)
            td_low.append(day_data.low)
            td_close.append(day_data.close)
            td_volume.append(day_data.volume)

        return IndicatorData({
                                'time': np.hstack(td_time),
                                'open': np.hstack(td_open),
                                'high': np.hstack(td_high),
                                'low': np.hstack(td_low),
                                'close': np.hstack(td_close),
                                'volume': np.hstack(td_volume)
                             })
