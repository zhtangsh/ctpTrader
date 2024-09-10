from dataclasses import dataclass


@dataclass
class CtpTradingAccount:
    """
    ///资金账户
    struct CThostFtdcTradingAccountField
    {
        ///经纪公司代码
        TThostFtdcBrokerIDType	BrokerID;
        ///投资者帐号
        TThostFtdcAccountIDType	AccountID;
        ///上次质押金额
        TThostFtdcMoneyType	PreMortgage;
        ///上次信用额度
        TThostFtdcMoneyType	PreCredit;
        ///上次存款额
        TThostFtdcMoneyType	PreDeposit;
        ///上次结算准备金
        TThostFtdcMoneyType	PreBalance;
        ///上次占用的保证金
        TThostFtdcMoneyType	PreMargin;
        ///利息基数
        TThostFtdcMoneyType	InterestBase;
        ///利息收入
        TThostFtdcMoneyType	Interest;
        ///入金金额
        TThostFtdcMoneyType	Deposit;
        ///出金金额
        TThostFtdcMoneyType	Withdraw;
        ///冻结的保证金
        TThostFtdcMoneyType	FrozenMargin;
        ///冻结的资金
        TThostFtdcMoneyType	FrozenCash;
        ///冻结的手续费
        TThostFtdcMoneyType	FrozenCommission;
        ///当前保证金总额
        TThostFtdcMoneyType	CurrMargin;
        ///资金差额
        TThostFtdcMoneyType	CashIn;
        ///手续费
        TThostFtdcMoneyType	Commission;
        ///平仓盈亏
        TThostFtdcMoneyType	CloseProfit;
        ///持仓盈亏
        TThostFtdcMoneyType	PositionProfit;
        ///期货结算准备金
        TThostFtdcMoneyType	Balance;
        ///可用资金
        TThostFtdcMoneyType	Available;
        ///可取资金
        TThostFtdcMoneyType	WithdrawQuota;
        ///基本准备金
        TThostFtdcMoneyType	Reserve;
        ///交易日
        TThostFtdcDateType	TradingDay;
        ///结算编号
        TThostFtdcSettlementIDType	SettlementID;
        ///信用额度
        TThostFtdcMoneyType	Credit;
        ///质押金额
        TThostFtdcMoneyType	Mortgage;
        ///交易所保证金
        TThostFtdcMoneyType	ExchangeMargin;
        ///投资者交割保证金
        TThostFtdcMoneyType	DeliveryMargin;
        ///交易所交割保证金
        TThostFtdcMoneyType	ExchangeDeliveryMargin;
        ///保底期货结算准备金
        TThostFtdcMoneyType	ReserveBalance;
        ///币种代码
        TThostFtdcCurrencyIDType	CurrencyID;
        ///上次货币质入金额
        TThostFtdcMoneyType	PreFundMortgageIn;
        ///上次货币质出金额
        TThostFtdcMoneyType	PreFundMortgageOut;
        ///货币质入金额
        TThostFtdcMoneyType	FundMortgageIn;
        ///货币质出金额
        TThostFtdcMoneyType	FundMortgageOut;
        ///货币质押余额
        TThostFtdcMoneyType	FundMortgageAvailable;
        ///可质押货币金额
        TThostFtdcMoneyType	MortgageableFund;
        ///特殊产品占用保证金
        TThostFtdcMoneyType	SpecProductMargin;
        ///特殊产品冻结保证金
        TThostFtdcMoneyType	SpecProductFrozenMargin;
        ///特殊产品手续费
        TThostFtdcMoneyType	SpecProductCommission;
        ///特殊产品冻结手续费
        TThostFtdcMoneyType	SpecProductFrozenCommission;
        ///特殊产品持仓盈亏
        TThostFtdcMoneyType	SpecProductPositionProfit;
        ///特殊产品平仓盈亏
        TThostFtdcMoneyType	SpecProductCloseProfit;
        ///根据持仓盈亏算法计算的特殊产品持仓盈亏
        TThostFtdcMoneyType	SpecProductPositionProfitByAlg;
        ///特殊产品交易所保证金
        TThostFtdcMoneyType	SpecProductExchangeMargin;
        ///业务类型
        TThostFtdcBizTypeType	BizType;
        ///延时换汇冻结金额
        TThostFtdcMoneyType	FrozenSwap;
        ///剩余换汇额度
        TThostFtdcMoneyType	RemainSwap;
    };
    """
    # 经纪公司代码
    broker_id: str
    # 投资者帐号
    account_id: str
    # 上次质押金额
    pre_mortgage: str
    # 上次信用额度
    pre_credit: str
    # 上次存款额
    pre_deposit: str
    # 上次结算准备金
    pre_balance: str
    # 上次占用的保证金
    pre_margin: str
    # 利息基数
    interest_base: str
    # 利息收入
    interest: str
    # 入金金额
    deposit: str
    # 出金金额
    withdraw: str
    # 冻结的保证金
    frozen_margin: str
    # 冻结的资金
    frozen_cash: str
    # 冻结的手续费
    frozen_commission: str
    # 当前保证金总额
    curr_margin: str
    # 资金差额
    cash_in: str
    # 手续费
    commission: str
    # 平仓盈亏
    close_profit: str
    # 持仓盈亏
    position_profit: str
    # 期货结算准备金
    balance: str
    # 可用资金
    available: str
    # 可取资金
    withdraw_quota: str
    # 基本准备金
    reserve: str
    # 交易日
    trading_day: str
    # 结算编号
    settlement_id: str
    # 信用额度
    credit: str
    # 质押金额
    mortgage: str
    # 交易所保证金
    exchange_margin: str
    # 投资者交割保证金
    delivery_margin: str
    # 交易所交割保证金
    exchange_delivery_margin: str
    # 保底期货结算准备金
    reserve_balance: str
    # 币种代码
    currency_id: str
    # 上次货币质入金额
    pre_fund_mortgage_in: str
    # 上次货币质出金额
    pre_fund_mortgage_out: str
    # 货币质入金额
    fund_mortgage_in: str
    # 货币质出金额
    fund_mortgage_out: str
    # 货币质押余额
    fund_mortgage_available: str
    # 可质押货币金额
    mortgageable_fund: str
    # 特殊产品占用保证金
    spec_product_margin: str
    # 特殊产品冻结保证金
    spec_product_frozen_margin: str
    # 特殊产品手续费
    spec_product_commission: str
    # 特殊产品冻结手续费
    spec_product_frozen_commission: str
    # 特殊产品持仓盈亏
    spec_product_position_profit: str
    # 特殊产品平仓盈亏
    spec_product_close_profit: str
    # 根据持仓盈亏算法计算的特殊产品持仓盈亏
    spec_product_position_profit_by_alg: str
    # 特殊产品交易所保证金
    spec_product_exchange_margin: str
    # 业务类型
    biz_type: str
    # 延时换汇冻结金额
    frozen_swap: str
    # 剩余换汇额度
    remain_swap: str

    def __init__(self, o):
        self.broker_id = o.get('BrokerID')
        self.account_id = o.get('AccountID')
        self.pre_mortgage = o.get('PreMortgage')
        self.pre_credit = o.get('PreCredit')
        self.pre_deposit = o.get('PreDeposit')
        self.pre_balance = o.get('PreBalance')
        self.pre_margin = o.get('PreMargin')
        self.interest_base = o.get('InterestBase')
        self.interest = o.get('Interest')
        self.deposit = o.get('Deposit')
        self.withdraw = o.get('Withdraw')
        self.frozen_margin = o.get('FrozenMargin')
        self.frozen_cash = o.get('FrozenCash')
        self.frozen_commission = o.get('FrozenCommission')
        self.curr_margin = o.get('CurrMargin')
        self.cash_in = o.get('CashIn')
        self.commission = o.get('Commission')
        self.close_profit = o.get('CloseProfit')
        self.position_profit = o.get('PositionProfit')
        self.balance = o.get('Balance')
        self.available = o.get('Available')
        self.withdraw_quota = o.get('WithdrawQuota')
        self.reserve = o.get('Reserve')
        self.trading_day = o.get('TradingDay')
        self.settlement_id = o.get('SettlementID')
        self.credit = o.get('Credit')
        self.mortgage = o.get('Mortgage')
        self.exchange_margin = o.get('ExchangeMargin')
        self.delivery_margin = o.get('DeliveryMargin')
        self.exchange_delivery_margin = o.get('ExchangeDeliveryMargin')
        self.reserve_balance = o.get('ReserveBalance')
        self.currency_id = o.get('CurrencyID')
        self.pre_fund_mortgage_in = o.get('PreFundMortgageIn')
        self.pre_fund_mortgage_out = o.get('PreFundMortgageOut')
        self.fund_mortgage_in = o.get('FundMortgageIn')
        self.fund_mortgage_out = o.get('FundMortgageOut')
        self.fund_mortgage_available = o.get('FundMortgageAvailable')
        self.mortgageable_fund = o.get('MortgageableFund')
        self.spec_product_margin = o.get('SpecProductMargin')
        self.spec_product_frozen_margin = o.get('SpecProductFrozenMargin')
        self.spec_product_commission = o.get('SpecProductCommission')
        self.spec_product_frozen_commission = o.get('SpecProductFrozenCommission')
        self.spec_product_position_profit = o.get('SpecProductPositionProfit')
        self.spec_product_close_profit = o.get('SpecProductCloseProfit')
        self.spec_product_position_profit_by_alg = o.get('SpecProductPositionProfitByAlg')
        self.spec_product_exchange_margin = o.get('SpecProductExchangeMargin')
        self.biz_type = o.get('BizType')
        self.frozen_swap = o.get('FrozenSwap')
        self.remain_swap = o.get('RemainSwap')


if __name__ == '__main__':
    t = CtpTradingAccount({})
    print(t)
