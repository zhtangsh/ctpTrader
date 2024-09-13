from ctpApi.md_v2 import get_market_data
from utils import sys_utils
import time
import datetime
import json
import logging

logger = logging.getLogger(__name__)


def fetch_contract_list(underlying, maturity):
    import rqdatac as rq
    today = datetime.date.today() - datetime.timedelta(days=1)
    rq.init()
    return rq.options.get_contracts(underlying=underlying, maturity=maturity, trading_date=today.strftime('%Y%m%d'))


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


def entrypoint():
    # underlying_list_str = sys_utils.get_env('UNDERLYING_LIST', '["IO","HO"]')
    # maturity_list_str = sys_utils.get_env('MATURITY_LIST', '["2409","2410","2411"]')
    # underlying_list = json.loads(underlying_list_str)
    # maturity_list = json.loads(maturity_list_str)
    # target_contract_list = []
    # for underlying in underlying_list:
    #     for maturity in maturity_list:
    #         rq_contract_list = fetch_contract_list(underlying=underlying, maturity=maturity)
    #         contract_list = parse_rq_contract(rq_contract_list, underlying)
    #         target_contract_list.extend(contract_list)
    target_contract_list = []
    t_2411 = [f"TTO2411-{dir}-{100 + 0.25 * price:.2f}" for dir in ['C', 'P'] for price in range(50)]
    t_2412 = [f"TTO2412-{dir}-{100 + 0.5 * price:.2f}" for dir in ['C', 'P'] for price in range(30)]
    t_2501 = [f"TTO2501-{dir}-{100 + 0.5 * price:.2f}" for dir in ['C', 'P'] for price in range(30)]
    t_2503 = [f"TTO2503-{dir}-{100 + 0.5 * price:.2f}" for dir in ['C', 'P'] for price in range(30)]
    ts_2411 = [f"TSO2411-{dir}-{100 + 0.1 * price:.2f}" for dir in ['C', 'P'] for price in range(40)]
    ts_2412 = [f"TSO2412-{dir}-{100 + 0.1 * price:.2f}" for dir in ['C', 'P'] for price in range(40)]
    ts_2501 = [f"TSO2501-{dir}-{100 + 0.1 * price:.2f}" for dir in ['C', 'P'] for price in range(40)]
    ts_2503 = [f"TSO2503-{dir}-{100 + 0.1 * price:.2f}" for dir in ['C', 'P'] for price in range(40)]
    tf_2411 = [f"TFO2411-{dir}-{100 + 0.25 * price:.2f}" for dir in ['C', 'P'] for price in range(50)]
    tf_2412 = [f"TFO2412-{dir}-{100 + 0.25 * price:.2f}" for dir in ['C', 'P'] for price in range(50)]
    tf_2501 = [f"TFO2501-{dir}-{100 + 0.25 * price:.2f}" for dir in ['C', 'P'] for price in range(50)]
    tf_2503 = [f"TFO2503-{dir}-{100 + 0.25 * price:.2f}" for dir in ['C', 'P'] for price in range(50)]

    tl_2411 = [f"TLO2411-{dir}-{100 + 0.5 * price:.2f}" for dir in ['C', 'P'] for price in range(50)]
    tl_2412 = [f"TLO2412-{dir}-{100 + 1 * price:.2f}" for dir in ['C', 'P'] for price in range(30)]
    tl_2501 = [f"TLO2501-{dir}-{100 + 1 * price:.2f}" for dir in ['C', 'P'] for price in range(30)]
    tl_2503 = [f"TLO2503-{dir}-{100 + 1 * price:.2f}" for dir in ['C', 'P'] for price in range(30)]

    target_contract_list.extend(t_2411)
    target_contract_list.extend(t_2412)
    target_contract_list.extend(t_2501)
    target_contract_list.extend(t_2503)

    target_contract_list.extend(ts_2411)
    target_contract_list.extend(ts_2412)
    target_contract_list.extend(ts_2501)
    target_contract_list.extend(ts_2503)

    target_contract_list.extend(tf_2411)
    target_contract_list.extend(tf_2412)
    target_contract_list.extend(tf_2501)
    target_contract_list.extend(tf_2503)

    target_contract_list.extend(tl_2411)
    target_contract_list.extend(tl_2412)
    target_contract_list.extend(tl_2501)
    target_contract_list.extend(tl_2503)

    # target_contract_list = ['TTO2411-C-105.00', 'TTO2411-P-105.00']
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
