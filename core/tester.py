import logging
import time
from pathlib import Path
from threading import Event

# vnpy_ctp
from typing import List

from vnpy.trader.constant import Exchange
from vnpy.trader.object import SubscribeRequest
from vnpy_ctp.api import TdApi
from vnpy_ctp.api.ctp_constant import (THOST_FTDC_D_Buy, THOST_FTDC_D_Sell,
                                       THOST_FTDC_OF_Close,
                                       THOST_FTDC_OF_CloseToday,
                                       THOST_FTDC_OF_CloseYesterday,
                                       THOST_FTDC_OF_Open,
                                       THOST_FTDC_PD_Long,
                                       THOST_FTDC_PD_Short, THOST_FTDC_OPT_LimitPrice, THOST_FTDC_HF_Speculation,
                                       THOST_FTDC_CC_Immediately, THOST_FTDC_FCC_NotForceClose, THOST_FTDC_TC_GFD,
                                       THOST_FTDC_VC_AV, THOST_FTDC_AF_Delete)

from core.ctpmodel import *
from utils import sys_utils

logger = logging.getLogger(__name__)


class TestTdApi(TdApi):
    def __init__(self, address, user_id, password, broker_id, auth_code, app_id, group='ctptest',
                 initial_password='q9yvcbw7RuHv@Zs'):
        super().__init__()
        self.address: str = address
        self.user_id: str = user_id
        self.password: str = password
        self.broker_id: str = broker_id
        self.auth_code: str = auth_code
        self.app_id: str = app_id
        self.group = group
        self.name = 'td'
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
        self._initial_password = 'q9yvcbw7RuHv@Zs'

        self.req_id = 0  # 自增ID

    def connect(self) -> None:
        """
        连接服务器
        """

        if not self.connect_status:
            path: Path = sys_utils.get_folder_path(self.group.lower())
            self.initial_event = Event()
            self.createFtdcTraderApi(f"{str(path)}\\{self.name}")
            self.registerFront(self.address)
            self.init()
            self.initial_event.wait()
            self.connect_status = True
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

    def cancel_order(self, order_sys_id):
        ctp_req = {
            "BrokerID": self.broker_id,
            "InvestorID": self.user_id,
            "UserID": self.user_id,
            "ExchangeID": Exchange.CFFEX.name,
            "OrderSysID": order_sys_id,
            "ActionFlag": THOST_FTDC_AF_Delete,
        }
        req_id = self.get_req_id()
        self.reqOrderAction(ctp_req, req_id)
        # self.wait_event(req_id)

    def query_order(self) -> List[CtpOrder]:
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
        if self.auth_code:
            self.authenticate()
        else:
            self.login()

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

    def query_trade(self) -> List[CtpTrade]:
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


def print_position(p_list: List[CtpPosition]):
    for p in p_list:
        logger.info(f"position:symbol={p.instrument_id},position={p.position},direction={DIRE_MAP[p.posi_direction]}")


def print_trade(t_list: List[CtpTrade]):
    for t in t_list:
        logger.info(
            f"trade:order_id={t.order_sys_id},symbol={t.instrument_id},direction={DIRE_MAP[t.direction]},offset={OFFSET_MAP[t.offset_flag]},trade_time={t.trade_time}")


# 多空映射
DIRE_MAP = {
    THOST_FTDC_D_Sell: '做空',
    THOST_FTDC_D_Buy: '做多',
    THOST_FTDC_PD_Short: '空',
    THOST_FTDC_PD_Long: '多',
}

# 开平映射
OFFSET_MAP = {
    THOST_FTDC_OF_Close: '平',
    THOST_FTDC_OF_Open: '开',
    THOST_FTDC_OF_CloseYesterday: '平昨',
    THOST_FTDC_OF_CloseToday: '平今'
}


