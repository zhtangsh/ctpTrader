# from ctpApi.md_v2 import get_market_data
import pandas as pd

from ctpApi.md_v2 import get_market_data
from utils import sys_utils
from utils.datasource import DbEngineFactory
import time
import datetime
import logging

logger = logging.getLogger(__name__)

OPTION_CODE_CONFIG_LIST = [
    {
        'option_prefix': 'TSO',
        'future_prefix': 'TS',
        'price_step': 0.1,
        'price_limit': 0.5
    },
    {
        'option_prefix': 'TFO',
        'future_prefix': 'TF',
        'price_step': 0.25,
        'price_limit': 1.2
    },
    {
        'option_prefix': 'TTO',
        'future_prefix': 'T',
        'price_step': [0.25, 0.5, 0.5, 0.5],
        'price_limit': 2.0
    },
    {
        'option_prefix': 'TLO',
        'future_prefix': 'TL',
        'price_step': [0.5, 1, 1, 1],
        'price_limit': 3.5
    }
]


def parse_rq_contract(contract_list, underlying):
    res = []
    underlying_length = len(underlying)
    for contract in contract_list:
        p1 = contract[0:underlying_length]
        p2 = contract[underlying_length:underlying_length + 4]
        p3 = contract[underlying_length + 4:underlying_length + 5]
        p4 = contract[underlying_length + 5:]
        res.append(f"{p1}{p2}-{p3}-{p4}")
    return res


def add_month(cur: datetime.date, month_count=1):
    if cur.month < 12 - month_count + 1:
        return datetime.date(cur.year, cur.month + month_count, cur.day)
    return datetime.date(cur.year + 1, (cur.month + month_count) % 12, cur.day)


def next_quarter_month(cur: datetime.date):
    if cur.month == 12:
        return datetime.date(cur.year + 1, ((cur.month // 3 + 1) * 3) % 12, cur.day)
    return datetime.date(cur.year, (cur.month // 3 + 1) * 3, cur.day)


def underlying_month(cur: datetime.date):
    if cur.month % 3 == 0:
        return datetime.date(cur.year, cur.month, cur.day)
    return datetime.date(cur.year, (cur.month // 3 + 1) * 3, cur.day)


def build_contract_month_list():
    today = datetime.date.today()
    first_day_of_month = datetime.date(today.year, today.month, 1)
    first_day_weekday = first_day_of_month.isoweekday()
    kitten_day = datetime.date(today.year, today.month, 13 - (first_day_weekday % 7))
    if today > kitten_day:
        contract_date1 = add_month(first_day_of_month, month_count=2)
    else:
        contract_date1 = add_month(first_day_of_month, month_count=1)
    contract_date2 = add_month(contract_date1)
    contract_date3 = add_month(contract_date2)
    contract_date4 = next_quarter_month(contract_date3)
    return [contract_date1, contract_date2, contract_date3, contract_date4]


def build_price_list(settlement_price, price_step, price_limit):
    lowest_price = (settlement_price * (1 - price_limit / 100) // price_step - 1) * price_step
    highest_price = (settlement_price * (1 + price_limit / 100) // price_step + 1) * price_step
    return [lowest_price + i * price_step for i in range(int((highest_price - lowest_price) // price_step))]


def get_previous_settlement_price(underlying_code):
    sql = f"select * from metrics_day where order_book_id='{underlying_code}' order by date desc limit 1"
    engine = DbEngineFactory.engine_clickhouse_rqdata_future()
    df = pd.read_sql(sql, con=engine)
    return df['settlement'].iloc[0]


def build_option_code_list(option_prefix, future_prefix, price_step_list, price_limit):
    contract_month_list = build_contract_month_list()
    if not isinstance(price_step_list, list):
        price_step_list = [price_step_list for i in range(4)]
    res = []
    for i in range(4):
        month_date = contract_month_list[i]
        month = month_date.strftime("%Y%m")
        underlying_month_str = underlying_month(month_date).strftime("%y%m")
        underlying_code = f"{future_prefix}{underlying_month_str}"
        settlement_price = get_previous_settlement_price(underlying_code)
        price_step = price_step_list[i]
        price_list = build_price_list(settlement_price, price_step, price_limit)
        res.extend([f"{option_prefix}{month}-{dir}-{price:.2f}" for dir in ['C', 'P'] for price in price_list])
    return res


def get_option_code_list():
    res = []
    for option_code_config in OPTION_CODE_CONFIG_LIST:
        option_prefix = option_code_config['option_prefix']
        future_prefix = option_code_config['future_prefix']
        price_step = option_code_config['price_step']
        price_limit = option_code_config['price_limit']
        tmp = build_option_code_list(option_prefix, future_prefix, price_step, price_limit)
        res.extend(tmp)
    return res


def entrypoint():
    target_contract_list = get_option_code_list()
    logger.info(f"订阅的合约列表{target_contract_list}")
    md = get_market_data()
    for contract in target_contract_list:
        md.subscribe(contract)
    today = datetime.date.today()
    close_datetime = datetime.datetime(today.year, today.month, today.day, 15, 45)
    while True:
        now = datetime.datetime.now()
        if now > close_datetime:
            logger.info("收盘，推出程序")
            break
        time.sleep(100)


if __name__ == '__main__':
    sys_utils.logging_config()
    entrypoint()
