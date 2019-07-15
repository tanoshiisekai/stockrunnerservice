# -*-coding:utf-8-*-
#
# 本代码文件用于创建数据库表格
#

from appbase import global_db as _
import dbmodels  # 引入有效的数据库模型


def create_db():
    _.create_all()