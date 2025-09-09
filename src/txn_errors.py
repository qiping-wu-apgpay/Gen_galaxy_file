#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交易数据生成器异常类
Transaction Data Generator Exception Classes
"""

class TransactionError(Exception):
    """交易数据生成器基础异常类"""
    pass

class ConfigError(TransactionError):
    """配置错误"""
    pass

class FileTypeError(TransactionError):
    """文件类型错误"""
    pass

class BusinessTypeError(TransactionError):
    """业务类型错误"""
    pass

class CardNumberError(TransactionError):
    """卡号错误"""
    pass

class FormatError(TransactionError):
    """格式错误"""
    pass
