import json
import logging
import time
from pathlib import Path
from threading import Event
# vnpy_ctp
from typing import List

from kafka import KafkaProducer
from vnpy.trader.object import SubscribeRequest
from vnpy_ctp.api import TdApi
from vnpy_ctp.api.ctp_constant import (THOST_FTDC_OPT_LimitPrice, THOST_FTDC_HF_Speculation,
                                       THOST_FTDC_CC_Immediately, THOST_FTDC_FCC_NotForceClose, THOST_FTDC_TC_GFD,
                                       THOST_FTDC_VC_AV, THOST_FTDC_AF_Delete)

from ctpApi.ctpmodel import *
from utils import sys_utils

logger = logging.getLogger(__name__)

CTP_TRADE_TOPIC = sys_utils.get_env('CTP_TRADE_TOPIC', 'ctpTradeTest00')
CTP_ORDER_TOPIC = sys_utils.get_env('CTP_ORDER_TOPIC', 'ctpOrderTest00')
API_REF = {}
EXIT_API_SET = set()

"""
常规流程
1. 初始化ctp
2. 连接交易服务器(onFrontConnected)
3. 验证auth code(reqAuthenticate)
4. 登陆帐户(reqUserLogin)
连接中断:
1. onFrontDisconnected，此时不能走：验证auth code-> 登陆帐户(reqUserLogin)的流程，需要重新初始化ctp，否则会报{'ErrorID': 7, 'ErrorMsg': 'CTP:还没有初始化'}
"""


