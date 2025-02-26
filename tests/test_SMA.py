import datetime as dt
import numpy as np
import pytest
import src.live_trading_indicators as lti
from src.live_trading_indicators.exceptions import *


@pytest.mark.parametrize('time_begin, time_end, period', [
    ('2022-07-01', '2022-07-22', 1),
    ('2022-07-01', '2022-07-10', 3),
    ('2022-07-01', '2022-07-10', 5),
    ('2022-07-01', '2022-07-31', 22),
    ('2022-07-01', '2022-07-22', 22)
])
def test_sma(config_default, test_source, time_begin, time_end, period, a_big_timeframe):

    test_symbol = 'um/ethusdt'

    indicators = lti.Indicators(test_source)
    out = indicators.OHLCV(test_symbol, a_big_timeframe, time_begin, time_end)
    sma = indicators.SMA(test_symbol, a_big_timeframe, time_begin, time_end, period=period)

    values = out.close
    values_sma = sma.sma
    for i in range(len(values)):

        if i < period - 1:
            assert np.isnan(values_sma[i])
            continue

        assert values_sma[i] - values[i - period + 1: i + 1].sum() / period < 1e-12


@pytest.mark.parametrize('time_begin, time_end, period', [
    ('2022-07-01', '2022-07-22', 1),
    ('2022-07-01', '2022-07-10', 3),
    ('2022-07-01', '2022-07-10', 5),
    ('2022-07-01', '2022-07-31', 22),
    ('2022-07-01', '2022-07-22', 22),
    ((dt.datetime.utcnow() - dt.timedelta(days=5)).date(), None, 5)  # live
])
def test_sma1(config_default, test_source, time_begin, time_end, period, a_big_timeframe):

    test_symbol = 'um/ethusdt'

    indicators = lti.Indicators(test_source, time_begin, time_end)
    out = indicators.OHLCV(test_symbol, a_big_timeframe)
    sma = indicators.SMA(test_symbol, a_big_timeframe, period=period)

    values = out.close
    values_sma = sma.sma
    for i in range(len(values)):

        if i < period - 1:
            assert np.isnan(values_sma[i])
            continue

        assert values_sma[i] - values[i - period + 1: i + 1].sum() / period < 1e-11


@pytest.mark.parametrize('time_begin, time_end, period, timeframe', [
    ('2022-07-01', '2022-07-10', 22, lti.Timeframe.t1d),
    ('2022-07-01', '2022-07-21', 22, lti.Timeframe.t1d),
    ('2022-07-01', '2022-07-10', 241, lti.Timeframe.t1d)
])
def test_sma_value_error(config_default, test_source, test_symbol, time_begin, time_end, period, timeframe):

    indicators = lti.Indicators(test_source)
    out = indicators.OHLCV(test_symbol, timeframe, time_begin, time_end)
    with pytest.raises(LTIExceptionTooLittleData):
        sma = indicators.SMA(test_symbol, timeframe, time_begin, time_end, period=period)

