import datetime
import logging
from typing import List, Dict

import exchange_calendars as xcals
from flask import Flask
from flask.json import JSONEncoder
from flask_jsonrpc import JSONRPC

from ctpApi.md import get_market_data
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
appmd = Flask(__name__)
appmd.json_encoder = CustomJSONEncoder
jsonrpc = JSONRPC(appmd, "/api", enable_web_browsable_api=True)


@jsonrpc.method("data.live_tick_data")
def live_tick_data(
        symbol: str
) -> Dict[str, any]:
    market_data = get_market_data()
    data = market_data.live_tick_data(symbol)
    return data


@jsonrpc.method("data.live_tick_data_v2")
def live_tick_data_v2(
        symbol: List[str]
) -> Dict[str, any]:
    market_data = get_market_data()
    data = market_data.live_tick_data_v2(symbol)
    return data


@jsonrpc.method("utils.is_trading_day")
def is_trading_day() -> bool:
    xshg = xcals.get_calendar("XSHG")
    return xshg.is_session(datetime.date.today())


level = logging.INFO
sys_utils.logging_config(level=level)
logging.getLogger("ctpApi.md").setLevel(logging.DEBUG)
if __name__ == '__main__':
    appmd.run(host='0.0.0.0', port=8000)