class TestTdApi(TdApi):
    def __init__(self, address, user_id, password, broker_id, auth_code, app_id, kafka_client: KafkaProducer,
                 name='td', group='ctptest'):
        super().__init__()
        self.address: str = address
        self.user_id: str = user_id
        self.password: str = password
        self.broker_id: str = broker_id
        self.auth_code: str = auth_code
        self.app_id: str = app_id
        self.group = group
        self.name = name
        self.initialize_status: bool = False
        self.connect_status: bool = False
        self.auth_status: bool = False
        self.auth_failed: bool = False
        self.login_status: bool = False
        self.login_failed: bool = False
        self.req_cache = {}

        self.front_id: str = ""
        self.session_id: str = ""
        self.event_dict = {}
        self.initial_event = None
        self.disconnected_code = -1
        self._initial_password = 'q9yvcbw7RuHv@Zs'
        self.kafka_client = kafka_client

        self.req_id = 0  # 自增ID
        self.event_timeout = 60.0

    def connect(self) -> None:
        """
        连接服务器
        """

        if not self.connect_status:
            logger.debug("尝试连接到前置机")
            path: Path = sys_utils.get_folder_path(self.group.lower())
            self.initial_event = Event()
            logger.debug("尝试createFtdcTraderApi")
            self.createFtdcTraderApi(f"{str(path)}\\{self.name}")
            logger.debug("尝试registerFront")
            self.registerFront(self.address)
            logger.debug("尝试init")
            self.init()
            self.initialize_status = True
            logger.debug("等待连接信息")
            self.initial_event.wait(timeout=self.event_timeout)
        else:
            self.authenticate()

    def login(self) -> None:
        """用户登录"""
        if self.login_failed:
            logger.info("之前登陆失败，请检查代码")
            return

        ctp_req: dict = {
            "UserID": self.user_id,
            "Password": self.password,
            "BrokerID": self.broker_id
        }
        req_id = self.get_req_id()
        self.reqUserLogin(ctp_req, req_id)

    def update_password(self):
        ctp_req = {
            'BrokerID': self.broker_id,
            'UserID': self.user_id,
            'OldPassword': self.password,
            'NewPassword': self._initial_password
        }
        req_id = self.get_req_id()
        self.reqUserPasswordUpdate(ctp_req, req_id)

    def authenticate(self) -> None:
        """
        发起授权验证
        """
        if self.auth_failed:
            logger.info("之前授权验证失败，请检查代码")
            return

        ctp_req: dict = {
            "UserID": self.user_id,
            "BrokerID": self.broker_id,
            "AuthCode": self.auth_code,
            "AppID": self.app_id
        }
        req_id = self.get_req_id()
        logger.debug(f"authenticate:req={req_id}")
        self.reqAuthenticate(ctp_req, req_id)

    def subscribe(self, req: SubscribeRequest):
        logger.debug(f"subscribe:{req}")
        req_id = self.get_req_id()
        self.reqQryDepthMarketData({
            'InstrumentID': req.symbol,
            'ExchangeID': req.exchange.name,
        }, req_id)
        self.wait_event(req_id)
        return self.req_cache.get(req_id)

    def query_position(self) -> List[CtpPosition]:
        self.check_connection()
        req_id = self.get_req_id()
        self.reqQryInvestorPosition({}, req_id)
        self.wait_event(req_id)
        res = self.get_response(req_id)
        return [CtpPosition(r) for r in res]

    def onRspUserPasswordUpdate(self, data, error, reqid, last):
        logger.debug(f"onRspUserPasswordUpdate: data={data},error={error},reqid={reqid},last={last}")
        self.password = self._initial_password
        self.login()

    def onRspQryInvestorPosition(self, data, error, reqid, last):
        logger.debug(f"onRspQryInvestorPosition: data={data},error={error},reqid={reqid},last={last}")
        self.append_response(reqid, data)
        if last:
            self.set_event(reqid)

    def settlement_info_confirm(self):
        self.check_connection()
        ctp_req: dict = {
            "BrokerID": self.broker_id,
            "InvestorID": self.user_id
        }
        req_id = self.get_req_id()
        logger.debug("settlement_info_confirm")
        self.reqSettlementInfoConfirm(ctp_req, req_id)

    def send_order(
            self,
            symbol,
            exchange,
            price,
            volume,
            direction,
            offset
    ):
        """
        下单
        :param symbol: 合约
        :param exchange: 合约所属的交易所
        :param price: 价格
        :param volume: 数量
        :param direction: 方向
        :param offset: 开平
        :return:
        """
        self.check_connection()
        # 以下参数都是照着 vnpy 代码抄的
        req_id = self.get_req_id()
        ctp_req = {
            "InstrumentID": symbol,
            "ExchangeID": exchange,
            "LimitPrice": price,
            "VolumeTotalOriginal": volume,
            "OrderPriceType": THOST_FTDC_OPT_LimitPrice,
            "Direction": direction,
            "CombOffsetFlag": offset,
            "OrderRef": str(req_id),
            "InvestorID": self.user_id,
            "UserID": self.user_id,
            "BrokerID": self.broker_id,
            "CombHedgeFlag": THOST_FTDC_HF_Speculation,
            "ContingentCondition": THOST_FTDC_CC_Immediately,
            "ForceCloseReason": THOST_FTDC_FCC_NotForceClose,
            "IsAutoSuspend": 0,
            "TimeCondition": THOST_FTDC_TC_GFD,
            "VolumeCondition": THOST_FTDC_VC_AV,
            "MinVolume": 1
        }
        n: int = self.reqOrderInsert(ctp_req, req_id)
        logger.info(f"res={n}")
        self.wait_event(req_id)
        res = self.get_response(req_id)
        return res

    def cancel_order(self, order_sys_id, exchange_id):
        self.check_connection()
        ctp_req = {
            "BrokerID": self.broker_id,
            "InvestorID": self.user_id,
            "UserID": self.user_id,
            "ExchangeID": exchange_id,
            "OrderSysID": order_sys_id,
            "ActionFlag": THOST_FTDC_AF_Delete,
        }
        req_id = self.get_req_id()
        self.reqOrderAction(ctp_req, req_id)
        # self.wait_event(req_id)

    def query_order(self) -> List[CtpOrder]:
        self.check_connection()
        req_id = self.get_req_id()
        self.reqQryOrder({}, req_id)
        self.wait_event(req_id)
        res = self.get_response(req_id)
        return [CtpOrder(r) for r in res]

    def onRspQryOrder(self, data, error, reqid, last):
        logger.debug(f"onRspQryOrder: data={data},error={error},reqid={reqid},last={last}")
        self.append_response(reqid, data)
        if last:
            self.set_event(reqid)

    def query_account(self):
        self.check_connection()
        req_id = self.get_req_id()
        logger.debug(f"query_account:req_id={req_id}")
        self.reqQryTradingAccount({}, req_id)
        self.wait_event(req_id)
        res = self.get_response(req_id)
        return res

    def onRspQryTradingAccount(self, data, error, reqid, last):
        logger.debug(f"onRspQryTradingAccount: data={data},error={error},reqid={reqid},last={last}")
        self.append_response(reqid, data)
        if last:
            self.set_event(reqid)

    def onRspQryDepthMarketData(self, data, error, reqid, last):
        logger.debug(f"onRspQryDepthMarketData: data={data},error={error},reqid={reqid},last={last}")
        self.req_cache[reqid] = data
        self.set_event(reqid)

    def onFrontConnected(self) -> None:
        """
        交易服务器连接成功
        """
        logger.info(f"交易服务器连接成功:{self.address}")
        self.connect_status = True
        if self.initialize_status:
            logger.debug("ctp已初始化，尝试登陆")
            self.authenticate()

    def onFrontDisconnected(self, reason: int) -> None:
        """服务器连接断开回报"""
        logger.info(f"交易服务器连接断开,原因:{reason}")
        self.login_status = False
        self.connect_status = False
        self.initialize_status = False
        self.disconnected_code = reason
        EXIT_API_SET.add(self.name)

    def onRspAuthenticate(self, data: dict, error: dict, reqid: int, last: bool) -> None:
        """
        用户授权验证回报
        """
        logger.debug(f"onRspAuthenticate: data={data},error={error},reqid={reqid},last={last}")
        if not error['ErrorID']:
            self.auth_status = True
            logger.info("交易服务器授权验证成功")
            self.login()
        else:
            # 如果是授权码错误，则禁止再次发起认证
            if error['ErrorID'] == 63:
                self.auth_failed = True
            logger.info(f"交易服务器授权验证失败,error={error}")

    def onRspUserLogin(self, data: dict, error: dict, reqid: int, last: bool) -> None:
        """
        登陆请求回报
        """
        logger.debug(f"onRspUserLogin: data={data},error={error},reqid={reqid},last={last}")
        if not error["ErrorID"]:
            self.front_id = data["FrontID"]
            self.session_id = data["SessionID"]
            self.login_status = True
            logger.info(f"交易服务器登录成功,data={data},error={error}")

            # 自动确认结算单
            self.settlement_info_confirm()
        else:
            # CTP:首次登录必须修改密码，请修改密码后重新登录
            if error['ErrorID'] == 140:
                self.update_password()
                return
            self.login_failed = True
            logger.info(f"交易服务器登录失败,data={data},error={error}")

    def onRspSettlementInfoConfirm(self, data: dict, error: dict, reqid: int, last: bool) -> None:
        """
        确认结算单回报
        """
        logger.info(f"确认结算单回报: data={data}")
        logger.debug(f"onRspSettlementInfoConfirm: data={data},error={error},reqid={reqid},last={last}")
        if self.initial_event is not None:
            self.initial_event.set()

    def wait_event(self, req_id):
        logger.debug(f"wait_event,req_id={req_id},event_dict={self.event_dict}")
        event = Event()
        self.event_dict[str(req_id)] = event
        event.wait(timeout=self.event_timeout)

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
        return self.req_id

    def check_connection(self):
        if self.connect_status and not self.login_status:
            logger.info("check_connection - 连接到服务器，但是未登陆，尝试重新登陆")
            self.authenticate()
        if not self.connect_status:
            logger.info("check_connection - 未连接到服务器，重新连接")
            self.connect()

    def onRspError(self, error: dict, reqid: int, last: bool) -> None:
        """
        请求报错回报
        """
        logger.info(f"onRspError: 交易接口报错,error={error},reqid={reqid},last={last}")
        self.set_event(reqid)

    def onRspOrderInsert(self, data: dict, error: dict, reqid: int, last: bool) -> None:
        """
        委托下单回报
        """
        logger.info(f"onRspOrderInsert: data={data},error={error},reqid={reqid},last={last}")

    def onRspOrderAction(self, data: dict, error: dict, reqid: int, last: bool) -> None:
        """
        委托撤单失败回报
        """
        logger.info(f"onRspOrderAction: data={data},error={error},reqid={reqid},last={last}")

    # 订单状态改变回调
    def onRtnOrder(self, data):
        logger.info(f"onRtnOrder:data={data}")
        # 只管当前 SessionID 的单子
        if data['SessionID'] == self.session_id and data['OrderSysID']:
            req_id = data['OrderRef']
            order_sys_id = data["OrderSysID"]
            self.set_response(req_id, order_sys_id)
            self.set_event(req_id)
        self.kafka_client.send(CTP_ORDER_TOPIC, data)

    def onRtnTrade(self, data: dict) -> None:
        """成交数据推送"""
        logger.info(f"onRtnTrade:data={data}")
        self.kafka_client.send(CTP_TRADE_TOPIC, data)

    def query_trade(self) -> List[CtpTrade]:
        self.check_connection()
        req_id = self.get_req_id()
        self.reqQryTrade({}, req_id)
        self.wait_event(req_id)
        res = self.get_response(req_id)
        return [CtpTrade(r) for r in res]

    def onRspQryTrade(self, data, error, reqid, last):
        logger.debug(f"onRspQryTrade: data={data},error={error},reqid={reqid},last={last}")
        self.append_response(reqid, data)
        if last:
            self.set_event(reqid)


