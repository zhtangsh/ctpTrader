import logging
import json

from flask import Flask
from flask_jsonrpc import JSONRPC
from kafka import KafkaProducer
import redis

from core.ctpmodel import *
from utils import sys_utils
import datetime
from core.td import TestTdApi
from core.md import TestMdApi
from dotenv import load_dotenv
from typing import List, Dict
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
        kafka_url = sys_utils.get_env('KAFKA_URL', '192.168.1.60:9092')
        producer = KafkaProducer(bootstrap_servers=kafka_url, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        td_api = TestTdApi(address=td_server, user_id=user_id, password=password, broker_id=broker_id,
                           auth_code=auth_code, app_id=app_id, kafka_client=producer)
        td_api.connect()
        API_REF[code] = td_api
    return API_REF[code]


def get_market_data(code: str = 'md') -> TestMdApi:
    if code not in API_REF:
        md_server = sys_utils.get_env('CTP_MD_SERVER', 'tcp://180.168.146.187:10211')
        broker_id = sys_utils.get_env('CTP_BROKER_ID', '9999')
        user_id = sys_utils.get_env('CTP_USER_ID', '224850')
        password = sys_utils.get_env('CTP_PASSWORD', 'q9yvcbw7RuHv@Zs')
        auth_code = sys_utils.get_env('CTP_AUTH_CODE', '0000000000000000')
        app_id = sys_utils.get_env('CTP_APP_ID', 'simnow_client_test')
        redis_host = sys_utils.get_env('REDIS_HOST', '192.168.1.60')
        redis_port = sys_utils.get_env('REDIS_PORT', '16379')
        redis_client = redis.StrictRedis(
            host=redis_host,
            port=int(redis_port),
            db=0,
            password=None,
            encoding='utf-8',
            decode_responses=True
        )
        md_api = TestMdApi(address=md_server, user_id=user_id, password=password, broker_id=broker_id,
                           auth_code=auth_code, app_id=app_id, redis_client=redis_client)
        md_api.connect()
        API_REF[code] = md_api
    return API_REF[code]


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
        offset: str
) -> str:
    trader = get_trader()
    res = trader.send_order(symbol, exchange, price, volume, direction, offset)
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


if __name__ == '__main__':
    level = logging.INFO
    sys_utils.logging_config(level=level)
    app.run(host='0.0.0.0', port=5000)
