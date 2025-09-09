#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交易数据生成器命令行接口
Transaction Data Generator CLI (Command Line Interface)

此模块提供命令行接口，用于生成交易数据文件。
This module provides a command-line interface for generating transaction data files.
"""

import sys
import os
import argparse
from typing import Dict, List, Any

from full_txn_merger import FullTransactionMerger
from txn_errors import (
    TransactionError, ConfigError, FileTypeError,
    BusinessTypeError, CardNumberError, FormatError
)

def run_cli():
    """命令行接口入口函数"""
    parser = argparse.ArgumentParser(
        description="交易数据生成器 - 生成指定格式的交易数据文件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
1. 生成B类型文件:
   python3 generate.py -t B --count 3

2. 生成M类型文件:
   python3 generate.py -t M --count 5

3. 指定输出文件名:
   python3 generate.py -t B --count 3 -o custom_name

注意: 请在项目根目录下执行命令
        """
    )
    
    # 必选参数
    parser.add_argument('-t', '--file-type', choices=['B', 'M'], required=True,
                       help='文件类型: B (BSP) 或 M (MA)')
    
    # 可选参数
    parser.add_argument('--count', type=int, default=1,
                       help='生成的交易记录数量，范围1-9999 (默认: 1)')
    parser.add_argument('-o', '--output',
                       help='输出文件名 (不含扩展名)')
    
    args = parser.parse_args()
    
    try:
        # 验证交易记录数量
        if args.count < 1 or args.count > 9999:
            raise ConfigError(f"交易记录数量必须在1-9999之间，当前值: {args.count}")
            
        # 初始化生成器
        merger = FullTransactionMerger()
        
        # 准备业务配置
        business_configs = [{
            'business_type': 'hotel',  # 目前只支持hotel类型
            'count': args.count
        }]
        
        # 生成文件
        filepath = merger.generate_file(
            file_type=args.file_type,
            count=args.count,
            output_filename=args.output
        )
        
        print(f"\n✅ 文件生成成功: {filepath}")
        
    except FileNotFoundError as e:
        print(f"❌ 文件未找到: {e}")
        sys.exit(1)
    except FileTypeError as e:
        print(f"❌ 文件类型错误: {e}")
        print("支持的文件类型: B (BSP) 或 M (MA)")
        sys.exit(1)
    except BusinessTypeError as e:
        print(f"❌ 业务类型错误: {e}")
        print("当前支持的业务类型: hotel")
        sys.exit(1)
    except ConfigError as e:
        print(f"❌ 配置错误: {e}")
        print("请检查参数是否正确")
        sys.exit(1)
    except FormatError as e:
        print(f"❌ 格式错误: {e}")
        sys.exit(1)
    except CardNumberError as e:
        print(f"❌ 卡号错误: {e}")
        print("请检查卡号配置是否正确")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 未预期的错误: {e}")
        print("如果问题持续存在，请联系开发人员")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_cli()
