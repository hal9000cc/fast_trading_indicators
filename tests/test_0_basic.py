import pytest
import datetime as dt
import numpy as np
from src.fast_trading_indicators import TIME_TYPE
from src.fast_trading_indicators.common import param_time
import src.fast_trading_indicators as fti


def test_bad_datasource(config_default):
    with pytest.raises(TypeError) as error:
        indicators = fti.Indicators(None)


def test_no_date(config_default, default_source, default_symbol, default_timeframe):
    indicators = fti.Indicators(default_source)
    with pytest.raises(fti.FTIException) as error:
        indicators.OHLCV(default_symbol, default_timeframe)
    assert error.value.message == 'No begin_time set'


def test_no_date_end(config_default, default_source, default_symbol, default_timeframe):
    indicators = fti.Indicators(default_source, 20200101)
    with pytest.raises(fti.FTIException) as error:
        indicators.OHLCV(default_symbol, default_timeframe)
    assert error.value.message == 'No end_time set'


def test_no_date_begin(config_default, default_source, default_symbol, default_timeframe):
    indicators = fti.Indicators(default_source, date_end=20200101)
    with pytest.raises(fti.FTIException) as error:
        indicators.OHLCV(default_symbol, default_timeframe)
    assert error.value.message == 'No begin_time set'


@pytest.mark.parametrize('time_begin, time_end', [
    (20220702, 20220717),
    (20220725, 20220731)
])
def test_date_type_int(config_default, default_source, default_symbol, time_begin, time_end, a_timeframe):
    indicators = fti.Indicators(default_source)
    out = indicators.OHLCV(default_symbol, a_timeframe, time_begin=time_begin, time_end=time_end)
    assert out.time[0] == np.datetime64(param_time(time_begin, False)).astype(TIME_TYPE)
    assert out.time[-1] == np.datetime64(a_timeframe.begin_of_tf(param_time(time_end, True))).astype(TIME_TYPE)


@pytest.mark.parametrize('time_begin, time_end', [
    ('2022-07-02T10:10', '2022-07-17T15:15'),
    ('2022-07-25T13:59', '2022-07-31T15:23'),
    ('2022-07-25', '2022-07-31')
])
def test_date_type_str(config_default, default_source, default_symbol, time_begin, time_end, a_timeframe):
    indicators = fti.Indicators(default_source)
    out = indicators.OHLCV(default_symbol, a_timeframe, time_begin=time_begin, time_end=time_end)
    assert out.time[0] == np.datetime64(a_timeframe.begin_of_tf(param_time(time_begin, False))).astype(TIME_TYPE)
    assert out.time[-1] == np.datetime64(a_timeframe.begin_of_tf(param_time(time_end, True))).astype(TIME_TYPE)


def test_date_datetime(config_default, default_source, default_symbol, a_timeframe):

    indicators = fti.Indicators(default_source, 20220901, 20220905)

    time_begin, time_end = dt.datetime(2022, 9, 1, 3, 0), dt.datetime(2022, 9, 2, 2, 0)

    data = indicators.OHLCV(default_symbol, a_timeframe, time_begin=time_begin, time_end=time_end)
    assert data.time[0] == np.datetime64(a_timeframe.begin_of_tf(time_begin), 'ms')
    assert data.time[-1] == np.datetime64(a_timeframe.begin_of_tf(time_end), 'ms')


def test_date_v1(config_default, default_source, default_symbol, a_timeframe):

    indicators = fti.Indicators(default_source, 20220901, 20220905)

    data = indicators.OHLCV(default_symbol, a_timeframe)

    assert data.time[0] == np.datetime64('2022-09-01T00:00', 'ms')
    assert data.time[-1] == np.datetime64(a_timeframe.begin_of_tf(np.datetime64('2022-09-05T23:59', 'ms')), 'ms')


def test_date_v1_interval(config_default, default_source, default_symbol, a_timeframe):

    indicators = fti.Indicators(default_source, 20220901, 20220905)

    time_begin, time_end = dt.datetime(2022, 9, 1, 3, 0), dt.datetime(2022, 9, 2, 2, 0)

    data = indicators.OHLCV(default_symbol, a_timeframe, time_begin=time_begin, time_end=time_end)
    assert data.time[0] == np.datetime64(a_timeframe.begin_of_tf(time_begin), 'ms')
    assert data.time[-1] == np.datetime64(a_timeframe.begin_of_tf(time_end), 'ms')

    time_begin, time_end = np.datetime64('2022-09-01T03:00', 'm'),  np.datetime64('2022-09-02T02:00', 'm')

    data = indicators.OHLCV(default_symbol, a_timeframe, time_begin=time_begin, time_end=time_end)
    assert data.time[0] == np.datetime64(a_timeframe.begin_of_tf(time_begin), 'ms')
    assert data.time[-1] == np.datetime64(a_timeframe.begin_of_tf(time_end), 'ms')


def test_date_v1_interval_date(config_default, default_source, default_symbol, a_timeframe):

    indicators = fti.Indicators(default_source, 20220901, 20220905)

    time_begin, time_end = dt.date(2022, 9, 1), dt.date(2022, 9, 5)

    data = indicators.OHLCV(default_symbol, a_timeframe, time_begin=time_begin, time_end=time_end)
    assert data.time[0] == np.datetime64(time_begin, 'ms')
    assert data.time[-1] == np.datetime64(time_end + dt.timedelta(days=1)) - a_timeframe.timedelta64()


def test_OHLCV_out_of_the_period(config_default, default_timeframe):
    indicators = fti.Indicators('binance', date_begin=20220201, date_end=20220220)
    with pytest.raises(fti.FTIExceptionOutOfThePeriod) as error:
        out = indicators.OHLCV('um/ethusdt', default_timeframe, time_begin=20220210, time_end=20220221)


def test_OHLCV_ticks_not_found(config_default, default_timeframe):

    indicators = fti.Indicators('binance', date_begin=20100201, date_end=20100201)

    for symbol in ('um/ethusdt', 'cm/ethusd_perp', 'ethusdt'):
        with pytest.raises(fti.FTISourceDataNotFound) as error:
            out = indicators.OHLCV(symbol, default_timeframe)

