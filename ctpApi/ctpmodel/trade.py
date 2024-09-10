from dataclasses import dataclass


@dataclass
class CtpTrade:
    """
    ///成交
    struct CThostFtdcTradeField
    {
        ///经纪公司代码
        TThostFtdcBrokerIDType	BrokerID;
        ///投资者代码
        TThostFtdcInvestorIDType	InvestorID;
        ///保留的无效字段
        TThostFtdcOldInstrumentIDType	reserve1;
        ///报单引用
        TThostFtdcOrderRefType	OrderRef;
        ///用户代码
        TThostFtdcUserIDType	UserID;
        ///交易所代码
        TThostFtdcExchangeIDType	ExchangeID;
        ///成交编号
        TThostFtdcTradeIDType	TradeID;
        ///买卖方向
        TThostFtdcDirectionType	Direction;
        ///报单编号
        TThostFtdcOrderSysIDType	OrderSysID;
        ///会员代码
        TThostFtdcParticipantIDType	ParticipantID;
        ///客户代码
        TThostFtdcClientIDType	ClientID;
        ///交易角色
        TThostFtdcTradingRoleType	TradingRole;
        ///保留的无效字段
        TThostFtdcOldExchangeInstIDType	reserve2;
        ///开平标志
        TThostFtdcOffsetFlagType	OffsetFlag;
        ///投机套保标志
        TThostFtdcHedgeFlagType	HedgeFlag;
        ///价格
        TThostFtdcPriceType	Price;
        ///数量
        TThostFtdcVolumeType	Volume;
        ///成交时期
        TThostFtdcDateType	TradeDate;
        ///成交时间
        TThostFtdcTimeType	TradeTime;
        ///成交类型
        TThostFtdcTradeTypeType	TradeType;
        ///成交价来源
        TThostFtdcPriceSourceType	PriceSource;
        ///交易所交易员代码
        TThostFtdcTraderIDType	TraderID;
        ///本地报单编号
        TThostFtdcOrderLocalIDType	OrderLocalID;
        ///结算会员编号
        TThostFtdcParticipantIDType	ClearingPartID;
        ///业务单元
        TThostFtdcBusinessUnitType	BusinessUnit;
        ///序号
        TThostFtdcSequenceNoType	SequenceNo;
        ///交易日
        TThostFtdcDateType	TradingDay;
        ///结算编号
        TThostFtdcSettlementIDType	SettlementID;
        ///经纪公司报单编号
        TThostFtdcSequenceNoType	BrokerOrderSeq;
        ///成交来源
        TThostFtdcTradeSourceType	TradeSource;
        ///投资单元代码
        TThostFtdcInvestUnitIDType	InvestUnitID;
        ///合约代码
        TThostFtdcInstrumentIDType	InstrumentID;
        ///合约在交易所的代码
        TThostFtdcExchangeInstIDType	ExchangeInstID;
    };
    """
    # 经纪公司代码
    broker_id: str
    # 投资者代码
    investor_id: str
    # 保留的无效字段
    reserve1: str
    # 报单引用
    order_ref: str
    # 用户代码
    user_id: str
    # 交易所代码
    exchange_id: str
    # 成交编号
    trade_id: str
    # 买卖方向
    direction: str
    # 报单编号
    order_sys_id: str
    # 会员代码
    participant_id: str
    # 客户代码
    client_id: str
    # 交易角色
    trading_role: str
    # 保留的无效字段
    reserve2: str
    # 开平标志
    offset_flag: str
    # 投机套保标志
    hedge_flag: str
    # 价格
    price: str
    # 数量
    volume: str
    # 成交时期
    trade_date: str
    # 成交时间
    trade_time: str
    # 成交类型
    trade_type: str
    # 成交价来源
    price_source: str
    # 交易所交易员代码
    trader_id: str
    # 本地报单编号
    order_local_id: str
    # 结算会员编号
    clearing_part_id: str
    # 业务单元
    business_unit: str
    # 序号
    sequence_no: str
    # 交易日
    trading_day: str
    # 结算编号
    settlement_id: str
    # 经纪公司报单编号
    broker_order_seq: str
    # 成交来源
    trade_source: str
    # 投资单元代码
    invest_unit_id: str
    # 合约代码
    instrument_id: str
    # 合约在交易所的代码
    exchange_inst_id: str

    def __init__(self, o):
        self.broker_id = o.get('BrokerID')
        self.investor_id = o.get('InvestorID')
        self.reserve1 = o.get('reserve1')
        self.order_ref = o.get('OrderRef')
        self.user_id = o.get('UserID')
        self.exchange_id = o.get('ExchangeID')
        self.trade_id = o.get('TradeID')
        self.direction = o.get('Direction')
        self.order_sys_id = o.get('OrderSysID')
        self.participant_id = o.get('ParticipantID')
        self.client_id = o.get('ClientID')
        self.trading_role = o.get('TradingRole')
        self.reserve2 = o.get('reserve2')
        self.offset_flag = o.get('OffsetFlag')
        self.hedge_flag = o.get('HedgeFlag')
        self.price = o.get('Price')
        self.volume = o.get('Volume')
        self.trade_date = o.get('TradeDate')
        self.trade_time = o.get('TradeTime')
        self.trade_type = o.get('TradeType')
        self.price_source = o.get('PriceSource')
        self.trader_id = o.get('TraderID')
        self.order_local_id = o.get('OrderLocalID')
        self.clearing_part_id = o.get('ClearingPartID')
        self.business_unit = o.get('BusinessUnit')
        self.sequence_no = o.get('SequenceNo')
        self.trading_day = o.get('TradingDay')
        self.settlement_id = o.get('SettlementID')
        self.broker_order_seq = o.get('BrokerOrderSeq')
        self.trade_source = o.get('TradeSource')
        self.invest_unit_id = o.get('InvestUnitID')
        self.instrument_id = o.get('InstrumentID')
        self.exchange_inst_id = o.get('ExchangeInstID')


if __name__ == '__main__':
    t = CtpTrade({})
    print(t)
