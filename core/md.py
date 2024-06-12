import logging
import time
from pathlib import Path
from threading import Event

from redis import StrictRedis

from vnpy_ctp.api import MdApi
import json

from utils import sys_utils

# vnpy_ctp

logger = logging.getLogger(__name__)


class TestMdApi(MdApi):
    def __init__(self, address, user_id, password, broker_id, auth_code, app_id, redis_client: StrictRedis,
                 group='ctptest'):
        super().__init__()
        self.address: str = address
        self.user_id: str = user_id
        self.password: str = password
        self.broker_id: str = broker_id
        self.auth_code: str = auth_code
        self.app_id: str = app_id
        self.group = group
        self.name = 'md'
        self.connect_status: bool = False
        self.auth_status: bool = False
        self.auth_failed: bool = False
        self.login_status: bool = False
        self.login_failed: bool = False
        self.req_cache = {}

        self.front_id: str = ""
        self.session_id: str = ""
        self.event_dict = {}
        self.subscribe_event_dict = {}
        self.initial_event = None
        self.subscribe_set = set()

        self.req_id = 0  # 自增ID
        self.redis_client = redis_client

    def connect(self) -> None:
        """
        连接服务器
        """
        if not self.connect_status:
            path: Path = sys_utils.get_folder_path(self.group.lower())
            self.initial_event = Event()
            self.createFtdcMdApi(f"{str(path)}\\{self.name}")
            self.registerFront(self.address)
            self.init()
            self.initial_event.wait()
            self.connect_status = True

    def login(self) -> None:
        """用户登录"""
        ctp_req: dict = {
            "UserID": self.user_id,
            "Password": self.password,
            "BrokerID": self.broker_id
        }

        req_id = self.get_req_id()
        logger.info(f"login:{ctp_req}")
        self.reqUserLogin(ctp_req, req_id)

    def subscribe(self, symbol) -> None:
        """
        订阅行情
        """
        if not self.login_status:
            return
        if symbol not in self.subscribe_set:
            self.subscribeMarketData(symbol)
            self.subscribe_set.add(symbol)
            self.wait_subscribe_event(symbol)

    def live_tick_data(self, symbol):
        self.subscribe(symbol)
        value = self.redis_client.get(symbol)
        logger.info(f"data:{value}")
        return json.loads(value)

    def onFrontConnected(self) -> None:
        """
        服务器连接成功回报
        """
        logger.info("行情服务器连接成功")
        self.login()

    def onFrontDisconnected(self, reason: int) -> None:
        """服务器连接断开回报"""
        logger.info(f"行情服务器连接断开，原因{reason}")
        self.login_status = False

    def onRspUserLogin(self, data: dict, error: dict, reqid: int, last: bool) -> None:
        """
        用户登录请求回报
        """
        if not error["ErrorID"]:
            self.login_status = True
            logger.info(f"行情服务器登录成功,data={data},reqid={reqid},error={error},last={last}")
        else:
            logger.info(f"行情服务器登录失败,error={error}")
        self.initial_event.set()

    def onRspQryDepthMarketData(self, data, error, reqid, last):
        logger.debug(f"onRspQryDepthMarketData: data={data},error={error},reqid={reqid},last={last}")
        self.req_cache[reqid] = data
        self.set_event(reqid)

    def onFrontConnected(self) -> None:
        """
        交易服务器连接成功
        """
        logger.info(f"交易服务器连接成功:{self.address}")
        self.login()

    def wait_subscribe_event(self, symbol):
        logger.debug(f"wait_subscribe_event,symbol={symbol},event_dict={self.subscribe_event_dict}")
        event = Event()
        self.subscribe_event_dict[symbol] = event
        event.wait()

    def set_subscribe_event(self, symbol):
        logger.debug(f"set_subscribe_event:symbol={symbol},event_dict={self.subscribe_event_dict}")
        if symbol not in self.subscribe_event_dict:
            return
        event = self.subscribe_event_dict.pop(symbol)
        if event is not None:
            event.set()

    def wait_event(self, req_id):
        logger.debug(f"wait_event,req_id={req_id},event_dict={self.event_dict}")
        event = Event()
        self.event_dict[str(req_id)] = event
        event.wait()

    def set_event(self, req_id):
        logger.debug(f"set_event:{req_id},event_dict={self.event_dict}")
        if str(req_id) not in self.event_dict:
            return
        event = self.event_dict.pop(str(req_id))
        if event is not None:
            event.set()

    def set_response(self, req_id, data):
        self.req_cache[str(req_id)] = data

    def append_response(self, req_id, data):
        res_list = self.req_cache.get(str(req_id))
        if res_list is None:
            res_list = []
            self.req_cache[str(req_id)] = res_list
        if data:
            res_list.append(data)

    def get_response(self, req_id):
        if str(req_id) not in self.req_cache:
            return None
        return self.req_cache.pop(str(req_id))

    def get_req_id(self):
        self.req_id += 1
        logger.debug(f"get_req_id,req_id={self.req_id}")
        time.sleep(0.1)
        return self.req_id

    def onRspError(self, error: dict, reqid: int, last: bool) -> None:
        """
        请求报错回报
        """
        logger.info(f"onRspError: 交易接口报错,error={error},reqid={reqid},last={last}")
        self.set_event(reqid)

    def onRspSubMarketData(self, data: dict, error: dict, reqid: int, last: bool) -> None:
        """
        订阅行情回报
        """
        logger.info(f"onRspSubMarketData: 订阅行情回报,error={error},data={data},reqid={reqid},last={last}")
        if not error or not error["ErrorID"]:
            return
        else:
            logger.info(f"onRspSubMarketData: 行情订阅失败{error}")

    def onRtnDepthMarketData(self, data: dict) -> None:
        """
        深度行情通知
        """
        key = data.get('InstrumentID')
        if key is None:
            logger.info(f"行情数据有误,内容:{data}")
            return
        self.redis_client.set(key, json.dumps(data))
        self.set_subscribe_event(key)
