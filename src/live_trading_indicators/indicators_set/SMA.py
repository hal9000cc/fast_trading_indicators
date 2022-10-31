from ..calculator import ma_calculate
from ..indicator_data import IndicatorData


def get_indicator_out(indicators, symbol, timeframe, period, value='close'):

    ohlcv = indicators.get_bar_data(symbol, timeframe)
    source_values = ohlcv.data[value]

    out = ma_calculate(source_values, period)

    return IndicatorData({
        'name': 'SMA',
        'timeframe': timeframe,
        'time': ohlcv.time,
        f'sma_{value}': out
    })

