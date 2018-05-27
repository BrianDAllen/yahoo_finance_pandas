import requests
import datetime
import json
import pandas as pd


def _convert_epoch_to_datetime(epoch_seconds):
    epoch = datetime.datetime(1970, 1, 1)
    dt = epoch + datetime.timedelta(seconds=epoch_seconds)
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


def _convert_datetime_to_epoch(dt):
    epoch = datetime.datetime(1970, 1, 1)

    return int((dt - epoch).total_seconds())


# Collect dividends from yahoo finance for the given ticker for the time period of start_date to end_date.
#
# ticker(string) - stock ticker in caps, ex: AAPL, IBM, IVV
# start_date(datetime) - earliest date to collect price for the given ticker
# end_date(datetime) - latest date to collect price for the given ticker
def get_dividends(ticker=None, start_date=datetime.datetime(2010, 1, 1), end_date=datetime.datetime.now()):

    # convert datetimes to epoch
    dstart_secs = _convert_datetime_to_epoch(start_date)
    dend_secs = _convert_datetime_to_epoch(end_date)

    # set url for yahoo finance with filled in parameters
    url = "https://finance.yahoo.com/quote/{0}/history?period1={1}&period2={2}&interval=1d&filter=history&frequency=1d".format(
        ticker, dstart_secs, dend_secs)

    response = requests.get(url).content

    # find the json object in the response, format it, and load it
    index_s = response.find("HistoricalPriceStore")
    index_e = response.find("isPending", index_s)

    response = response[index_s:index_e]
    json_string = response[22:len(response) - 2] + "}"

    mm = json.loads(json_string)
    dividends = []
    for row in mm["prices"]:
        if "type" in row:
            dividends.append(row)

    df_dividends = pd.DataFrame.from_dict(dividends)
    df_dividends["date"] = df_dividends["date"].apply(lambda x: _convert_epoch_to_datetime(x))
    del df_dividends["data"]

    return df_dividends