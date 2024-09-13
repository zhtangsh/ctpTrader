import json
import logging
from pathlib import Path
from threading import Event

import redis
from vnpy_ctptest.api import MdApi

from utils import sys_utils
from kafka import KafkaProducer

# vnpy_ctp

logger = logging.getLogger(__name__)

API_REF = {}
EXIT_API_SET = set()
CTP_LIVE_TICK_TOPIC = sys_utils.get_env('CTP_LIVE_TICK_TOPIC', 'ctpLiveTickTest')


class TickDataSyncerMdApi(MdApi):
    def __init__(self, address, user_id, password, broker_id, auth_code, app_id, redis_client: redis.StrictRedis = None,
                 name='md', group='ctptest', persist_type='redis', kafka_client: KafkaProducer = None):
        super().__init__()
        self.address: str = address
        self.user_id: str = user_id
        self.password: str = password
        self.broker_id: str = broker_id
        self.auth_code: str = auth_code
        self.app_id: str = app_id
        self.group = group
        self.name = name
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
        self.persist_type = persist_type
        self.kafka_client = kafka_client

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

    def maintain_subscription(self):
        for symbol in self.subscribe_set:
            self.subscribeMarketData(symbol)

    def subscribe(self, symbol) -> None:
        """
        订阅行情
        """
        if not self.login_status:
            return
        if symbol not in self.subscribe_set:
            logger.info(f"{symbol}不在订阅集合中，调用接口进行订阅")
            self.subscribeMarketData(symbol)
            self.subscribe_set.add(symbol)

    def onFrontConnected(self) -> None:
        """
        服务器连接成功回报
        """
        logger.info("行情服务器连接成功")
        self.login()
        self.maintain_subscription()

    def onFrontDisconnected(self, reason: int) -> None:
        """服务器连接断开回报"""
        logger.info(f"行情服务器连接断开，原因{reason}")
        self.login_status = False
        EXIT_API_SET.add(self.name)

    def onRspUserLogin(self, data: dict, error: dict, reqid: int, last: bool) -> None:
        """
        用户登录请求回报
        """
        if not error["ErrorID"]:
            self.login_status = True
            self.connect_status = True
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
        logger.info(f"行情服务器连接成功:{self.address}")
        self.login()

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

    def check_connection(self):
        if not self.connect_status:
            logger.info("check_connection - 未连接到服务器，重新连接")
            self.connect()

    def get_req_id(self):
        self.req_id += 1
        logger.debug(f"get_req_id,req_id={self.req_id}")
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
        logger.debug(f"onRtnDepthMarketData:数据{data}")
        if key is None:
            logger.info(f"行情数据有误,内容:{data}")
            return
        logging.debug(f"persist_type={self.persist_type}")
        if self.persist_type == 'redis':
            self.redis_client.set(key, json.dumps(data))
        elif self.persist_type == 'kafka':
            logging.debug(f"send to kafka:topic:{CTP_LIVE_TICK_TOPIC},data:{data}")
            self.kafka_client.send(CTP_LIVE_TICK_TOPIC, data)


def get_market_data(code: str = 'md') -> TickDataSyncerMdApi:
    if code in EXIT_API_SET:
        logger.info(f"{code}属于待退出状态")
        EXIT_API_SET.remove(code)
        api = API_REF.pop(code)
        logger.info(f"{code}运行exit")
        ok = api.exit()
        logger.info(f"{code} exit运行结果:{ok}")
    if code not in API_REF:
        md_server = sys_utils.get_env('CTP_MD_SERVER', 'tcp://180.166.103.37:51218')
        broker_id = sys_utils.get_env('CTP_BROKER_ID', '6666')
        user_id = sys_utils.get_env('CTP_USER_ID', '66680162')
        password = sys_utils.get_env('CTP_PASSWORD', 'q9yvcbw7RuHv@Zs')
        auth_code = sys_utils.get_env('CTP_AUTH_CODE', 'SXEX6UAU35NPVAZY')
        app_id = sys_utils.get_env('CTP_APP_ID', 'client_dlzh0222_alpha')
        persist_type = sys_utils.get_env('PERSIST_TYPE', 'kafka')
        redis_client = None
        kafka_client = None
        if persist_type == 'redis':
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
        elif persist_type == 'kafka':
            kafka_url = sys_utils.get_env('KAFKA_URL', '192.168.1.60:9092')
            kafka_client = KafkaProducer(bootstrap_servers=kafka_url,
                                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        md_api = TickDataSyncerMdApi(address=md_server, user_id=user_id, password=password, broker_id=broker_id,
                                     auth_code=auth_code, app_id=app_id, persist_type=persist_type,
                                     redis_client=redis_client, kafka_client=kafka_client, name=code)
        md_api.connect()
        API_REF[code] = md_api
    return API_REF[code]
