import yahoo_finance_pandas
import datetime

# get stock prices
stocks_df = yahoo_finance_pandas.get_stocks(ticker='IBM',
                                            start_date=datetime.datetime(2018,1,1),
                                            end_date=datetime.datetime(2018,4,1))

# results:
print stocks_df.head()


# get dividends
dividend_df = yahoo_finance_pandas.get_dividends(ticker='IBM',
                                            start_date=datetime.datetime(2018,1,1),
                                            end_date=datetime.datetime(2018,4,1))

# results
print dividend_df.head()


# get current option chains
option_calls_df, option_puts_df = yahoo_finance_pandas.get_option_chains(ticker='IBM')


# results
print option_calls_df.head()
print option_puts_df.head()
