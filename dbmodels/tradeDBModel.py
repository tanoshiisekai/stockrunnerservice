# -*-coding:utf-8-*-
#
# 本代码文件用于创建数据库表格
#

from appbase import global_db as _


class Trade(_.Model):
    __tablename__ = 'trade'
    trade_id = _.Column(_.Integer, primary_key=True)   # 交易编号
    trade_datetime = _.Column(_.String(10), nullable=False)  # 交易日期
    trade_time = _.Column(_.String(10), nullable=False)  # 交易时间
    trade_stock_id = _.Column(_.String(10), nullable=False)  # 股票代码
    trade_stock_name = _.Column(_.String(10), nullable=False)  # 股票名称
    trade_type = _.Column(_.Integer, nullable=False)  # 1买入，2卖出  # 交易类型
    trade_amount = _.Column(_.Integer, nullable=False)  # 交易手数
    trade_price = _.Column(_.String(10), nullable=False)   # 交易价格
    trade_brokerage = _.Column(_.String(10), nullable=False)   # 手续费
    trade_totalvalue = _.Column(_.String(20), nullable=False)   # 交易总费用

    def __init__(self, trade_datetime, trade_time, trade_stock_id, trade_stock_name,
                 trade_type, trade_amount, trade_price, trade_brokerage, trade_totalvalue):
        self.trade_datetime = trade_datetime
        self.trade_time = trade_time
        self.trade_stock_id = trade_stock_id
        self.trade_stock_name = trade_stock_name
        self.trade_type = trade_type
        self.trade_amount = trade_amount
        self.trade_price = trade_price
        self.trade_brokerage = trade_brokerage
        self.trade_totalvalue = trade_totalvalue

    def tolist(self):
        return [self.trade_datetime, self.trade_time, self.trade_stock_id, self.trade_stock_name,
                self.trade_type, self.trade_amount, self.trade_price, self.trade_brokerage, self.trade_totalvalue]
