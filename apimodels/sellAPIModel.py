# -*-coding:utf-8-*-
#
# 本代码文件用于创建接口模型
#

from appbase import global_api
from flask_restplus import fields


sellmodel = global_api.model('sellmodel', {
    'trade_stock_id': fields.String(required=True, description="strade_stock_id"),
    'trade_amount': fields.Integer(required=True, description="trade_amount"),
    'trade_price': fields.Float(required=True, description="trade_price"),
    'trade_brokerage': fields.Float(required=True, description="trade_brokerage"),
    'trade_totalvalue': fields.Float(required=True, description="trade_totalvalue")
})