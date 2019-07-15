# -*-coding:utf-8-*-
#
# 本代码文件用于创建服务接口
#

from appbase import global_api as api
from apimodels.buyAPIModel import buymodel
from apimodels.sellAPIModel import sellmodel
from daos.tradeDAO import TradeDAO
from flask_restplus import Resource

ns_account = api.namespace("trade", description="交易管理")


@ns_account.route("/buystock/")
class BuyStock(Resource):

    @ns_account.expect(buymodel)
    def post(self):
        """
        Buy Stock
        """
        return TradeDAO.buystock(api.payload)


@ns_account.route("/<string:stockid>/getbuy_1/")
class GetBuy_1(Resource):

    def get(self, stockid):
        """
        Get the buy_1 price of stock
        """
        return TradeDAO.getbuy_1(stockid)


@ns_account.route("/<string:stockid>/getsell_1/")
class GetSell_1(Resource):

    def get(self, stockid):
        """
        Get the sell_1 price of stock
        """
        return TradeDAO.getsell_1(stockid)


@ns_account.route("/<string:stockid>/getnowamount/")
class GetBuy_1(Resource):

    def get(self, stockid):
        """
        Get the buy_1 price of stock
        """
        return TradeDAO.getnowamount(stockid)


@ns_account.route("/sellstock/")
class Account(Resource):

    @ns_account.expect(sellmodel)
    def post(self):
        """
        Sell Stock
        """
        return TradeDAO.sellstock(api.payload)


@ns_account.route("/getstockintrade/")
class GetStockInTrade(Resource):

    def get(self):
        """
        Get Stocks in Trade now
        """
        return TradeDAO.getstockintrade()


@ns_account.route("/getsummary/")
class GetSummary(Resource):

    def get(self):
        """
        Get Summary
        """
        return TradeDAO.getsummary()

