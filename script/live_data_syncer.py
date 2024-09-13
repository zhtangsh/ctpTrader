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
    # target_contract_list = [f"TTO2411-{dir}-{105 + 0.25 * price}" for dir in ['C', 'P'] for price in range(10)]
    target_contract_list = ['TTO2411-C-105', 'TTO2411-P-105', 'TTO2411-C-106', 'TTO2411-P-106']
    logger.info(f"订阅的合约列表{target_contract_list}")
    md = get_market_data()
    for contract in target_contract_list:
        md.subscribe(contract)
    while True:
        time.sleep(100)


if __name__ == '__main__':
    sys_utils.logging_config(logging.DEBUG)
    entrypoint()
