from .utils import *
import os
import datetime
import pandas as pd
from loguru import logger

def get_price(securitys=None, type='stock', start_date=None, end_date=None, frequency='daily', fields=None, fq='pre', engine='thread'):
    assert type in PRICE_TYPE, f'type must be in {PRICE_TYPE}'
    assert engine in ENGINE_TYPE, f'engine must be in {ENGINE_TYPE}'
    base_path = ""
    if type == 'stock':
        assert frequency in FREQUENCY_TYPE, f'frequency must be in {FREQUENCY_TYPE}'
        assert fq in FQ_TYPE, f'fq must be in {FQ_TYPE}'
        if fq == 'none':
            base_path = '/mnt/data/hub/stock/stock_quote/unadjusted_daily'
        if fq == 'pre':
           base_path = '/mnt/data/hub/stock/stock_quote/forward_adjusted_daily'
        if fq == 'post':
            base_path = '/mnt/data/hub/stock/stock_quote/post_adjusted_daily'
    elif type == 'index':
        base_path = '/mnt/data/hub/index/daily_quote'
    elif type == 'future':
        base_path = '/mnt/data/hub/future/future_quote/daily_quote'
    
    date_list = os.listdir(base_path)
    date_list = sorted([x.split('.')[0] for x in date_list])
    start_date = parse_date(start_date).strftime('%Y-%m-%d')
    end_date = parse_date(end_date).strftime('%Y-%m-%d')
    date_list = [x for x in date_list if x >= start_date and x <= end_date]
    def fun(path):
        df = pd.read_csv(path+'.csv')
        df.sort_values('order_book_id', inplace=True)
        return df
    res = concurrent_read(date_list, base_path, fun, engine=engine)
    
    # assert security 和 fields 为 list或者None
    assert (isinstance(securitys, list) or securitys is None) and (isinstance(fields, list) or fields is None), "securitys and fields must be list or None"
    if securitys is not None:
        res = res[res['order_book_id'].isin(securitys)]
    
    if fields is not None:
        res = res[['date', 'order_book_id'] + fields]
    
    res.reset_index(drop=True, inplace=True)
    return res
