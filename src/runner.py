# use yfinance to download daily fc prices for GBPUSD=
from datetime import datetime
import yfinance as yf

def get_fx_data():
    # download daily data for GBPUSD
    data = yf.download('GBPUSD=X', start='2020-01-01', end='2021-01-01')
    # data.to_csv('data/fx_data.csv')
    return data

if __name__ == '__main__':
    fx_data = get_fx_data()