def test():
    TD_SERVER = 'tcp://180.168.146.187:10201'  # 交易服务器
    BROKER_ID = '9999'  # 经纪商代码
    USER_ID = '224850'
    PASSWORD = 'q9yvcbw7RuHv@Zs'
    APP_ID = 'simnow_client_test'
    AUTH_CODE = '0000000000000000'
    level = logging.INFO
    sys_utils.logging_config(level=level)
    td_api = TestTdApi(address=TD_SERVER, user_id=USER_ID, password=PASSWORD, broker_id=BROKER_ID, auth_code=AUTH_CODE,
                       app_id=APP_ID)
    td_api.connect()
    req_list = [
        SubscribeRequest('T2406', Exchange.CFFEX),
        SubscribeRequest('T2409', Exchange.CFFEX),
        SubscribeRequest('T2412', Exchange.CFFEX),
        # SubscribeRequest('TS2406', Exchange.CFFEX),
        # SubscribeRequest('TS2409', Exchange.CFFEX),
        # SubscribeRequest('TS2412', Exchange.CFFEX),
        # SubscribeRequest('TF2406', Exchange.CFFEX),
        # SubscribeRequest('TF2409', Exchange.CFFEX),
        # SubscribeRequest('TF2412', Exchange.CFFEX),
        # SubscribeRequest('IF2404', Exchange.CFFEX),
        # SubscribeRequest('IF2409', Exchange.CFFEX),
        # SubscribeRequest('IF2412', Exchange.CFFEX)
    ]
    res = td_api.query_position()
    logger.info(f"position:{res}")
    res = td_api.query_order()
    logger.info(f"order:{res}")
    for req in req_list:
        res = td_api.subscribe(req)
        logger.info(f"subscribe res:{res}")
        res1 = td_api.send_order(req.symbol, req.exchange.name, res['LowerLimitPrice'], 1, THOST_FTDC_D_Buy,
                                 THOST_FTDC_OF_Open)
        logger.info(f"res1:{res1}")
        td_api.cancel_order(res1)
        # res2 = td_api.send_order(req.symbol, req.exchange.name, res['BidPrice1'], 1, THOST_FTDC_D_Sell,
        #                          THOST_FTDC_OF_Open)
        # logger.info(f"res1:{res2}")
    res = td_api.query_order()
    logger.info(f"order:{res}")
    res = td_api.query_account()
    logger.info(f"account:{res}")
    res = td_api.query_trade()
    logger.info(f"trade:{res}")


def query_price(td_api):
    req_list = [
        SubscribeRequest('T2406', Exchange.CFFEX),
        SubscribeRequest('T2406', Exchange.CFFEX),
        SubscribeRequest('TS2409', Exchange.CFFEX),
        SubscribeRequest('TS2412', Exchange.CFFEX),
    ]
    for req in req_list:
        res = td_api.subscribe(req)
        logger.info(f"market_data:{res}")


def place_and_hold(td_api: TestTdApi, req_list, cancel=False):
    for req in req_list:
        res = td_api.subscribe(req)
        logger.info(f"subscribe res:{res}")
        res = td_api.send_order(req.symbol, req.exchange.name, res['BidPrice1'], 2, THOST_FTDC_D_Buy,
                                THOST_FTDC_OF_Open)
        if cancel:
            time.sleep(3)
            td_api.cancel_order(res)


def check_position(td_api: TestTdApi, close=False):
    position_list = td_api.query_position()
    print_position(position_list)
    if not close:
        return
    for p in position_list:
        if p.position > 0:
            req = SubscribeRequest(p.instrument_id, Exchange.CFFEX)
            res = td_api.subscribe(req)
            logger.info(f"subscribe res:{res}")
            if p.posi_direction == THOST_FTDC_PD_Long:
                td_api.send_order(p.instrument_id, p.exchange_id, res['BidPrice1'], p.position, THOST_FTDC_D_Sell,
                                  THOST_FTDC_OF_Close)
            else:
                td_api.send_order(p.instrument_id, p.exchange_id, res['BidPrice1'], p.position, THOST_FTDC_D_Buy,
                                  THOST_FTDC_OF_Close)


def test_dzqh():
    TD_SERVER = 'tcp://180.166.103.37:51215'  # 交易服务器
    BROKER_ID = '6666'  # 经纪商代码
    USER_ID = '66680162'
    PASSWORD = 'q9yvcbw7RuHv@Zs'
    APP_ID = 'client_dlzh0222_alpha'
    AUTH_CODE = 'SXEX6UAU35NPVAZY'
    level = logging.DEBUG
    sys_utils.logging_config(level=level)
    td_api = TestTdApi(address=TD_SERVER, user_id=USER_ID, password=PASSWORD, broker_id=BROKER_ID, auth_code=AUTH_CODE,
                       app_id=APP_ID)
    td_api.connect()
    req_list_1 = [
        SubscribeRequest('T2409', Exchange.CFFEX),
        SubscribeRequest('T2412', Exchange.CFFEX),
    ]
    req_list_2 = [
        SubscribeRequest('TS2409', Exchange.CFFEX),
        SubscribeRequest('TS2412', Exchange.CFFEX),
    ]
    # place_and_hold(td_api, req_list_1)
    # place_and_hold(td_api, req_list_2,cancel=True)
    # time.sleep(10)
    check_position(td_api, True)


"""
Exchange.SHFE
CU2406
CU2407
Exchange.DCE
I2409
I2501
"""

if __name__ == '__main__':
    test_dzqh()
