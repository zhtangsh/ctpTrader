from dataclasses import dataclass


@dataclass
class CtpOrder:
    """
    ///报单
    struct CThostFtdcOrderField
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
        ///报单价格条件
        TThostFtdcOrderPriceTypeType	OrderPriceType;
        ///买卖方向
        TThostFtdcDirectionType	Direction;
        ///组合开平标志
        TThostFtdcCombOffsetFlagType	CombOffsetFlag;
        ///组合投机套保标志
        TThostFtdcCombHedgeFlagType	CombHedgeFlag;
        ///价格
        TThostFtdcPriceType	LimitPrice;
        ///数量
        TThostFtdcVolumeType	VolumeTotalOriginal;
        ///有效期类型
        TThostFtdcTimeConditionType	TimeCondition;
        ///GTD日期
        TThostFtdcDateType	GTDDate;
        ///成交量类型
        TThostFtdcVolumeConditionType	VolumeCondition;
        ///最小成交量
        TThostFtdcVolumeType	MinVolume;
        ///触发条件
        TThostFtdcContingentConditionType	ContingentCondition;
        ///止损价
        TThostFtdcPriceType	StopPrice;
        ///强平原因
        TThostFtdcForceCloseReasonType	ForceCloseReason;
        ///自动挂起标志
        TThostFtdcBoolType	IsAutoSuspend;
        ///业务单元
        TThostFtdcBusinessUnitType	BusinessUnit;
        ///请求编号
        TThostFtdcRequestIDType	RequestID;
        ///本地报单编号
        TThostFtdcOrderLocalIDType	OrderLocalID;
        ///交易所代码
        TThostFtdcExchangeIDType	ExchangeID;
        ///会员代码
        TThostFtdcParticipantIDType	ParticipantID;
        ///客户代码
        TThostFtdcClientIDType	ClientID;
        ///保留的无效字段
        TThostFtdcOldExchangeInstIDType	reserve2;
        ///交易所交易员代码
        TThostFtdcTraderIDType	TraderID;
        ///安装编号
        TThostFtdcInstallIDType	InstallID;
        ///报单提交状态
        TThostFtdcOrderSubmitStatusType	OrderSubmitStatus;
        ///报单提示序号
        TThostFtdcSequenceNoType	NotifySequence;
        ///交易日
        TThostFtdcDateType	TradingDay;
        ///结算编号
        TThostFtdcSettlementIDType	SettlementID;
        ///报单编号
        TThostFtdcOrderSysIDType	OrderSysID;
        ///报单来源
        TThostFtdcOrderSourceType	OrderSource;
        ///报单状态
        TThostFtdcOrderStatusType	OrderStatus;
        ///报单类型
        TThostFtdcOrderTypeType	OrderType;
        ///今成交数量
        TThostFtdcVolumeType	VolumeTraded;
        ///剩余数量
        TThostFtdcVolumeType	VolumeTotal;
        ///报单日期
        TThostFtdcDateType	InsertDate;
        ///委托时间
        TThostFtdcTimeType	InsertTime;
        ///激活时间
        TThostFtdcTimeType	ActiveTime;
        ///挂起时间
        TThostFtdcTimeType	SuspendTime;
        ///最后修改时间
        TThostFtdcTimeType	UpdateTime;
        ///撤销时间
        TThostFtdcTimeType	CancelTime;
        ///最后修改交易所交易员代码
        TThostFtdcTraderIDType	ActiveTraderID;
        ///结算会员编号
        TThostFtdcParticipantIDType	ClearingPartID;
        ///序号
        TThostFtdcSequenceNoType	SequenceNo;
        ///前置编号
        TThostFtdcFrontIDType	FrontID;
        ///会话编号
        TThostFtdcSessionIDType	SessionID;
        ///用户端产品信息
        TThostFtdcProductInfoType	UserProductInfo;
        ///状态信息
        TThostFtdcErrorMsgType	StatusMsg;
        ///用户强评标志
        TThostFtdcBoolType	UserForceClose;
        ///操作用户代码
        TThostFtdcUserIDType	ActiveUserID;
        ///经纪公司报单编号
        TThostFtdcSequenceNoType	BrokerOrderSeq;
        ///相关报单
        TThostFtdcOrderSysIDType	RelativeOrderSysID;
        ///郑商所成交数量
        TThostFtdcVolumeType	ZCETotalTradedVolume;
        ///互换单标志
        TThostFtdcBoolType	IsSwapOrder;
        ///营业部编号
        TThostFtdcBranchIDType	BranchID;
        ///投资单元代码
        TThostFtdcInvestUnitIDType	InvestUnitID;
        ///资金账号
        TThostFtdcAccountIDType	AccountID;
        ///币种代码
        TThostFtdcCurrencyIDType	CurrencyID;
        ///保留的无效字段
        TThostFtdcOldIPAddressType	reserve3;
        ///Mac地址
        TThostFtdcMacAddressType	MacAddress;
        ///合约代码
        TThostFtdcInstrumentIDType	InstrumentID;
        ///合约在交易所的代码
        TThostFtdcExchangeInstIDType	ExchangeInstID;
        ///IP地址
        TThostFtdcIPAddressType	IPAddress;
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
    # 报单价格条件
    order_price_type: str
    # 买卖方向
    direction: str
    # 组合开平标志
    comb_offset_flag: str
    # 组合投机套保标志
    comb_hedge_flag: str
    # 价格
    limit_price: str
    # 数量
    volume_total_original: str
    # 有效期类型
    time_condition: str
    # GTD日期
    gtd_date: str
    # 成交量类型
    volume_condition: str
    # 最小成交量
    min_volume: str
    # 触发条件
    contingent_condition: str
    # 止损价
    stop_price: str
    # 强平原因
    force_close_reason: str
    # 自动挂起标志
    is_auto_suspend: str
    # 业务单元
    business_unit: str
    # 请求编号
    request_id: str
    # 本地报单编号
    order_local_id: str
    # 交易所代码
    exchange_id: str
    # 会员代码
    participant_id: str
    # 客户代码
    client_id: str
    # 保留的无效字段
    reserve2: str
    # 交易所交易员代码
    trader_id: str
    # 安装编号
    install_id: str
    # 报单提交状态
    order_submit_status: str
    # 报单提示序号
    notify_sequence: str
    # 交易日
    trading_day: str
    # 结算编号
    settlement_id: str
    # 报单编号
    order_sys_id: str
    # 报单来源
    order_source: str
    # 报单状态
    order_status: str
    # 报单类型
    order_type: str
    # 今成交数量
    volume_traded: str
    # 剩余数量
    volume_total: str
    # 报单日期
    insert_date: str
    # 委托时间
    insert_time: str
    # 激活时间
    active_time: str
    # 挂起时间
    suspend_time: str
    # 最后修改时间
    update_time: str
    # 撤销时间
    cancel_time: str
    # 最后修改交易所交易员代码
    active_trader_id: str
    # 结算会员编号
    clearing_part_id: str
    # 序号
    sequence_no: str
    # 前置编号
    front_id: str
    # 会话编号
    session_id: str
    # 用户端产品信息
    user_product_info: str
    # 状态信息
    status_msg: str
    # 用户强评标志
    user_force_close: str
    # 操作用户代码
    active_user_id: str
    # 经纪公司报单编号
    broker_order_seq: str
    # 相关报单
    relative_order_sys_id: str
    # 郑商所成交数量
    zce_total_traded_volume: str
    # 互换单标志
    is_swap_order: str
    # 营业部编号
    branch_id: str
    # 投资单元代码
    invest_unit_id: str
    # 资金账号
    account_id: str
    # 币种代码
    currency_id: str
    # 保留的无效字段
    reserve3: str
    # Mac地址
    mac_address: str
    # 合约代码
    instrument_id: str
    # 合约在交易所的代码
    exchange_inst_id: str
    # IP地址
    ip_address: str

    def __init__(self, o):
        self.broker_id = o.get('BrokerID')
        self.investor_id = o.get('InvestorID')
        self.reserve1 = o.get('reserve1')
        self.order_ref = o.get('OrderRef')
        self.user_id = o.get('UserID')
        self.order_price_type = o.get('OrderPriceType')
        self.direction = o.get('Direction')
        self.comb_offset_flag = o.get('CombOffsetFlag')
        self.comb_hedge_flag = o.get('CombHedgeFlag')
        self.limit_price = o.get('LimitPrice')
        self.volume_total_original = o.get('VolumeTotalOriginal')
        self.time_condition = o.get('TimeCondition')
        self.gtd_date = o.get('GTDDate')
        self.volume_condition = o.get('VolumeCondition')
        self.min_volume = o.get('MinVolume')
        self.contingent_condition = o.get('ContingentCondition')
        self.stop_price = o.get('StopPrice')
        self.force_close_reason = o.get('ForceCloseReason')
        self.is_auto_suspend = o.get('IsAutoSuspend')
        self.business_unit = o.get('BusinessUnit')
        self.request_id = o.get('RequestID')
        self.order_local_id = o.get('OrderLocalID')
        self.exchange_id = o.get('ExchangeID')
        self.participant_id = o.get('ParticipantID')
        self.client_id = o.get('ClientID')
        self.reserve2 = o.get('reserve2')
        self.trader_id = o.get('TraderID')
        self.install_id = o.get('InstallID')
        self.order_submit_status = o.get('OrderSubmitStatus')
        self.notify_sequence = o.get('NotifySequence')
        self.trading_day = o.get('TradingDay')
        self.settlement_id = o.get('SettlementID')
        self.order_sys_id = o.get('OrderSysID')
        self.order_source = o.get('OrderSource')
        self.order_status = o.get('OrderStatus')
        self.order_type = o.get('OrderType')
        self.volume_traded = o.get('VolumeTraded')
        self.volume_total = o.get('VolumeTotal')
        self.insert_date = o.get('InsertDate')
        self.insert_time = o.get('InsertTime')
        self.active_time = o.get('ActiveTime')
        self.suspend_time = o.get('SuspendTime')
        self.update_time = o.get('UpdateTime')
        self.cancel_time = o.get('CancelTime')
        self.active_trader_id = o.get('ActiveTraderID')
        self.clearing_part_id = o.get('ClearingPartID')
        self.sequence_no = o.get('SequenceNo')
        self.front_id = o.get('FrontID')
        self.session_id = o.get('SessionID')
        self.user_product_info = o.get('UserProductInfo')
        self.status_msg = o.get('StatusMsg')
        self.user_force_close = o.get('UserForceClose')
        self.active_user_id = o.get('ActiveUserID')
        self.broker_order_seq = o.get('BrokerOrderSeq')
        self.relative_order_sys_id = o.get('RelativeOrderSysID')
        self.zce_total_traded_volume = o.get('ZCETotalTradedVolume')
        self.is_swap_order = o.get('IsSwapOrder')
        self.branch_id = o.get('BranchID')
        self.invest_unit_id = o.get('InvestUnitID')
        self.account_id = o.get('AccountID')
        self.currency_id = o.get('CurrencyID')
        self.reserve3 = o.get('reserve3')
        self.mac_address = o.get('MacAddress')
        self.instrument_id = o.get('InstrumentID')
        self.exchange_inst_id = o.get('ExchangeInstID')
        self.ip_address = o.get('IPAddress')


if __name__ == '__main__':
    o = CtpOrder({})
    print(o)
