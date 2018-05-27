import requests
import json
import datetime
import pandas as pd


def _get_fmt_value(x, v_type='float'):
    try:
        if v_type == 'float':
            return float(x['fmt'])

        elif v_type == 'percent':
            return float(x['raw'])

        elif v_type == 'int':
            return int(x['fmt'])

        elif v_type == 'date':
            return datetime.datetime.strptime(x['fmt'], '%Y-%m-%d')

        else:
            return x['fmt']
    except:
        if v_type == 'float':
            return 0.0

        elif v_type == 'percent':
            return 0.0

        elif v_type == 'int':
            return 0

        elif v_type == 'date':
            return ''


def _clean_and_return_options(jd):
    df_calls = pd.DataFrame.from_dict(jd['optionChain']['result'][0]['options'][0]['calls'])
    df_puts = pd.DataFrame.from_dict(jd['optionChain']['result'][0]['options'][0]['puts'])

    df_calls['ask'] = df_calls['ask'].apply(lambda x: _get_fmt_value(x, v_type='float'))
    df_calls['bid'] = df_calls['bid'].apply(lambda x: _get_fmt_value(x, v_type='float'))
    df_calls['change'] = df_calls['change'].apply(lambda x: _get_fmt_value(x, v_type='float'))
    df_calls['expiration'] = df_calls['expiration'].apply(lambda x: _get_fmt_value(x, v_type='date'))
    df_calls['impliedVolatility'] = df_calls['impliedVolatility'].apply(lambda x: _get_fmt_value(x, v_type='percent'))
    df_calls['lastPrice'] = df_calls['lastPrice'].apply(lambda x: _get_fmt_value(x, v_type='float'))
    df_calls['lastTradeDate'] = df_calls['lastTradeDate'].apply(lambda x: _get_fmt_value(x, v_type='date'))
    df_calls['openInterest'] = df_calls['openInterest'].apply(lambda x: _get_fmt_value(x, v_type='int'))
    df_calls['percentChange'] = df_calls['percentChange'].apply(lambda x: _get_fmt_value(x, v_type='percent'))
    df_calls['strike'] = df_calls['strike'].apply(lambda x: _get_fmt_value(x, v_type='float'))
    df_calls['volume'] = df_calls['volume'].apply(lambda x: _get_fmt_value(x, v_type='int'))

    df_puts['ask'] = df_puts['ask'].apply(lambda x: _get_fmt_value(x, v_type='float'))
    df_puts['bid'] = df_puts['bid'].apply(lambda x: _get_fmt_value(x, v_type='float'))
    df_puts['change'] = df_puts['change'].apply(lambda x: _get_fmt_value(x, v_type='float'))
    df_puts['expiration'] = df_puts['expiration'].apply(lambda x: _get_fmt_value(x, v_type='date'))
    df_puts['impliedVolatility'] = df_puts['impliedVolatility'].apply(lambda x: _get_fmt_value(x, v_type='percent'))
    df_puts['lastPrice'] = df_puts['lastPrice'].apply(lambda x: _get_fmt_value(x, v_type='float'))
    df_puts['lastTradeDate'] = df_puts['lastTradeDate'].apply(lambda x: _get_fmt_value(x, v_type='date'))
    df_puts['openInterest'] = df_puts['openInterest'].apply(lambda x: _get_fmt_value(x, v_type='int'))
    df_puts['percentChange'] = df_puts['percentChange'].apply(lambda x: _get_fmt_value(x, v_type='percent'))
    df_puts['strike'] = df_puts['strike'].apply(lambda x: _get_fmt_value(x, v_type='float'))
    df_puts['volume'] = df_puts['volume'].apply(lambda x: _get_fmt_value(x, v_type='int'))

    return df_calls, df_puts


# Collect current option chains from yahoo finance for the given ticker.
#
# ticker(string) - stock ticker in caps, ex: AAPL, IBM, IVV
# start_date(datetime) - earliest date to collect price for the given ticker
# end_date(datetime) - latest date to collect price for the given ticker
def get_option_chains(ticker=None):
    headers = {
        'authority': 'query1.finance.yahoo.com',
        'method': 'GET',
        'path': '/v7/finance/options/IBM?formatted=true&crumb=ZeAb%2F1A09Ta&lang=en-US&region=US&date=1527811200&corsDomain=finance.yahoo.com',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'dnt': '1',
        'origin': 'https://finance.yahoo.com',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'

    }

    calls = []
    puts = []

    # get first options to get all the expiration dates
    url = '''https://query1.finance.yahoo.com/v7/finance/options/{0}?formatted=true&lang=en-US&region=US&corsDomain=finance.yahoo.com'''.format(
        ticker)
    print url
    a = requests.request(url=url, method='GET', headers=headers)

    # get and store first set of options
    jd = json.loads(a.content)
    cur_calls, cur_puts = _clean_and_return_options(jd)
    calls.append(cur_calls)
    puts.append(cur_puts)

    # now walk through the rest of the expirations, collecting the rest
    # skip first since we already have it
    exps = jd['optionChain']['result'][0]['expirationDates'][1:]
    for exp in exps:
        url = '''https://query1.finance.yahoo.com/v7/finance/options/{0}?formatted=true&lang=en-US&region=US&date={1}&corsDomain=finance.yahoo.com'''.format(
            ticker, exp)
        print url

        a = requests.request(url=url, method='GET', headers=headers)
        jd = json.loads(a.content)
        cur_calls, cur_puts = _clean_and_return_options(jd)
        calls.append(cur_calls)
        puts.append(cur_puts)

    # finally, concat all the calls and puts into 2 dfs
    df_calls = pd.concat(calls)
    df_puts = pd.concat(puts)

    return df_calls, df_puts
