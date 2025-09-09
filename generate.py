#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交易数据生成器入口文件
此文件是项目的主入口点，用于从命令行生成交易数据文件。
"""

import os
import sys

# 添加src目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'src'))

from transaction_cli import run_cli

# 为了向后兼容，保留旧的配置文件支持
from full_txn_merger import FullTransactionMerger

if __name__ == "__main__":
    run_cli()
