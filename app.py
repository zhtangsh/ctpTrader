import logging

from flask import Flask
from flask_jsonrpc import JSONRPC

from core.ctpmodel import *
from utils import sys_utils
import datetime
from core.tester import TestTdApi
from dotenv import load_dotenv
from typing import List
from flask.json import JSONEncoder


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


def get_trader(code: str = 'td') -> TestTdApi:
    if code not in API_REF:
        td_server = sys_utils.get_env('CTP_TD_SERVER', 'tcp://180.168.146.187:10201')
        broker_id = sys_utils.get_env('CTP_BROKER_ID', '9999')
        user_id = sys_utils.get_env('CTP_USER_ID', '224850')
        password = sys_utils.get_env('CTP_PASSWORD', 'q9yvcbw7RuHv@Zs')
        auth_code = sys_utils.get_env('CTP_AUTH_CODE', '0000000000000000')
        app_id = sys_utils.get_env('CTP_APP_ID', 'simnow_client_test')
        td_api = TestTdApi(address=td_server, user_id=user_id, password=password, broker_id=broker_id,
                           auth_code=auth_code, app_id=app_id)
        td_api.connect()
        API_REF[code] = td_api
    return API_REF[code]


# @jsonrpc.method("accountInfo.getAccountStatus")
# def get_account_status() -> List[QmtAccountStatus]:
#     trader = get_trader()
#     res = trader.get_account_status()
#     return res
#
#
# @jsonrpc.method("accountInfo.getAccountInfo")
# def get_account_info() -> List[QmtAccountInfo]:
#     trader = get_trader()
#     res = trader.get_account_info()
#     return res
#
#
# @jsonrpc.method("accountInfo.getStockAsset")
# def get_stock_asset() -> QmtAsset:
#     trader = get_trader()
#     res = trader.get_stock_asset()
#     return res
#
#
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


# @jsonrpc.method("trade.orderStock")
# def order_stock(
#         stock_code: str,
#         order_type: int,
#         order_volume: int,
#         price_type: int,
#         price: float,
#         strategy_name: str,
#         order_remark: str
# ) -> int:
#     trader = get_trader()
#     res = trader.order_stock(stock_code, order_type, order_volume, price_type, price, strategy_name, order_remark)
#     return res
#
#
# @jsonrpc.method("trade.cancel_order_stock")
# def cancel_order_stock(
#         order_id: int
# ) -> int:
#     trader = get_trader()
#     res = trader.cancel_order_stock(order_id)
#     return res


if __name__ == '__main__':
    level = logging.INFO
    sys_utils.logging_config(level=level)
    app.run(host='0.0.0.0', port=5000)
