from dataclasses import dataclass


@dataclass
class CtpPosition:
    """
    ///投资者持仓
    struct CThostFtdcInvestorPositionField
    {
        ///保留的无效字段
        TThostFtdcOldInstrumentIDType	reserve1;
        ///经纪公司代码
        TThostFtdcBrokerIDType	BrokerID;
        ///投资者代码
        TThostFtdcInvestorIDType	InvestorID;
        ///持仓多空方向
        TThostFtdcPosiDirectionType	PosiDirection;
        ///投机套保标志
        TThostFtdcHedgeFlagType	HedgeFlag;
        ///持仓日期
        TThostFtdcPositionDateType	PositionDate;
        ///上日持仓
        TThostFtdcVolumeType	YdPosition;
        ///今日持仓
        TThostFtdcVolumeType	Position;
        ///多头冻结
        TThostFtdcVolumeType	LongFrozen;
        ///空头冻结
        TThostFtdcVolumeType	ShortFrozen;
        ///开仓冻结金额
        TThostFtdcMoneyType	LongFrozenAmount;
        ///开仓冻结金额
        TThostFtdcMoneyType	ShortFrozenAmount;
        ///开仓量
        TThostFtdcVolumeType	OpenVolume;
        ///平仓量
        TThostFtdcVolumeType	CloseVolume;
        ///开仓金额
        TThostFtdcMoneyType	OpenAmount;
        ///平仓金额
        TThostFtdcMoneyType	CloseAmount;
        ///持仓成本
        TThostFtdcMoneyType	PositionCost;
        ///上次占用的保证金
        TThostFtdcMoneyType	PreMargin;
        ///占用的保证金
        TThostFtdcMoneyType	UseMargin;
        ///冻结的保证金
        TThostFtdcMoneyType	FrozenMargin;
        ///冻结的资金
        TThostFtdcMoneyType	FrozenCash;
        ///冻结的手续费
        TThostFtdcMoneyType	FrozenCommission;
        ///资金差额
        TThostFtdcMoneyType	CashIn;
        ///手续费
        TThostFtdcMoneyType	Commission;
        ///平仓盈亏
        TThostFtdcMoneyType	CloseProfit;
        ///持仓盈亏
        TThostFtdcMoneyType	PositionProfit;
        ///上次结算价
        TThostFtdcPriceType	PreSettlementPrice;
        ///本次结算价
        TThostFtdcPriceType	SettlementPrice;
        ///交易日
        TThostFtdcDateType	TradingDay;
        ///结算编号
        TThostFtdcSettlementIDType	SettlementID;
        ///开仓成本
        TThostFtdcMoneyType	OpenCost;
        ///交易所保证金
        TThostFtdcMoneyType	ExchangeMargin;
        ///组合成交形成的持仓
        TThostFtdcVolumeType	CombPosition;
        ///组合多头冻结
        TThostFtdcVolumeType	CombLongFrozen;
        ///组合空头冻结
        TThostFtdcVolumeType	CombShortFrozen;
        ///逐日盯市平仓盈亏
        TThostFtdcMoneyType	CloseProfitByDate;
        ///逐笔对冲平仓盈亏
        TThostFtdcMoneyType	CloseProfitByTrade;
        ///今日持仓
        TThostFtdcVolumeType	TodayPosition;
        ///保证金率
        TThostFtdcRatioType	MarginRateByMoney;
        ///保证金率(按手数)
        TThostFtdcRatioType	MarginRateByVolume;
        ///执行冻结
        TThostFtdcVolumeType	StrikeFrozen;
        ///执行冻结金额
        TThostFtdcMoneyType	StrikeFrozenAmount;
        ///放弃执行冻结
        TThostFtdcVolumeType	AbandonFrozen;
        ///交易所代码
        TThostFtdcExchangeIDType	ExchangeID;
        ///执行冻结的昨仓
        TThostFtdcVolumeType	YdStrikeFrozen;
        ///投资单元代码
        TThostFtdcInvestUnitIDType	InvestUnitID;
        ///持仓成本差值
        TThostFtdcMoneyType	PositionCostOffset;
        ///tas持仓手数
        TThostFtdcVolumeType	TasPosition;
        ///tas持仓成本
        TThostFtdcMoneyType	TasPositionCost;
        ///合约代码
        TThostFtdcInstrumentIDType	InstrumentID;
    };
    """
    # 保留的无效字段
    reserve1: str
    # 经纪公司代码
    broker_id: str
    # 投资者代码
    investor_id: str
    # 持仓多空方向
    posi_direction: str
    # 投机套保标志
    hedge_flag: str
    # 持仓日期
    position_date: str
    # 上日持仓
    yd_position: int
    # 今日持仓
    position: str
    # 多头冻结
    long_frozen: str
    # 空头冻结
    short_frozen: str
    # 多头开仓冻结金额
    long_frozen_mount: str
    # 空头开仓冻结金额
    short_frozen_mount: str
    # 开仓量
    open_volume: str
    # 平仓量
    close_volume: str
    # 开仓金额
    open_amount: str
    # 平仓金额
    close_amount: str
    # 持仓成本
    position_cost: str
    # 上次占用的保证金
    pre_margin: str
    # 占用的保证金
    use_margin: str
    # 冻结的保证金
    frozen_margin: str
    # 冻结的资金
    frozen_cash: str
    # 冻结的手续费
    frozen_commission: str
    # 资金差额
    cash_in: str
    # 手续费
    commision: str
    # 平仓盈亏
    close_profit: str
    # 持仓盈亏
    position_profit: str
    # 上次结算价
    pre_settlement_price: str
    # 本次结算价
    settlement_price: str
    # 交易日
    trading_day: str
    # 结算编号
    settlement_id: str
    # 开仓成本
    open_cost: str
    # 交易所保证金
    exchange_margin: str
    # 组合成交形成的持仓
    comb_position: str
    # 组合多头冻结
    comb_long_frozen: str
    # 组合空头冻结
    comb_short_frozen: str
    # 逐日盯市平仓盈亏
    close_profit_by_date: str
    # 逐笔对冲平仓盈亏
    close_profit_by_trade: str
    # 今日持仓
    today_position: str
    # 保证金率
    margin_rate_by_money: str
    # 保证金率(按手数)
    margin_rate_by_volume: str
    # 执行冻结
    strike_frozen: str
    # 执行冻结金额
    strike_frozen_amount: str
    # 放弃执行冻结
    abandon_frozen: str
    # 交易所代码
    exchange_id: str
    # 执行冻结的昨仓
    yd_strike_frozen: str
    # 投资单元代码
    invest_unit_id: str
    # 持仓成本差值
    position_cost_offset: str
    # tas持仓手数
    tas_position: str
    # tas持仓成本
    tas_position_cost: str
    # 合约代码
    instrument_id: str

    def __init__(self, o):
        self.reserve1 = o.get('reserve1')
        self.broker_id = o.get('BrokerID')
        self.investor_id = o.get('InvestorID')
        self.posi_direction = o.get('PosiDirection')
        self.hedge_flag = o.get('HedgeFlag')
        self.position_date = o.get('PositionDate')
        self.yd_position = o.get('YdPosition')
        self.position = o.get('Position')
        self.long_frozen = o.get('LongFrozen')
        self.short_frozen = o.get('ShortFrozen')
        self.long_frozen_mount = o.get('LongFrozenAmount')
        self.short_frozen_mount = o.get('ShortFrozenAmount')
        self.open_volume = o.get('OpenVolume')
        self.close_volume = o.get('CloseVolume')
        self.open_amount = o.get('OpenAmount')
        self.close_amount = o.get('CloseAmount')
        self.position_cost = o.get('PositionCost')
        self.pre_margin = o.get('PreMargin')
        self.use_margin = o.get('UseMargin')
        self.frozen_margin = o.get('FrozenMargin')
        self.frozen_cash = o.get('FrozenCash')
        self.frozen_commission = o.get('FrozenCommission')
        self.cash_in = o.get('CashIn')
        self.commision = o.get('Commission')
        self.close_profit = o.get('CloseProfit')
        self.position_profit = o.get('PositionProfit')
        self.pre_settlement_price = o.get('PreSettlementPrice')
        self.settlement_price = o.get('SettlementPrice')
        self.trading_day = o.get('TradingDay')
        self.settlement_id = o.get('SettlementID')
        self.open_cost = o.get('OpenCost')
        self.exchange_margin = o.get('ExchangeMargin')
        self.comb_position = o.get('CombPosition')
        self.comb_long_frozen = o.get('CombLongFrozen')
        self.comb_short_frozen = o.get('CombShortFrozen')
        self.close_profit_by_date = o.get('CloseProfitByDate')
        self.close_profit_by_trade = o.get('CloseProfitByTrade')
        self.today_position = o.get('TodayPosition')
        self.margin_rate_by_money = o.get('MarginRateByMoney')
        self.margin_rate_by_volume = o.get('MarginRateByVolume')
        self.strike_frozen = o.get('StrikeFrozen')
        self.strike_frozen_amount = o.get('StrikeFrozenAmount')
        self.abandon_frozen = o.get('AbandonFrozen')
        self.exchange_id = o.get('ExchangeID')
        self.yd_strike_frozen = o.get('YdStrikeFrozen')
        self.invest_unit_id = o.get('InvestUnitID')
        self.position_cost_offset = o.get('PositionCostOffset')
        self.tas_position = o.get('TasPosition')
        self.tas_position_cost = o.get('TasPositionCost')
        self.instrument_id = o.get('InstrumentID')


if __name__ == '__main__':
    p = CtpPosition({})
    print(p)
