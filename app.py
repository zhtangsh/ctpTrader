import datetime
import logging
from typing import List, Dict

import exchange_calendars as xcals
from dotenv import load_dotenv
from flask import Flask
from flask.json import JSONEncoder
from flask_jsonrpc import JSONRPC

from ctpApi.ctpmodel import *
from ctpApi.md import get_market_data
from ctpApi.td import get_trader
from utils import sys_utils


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime.date):
                return obj.isoformat()
            elif isinstance(obj, datetime.datetime):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


API_REF = {}
app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
jsonrpc = JSONRPC(app, "/api", enable_web_browsable_api=True)
load_dotenv()


@jsonrpc.method("accountInfo.getTradingAccount")
def get_account_info() -> List[CtpTradingAccount]:
    trader = get_trader()
    res = trader.query_account()
    return [CtpTradingAccount(r) for r in res]


@jsonrpc.method("tradeInfo.getOrderList")
def get_order_list() -> List[CtpOrder]:
    trader = get_trader()
    res = trader.query_order()
    return res


@jsonrpc.method("tradeInfo.getTradeList")
def get_stock_trades() -> List[CtpTrade]:
    trader = get_trader()
    res = trader.query_trade()
    return res


@jsonrpc.method("tradeInfo.getPositionList")
def get_position() -> List[CtpPosition]:
    trader = get_trader()
    res = trader.query_position()
    return res


@jsonrpc.method("trade.send_order")
def order_stock(
        symbol: str,
        exchange: str,
        price: float,
        volume: int,
        direction: str,
        offset: str,
        price_type: str
) -> str:
    trader = get_trader()
    res = trader.send_order(symbol, exchange, price, volume, direction, offset, price_type)
    return res


@jsonrpc.method("trade.cancel_order")
def cancel_order_stock(
        order_sys_id: str,
        exchange_id: str
) -> None:
    trader = get_trader()
    res = trader.cancel_order(order_sys_id, exchange_id)
    return res


@jsonrpc.method("data.live_tick_data")
def live_tick_data(
        symbol: str
) -> Dict[str, any]:
    market_data = get_market_data()
    data = market_data.live_tick_data(symbol)
    return data


@jsonrpc.method("utils.is_trading_day")
def is_trading_day() -> bool:
    xshg = xcals.get_calendar("XSHG")
    return xshg.is_session(datetime.date.today())


level = logging.INFO
sys_utils.logging_config(level=level)
logging.getLogger("ctpApi.td").setLevel(logging.DEBUG)
logging.getLogger("ctpApi.md").setLevel(logging.DEBUG)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
