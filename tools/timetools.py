# -*-coding:utf-8-*-
#
# 本代码文件用于完成日期时间方面的计算

from datetime import datetime
import pytz


def getdatetime():
    """
    得到当前日期
    """
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.now(tz).strftime("%Y-%m-%d")


def gettime():
    """
    得到当前时间
    """
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.now(tz).strftime("%H:%M:%S")