def get_trader(code: str = 'td') -> TestTdApi:
    if code in EXIT_API_SET:
        logger.info(f"{code}属于待退出状态")
        EXIT_API_SET.remove(code)
        api = API_REF.pop(code)
        logger.info(f"{code}运行exit")
        ok = api.exit()
        logger.info(f"{code} exit运行结果:{ok}")
    if code not in API_REF:
        logger.info("构建td api")
        td_server = sys_utils.get_env('CTP_TD_SERVER', 'tcp://180.168.146.187:10201')
        broker_id = sys_utils.get_env('CTP_BROKER_ID', '9999')
        user_id = sys_utils.get_env('CTP_USER_ID', '224850')
        password = sys_utils.get_env('CTP_PASSWORD', 'q9yvcbw7RuHv@Zs')
        auth_code = sys_utils.get_env('CTP_AUTH_CODE', '0000000000000000')
        app_id = sys_utils.get_env('CTP_APP_ID', 'simnow_client_test')
        kafka_url = sys_utils.get_env('KAFKA_URL', '192.168.1.60:9092')
        producer = KafkaProducer(bootstrap_servers=kafka_url, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        td_api = TestTdApi(address=td_server, user_id=user_id, password=password, broker_id=broker_id,
                           auth_code=auth_code, app_id=app_id, kafka_client=producer, name=code)
        td_api.connect()
        API_REF[code] = td_api
    return API_REF[code]
