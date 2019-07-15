# -*-coding:utf-8-*-
#
# 本代码文件用于完成数据库操作
#

from flask import jsonify
from sqlalchemy import and_, distinct
from appbase import global_db as db
from dbmodels.tradeDBModel import Trade
from tools.info import Info
from tools.log import logger
from decimal import Decimal
from tools.timetools import getdatetime, gettime
import tushare
from tools.debug import r_set


class TradeDAO:

    def __init__(self):
        pass

    @staticmethod
    def buystock(params):
        """
        买股票
        """
        trade = params
        trade_datetime = getdatetime()
        trade_time = gettime()
        trade_stock_id = trade["trade_stock_id"]
        trade_stock_name = tushare.get_realtime_quotes(trade_stock_id)["name"][0]
        trade_type = 1
        trade_amount = trade["trade_amount"]
        trade_price = trade["trade_price"]
        trade_brokerage = trade["trade_brokerage"]
        trade_totalvalue = trade["trade_totalvalue"]
        t = Trade(trade_datetime, trade_time, trade_stock_id, trade_stock_name,
                  trade_type, trade_amount, trade_price, trade_brokerage, trade_totalvalue)
        db.session.add(t)
        try:
            db.session.commit()
        except Exception as e:
            logger.error(e)
            return jsonify(Info(False, "购买股票失败").tojson())
        else:
            return jsonify(Info(True, "购买股票成功").tojson())

    @staticmethod
    def sellstock(params):
        """
        卖股票
        """
        trade = params
        trade_datetime = getdatetime()
        trade_time = gettime()
        trade_stock_id = trade["trade_stock_id"]
        trade_stock_name = tushare.get_realtime_quotes(trade_stock_id)["name"][0]
        trade_type = 2
        trade_amount = trade["trade_amount"]
        trade_price = trade["trade_price"]
        trade_brokerage = trade["trade_brokerage"]
        trade_totalvalue = trade["trade_totalvalue"]
        t = Trade(trade_datetime, trade_time, trade_stock_id, trade_stock_name,
                  trade_type, trade_amount, trade_price, trade_brokerage, trade_totalvalue)
        db.session.add(t)
        try:
            db.session.commit()
        except Exception as e:
            logger.error(e)
            return jsonify(Info(False, "出售股票失败").tojson())
        else:
            return jsonify(Info(True, "出售股票成功").tojson())

    @staticmethod
    def getbuy_1(stockid):
        """
        获取股票买一的价格
        """
        buy_1 = tushare.get_realtime_quotes(stockid)["b1_p"].get(0)
        return jsonify(Info(True, "成功", buy_1).tojson())

    @staticmethod
    def getsell_1(stockid):
        """
        获取股票卖一的价格
        """
        sell_1 = tushare.get_realtime_quotes(stockid)["a1_p"].get(0)
        return jsonify(Info(True, "成功", sell_1).tojson())


    @staticmethod
    def getnowamount(stockid):
        """
        获取当前持有股票的手数
        """
        return jsonify(Info(True, "成功", TradeDAO.nowamount(stockid)).tojson())

    @staticmethod
    def nowamount(stockid):
        """
        实现获取当前持有股票的手数
        """
        buyamount = db.session.query(Trade).filter(and_(
            Trade.trade_stock_id == stockid, Trade.trade_type == 1
        )).all()
        buyvalue = sum([x.trade_amount for x in buyamount])
        sellamount = db.session.query(Trade).filter(and_(
            Trade.trade_stock_id == stockid, Trade.trade_type == 2
        )).all()
        sellvalue = sum([x.trade_amount for x in sellamount])
        return buyvalue-sellvalue

    @staticmethod
    def getstockname(stockid):
        """
        获取股票名称
        """
        return db.session.query(Trade.trade_stock_name).filter(Trade.trade_stock_id==stockid).first()[0]

    @staticmethod
    def nowtotalvalue(stockid):
        """
        实现获取当前持有股票的买入结余总支出
        """
        buylist = db.session.query(Trade).filter(and_(
            Trade.trade_stock_id == stockid, Trade.trade_type == 1
        )).all()
        buytotalvalues = sum([float(x.trade_totalvalue) for x in buylist])
        selllist = db.session.query(Trade).filter(and_(
            Trade.trade_stock_id == stockid, Trade.trade_type == 2
        )).all()
        selltotalvalues = sum([float(x.trade_totalvalue) for x in selllist])
        return selltotalvalues-buytotalvalues

    @staticmethod
    def getstockintrade():
        """
        获取当前在交易中的股票数据
        """
        stocklist = [x[0] for x in db.session.query(Trade.trade_stock_id).distinct().all()]
        stocklist = [x for x in stocklist if TradeDAO.nowamount(x) > 0]
        namelist = [TradeDAO.getstockname(x) for x in stocklist]
        amountlist = [TradeDAO.nowamount(x) for x in stocklist]
        nowtotalvaluelist = [TradeDAO.nowtotalvalue(x) for x in stocklist]
        sell1list = [tushare.get_realtime_quotes(x)["b1_p"].get(0) for x in stocklist]
        validstocklist = list(zip(stocklist, namelist, amountlist, nowtotalvaluelist, sell1list))
        return jsonify(Info(True, "成功", validstocklist).tojson())

    @staticmethod
    def getsummary():
        """
        获取汇总
        """
        summary = 0
        sumlist = []
        stocklist = db.session.query(Trade).order_by(Trade.trade_datetime, Trade.trade_time).all()
        for sl in stocklist:
            if int(sl.trade_type) == 1:
                summary = summary - float(sl.trade_totalvalue)
                sumlist.append([sl.trade_datetime, sl.trade_time,
                                sl.trade_stock_id, sl.trade_stock_name,
                                sl.trade_amount,
                                sl.trade_price, sl.trade_brokerage, sl.trade_totalvalue,
                                0, 0, 0, 0, summary])
            elif int(sl.trade_type) == 2:
                summary = summary + float(sl.trade_totalvalue)
                sumlist.append([sl.trade_datetime, sl.trade_time,
                                sl.trade_stock_id, sl.trade_stock_name,
                                0, 0, 0, 0,
                                sl.trade_amount, sl.trade_price, sl.trade_brokerage,
                                sl.trade_totalvalue, summary])
        return jsonify(Info(True, "成功", sumlist).tojson())