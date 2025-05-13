import concurrent
from concurrent.futures import ThreadPoolExecutor
from joblib import Parallel, delayed
import os
import pandas as pd
import datetime
import time
from loguru import logger
PRICE_TYPE = ['stock', 'index', 'future']
FREQUENCY_TYPE = ['daily', 'minute']
FQ_TYPE = ['pre', 'none', 'post']
ENGINE_TYPE = ['thread', 'loky']

def concurrent_read(files, base_path, process_fun, engine='thread'):
    file_list = [os.path.join(base_path, date) for date in files]
    results = []
    if engine == 'thread':
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(process_fun, file) for file in file_list}
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                # 处理每个future的结果，比如添加到results列表
                results.append(result)
    else:
        results = Parallel(n_jobs=int(os.cpu_count()/8))(delayed(process_fun)(file) for file in file_list)
    return pd.concat(results)

def parse_date(date_string):
    for fmt in ("%Y%m%d", "%Y-%m-%d"):
        try:
            # print(date_string)
            return datetime.datetime.strptime(date_string, fmt)
        except ValueError:
            # print(date_string)
            continue
    raise ValueError("No valid date format found")