from ctpApi.md import get_market_data
from utils import sys_utils
import time
import datetime


def fetch_contract_list(underlying, maturity):
    import rqdatac as rq
    today = datetime.date.today() - datetime.timedelta(days=1)
    rq.init()
    return rq.options.get_contracts(underlying=underlying, maturity=maturity, trading_date=today.strftime('%Y%m%d'))


def parse_rq_contract(contract_list):
    res = []
    for contract in contract_list:
        p1 = contract[0:2]
        p2 = contract[2:6]
        p3 = contract[6:7]
        p4 = contract[7:]
        res.append(f"{p1}{p2}-{p3}-{p4}")
    return res


def entrypoint():
    underlying = 'IO'
    maturity = '2409'
    rq_contract_list = fetch_contract_list(underlying=underlying, maturity=maturity)
    contract_list = parse_rq_contract(rq_contract_list)
    md = get_market_data()
    for contract in contract_list:
        md.subscribe(contract)
    while True:
        time.sleep(100)


if __name__ == '__main__':
    sys_utils.logging_config()
    entrypoint()
