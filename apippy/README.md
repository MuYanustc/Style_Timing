# hashdatasdk

哈希数据sdk

# 数据结构
数据在180上 结构如下

base_dir = /mnt/data/hub/

## hub
- stock
    - stock_quote
        - adjust_factor  
        - forward_adjusted_daily  
        - unadjusted_daily
        - post_adjusted_daily
    - industry
    - market_cap_daily
    - turnover_daily
- index
    - daily_quote
    - idx_cons
- future
    - future_quote
        - daily_quote
- calendar
    - stock_holidays

index 里是指数数据
future 是期货数据
stock 是股票数据