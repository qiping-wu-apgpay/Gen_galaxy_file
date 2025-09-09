#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交易数据合并器
Transaction Data Merger

将公共交易数据和业务特定数据合并成完整的交易数据文件。
"""

import os
import random
from typing import Dict, List, Any

from txn_errors import FileTypeError
from common_transaction import CommonTransaction
from hotel_serviceDesc import HotelServiceDesc


class FullTransactionMerger:
    """交易数据合并器类"""
    
    def __init__(self, config_dir: str = "config"):
        """初始化合并器"""
        self.config_dir = config_dir
        
        # 确保输出目录存在
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_dir = os.path.normpath(os.path.join(current_dir, "..", "output"))
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 初始化生成器
        self.common = CommonTransaction(config_dir)
        self.hotel = HotelServiceDesc(config_dir)
    
    def generate_file(self, file_type: str, count: int = 1, output_filename: str = None) -> str:
        """生成完整的交易数据文件"""
        if file_type not in ["B", "M"]:
            raise FileTypeError(f"不支持的文件类型: {file_type}，只支持 B 或 M")
        
        lines = []
        
        # 1. 生成文件头
        header = self.common.generate_header(file_type)
        lines.append(header)
        
        # 2. 生成交易记录
        for _ in range(count):
            # 生成随机金额
            self.common.last_generated_amount = round(random.uniform(100.0, 2000.0), 2)
            
            # 生成完整的交易记录
            transaction = self.merge_transaction(file_type)
            lines.append(transaction)
        
        # 3. 生成文件尾
        total_records = len(lines) + 1
        trailer = self.common.generate_trailer(file_type, total_records)
        lines.append(trailer)
        
        # 4. 写入文件
        if output_filename:
            filename = output_filename
            if not filename.endswith('.txt'):
                filename += '.txt'
        else:
            filename = self.common.generate_standard_filename(file_type)
        
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            for line in lines:
                f.write(line + '\n')
        
        print(f"\n✅ 文件生成成功: {filepath}")
        print(f"📊 总交易记录数: {count}")
        print(f"📁 总文件行数: {len(lines)} (头: 1, 交易: {count}, 尾: 1)")
        
        return filepath
    
    def merge_transaction(self, file_type: str) -> str:
        """合并生成完整的交易记录 (850位)"""
        # 1. 生成公共字段（1-5, 7-48, 50字段）
        common_fields = self.common.generate_common_fields(file_type)
        
        # 获取交易类型（第2个字段，索引1）
        transaction_type = common_fields[1]
        
        # 2. 生成文档号（第6字段）和服务描述（第49字段）
        if transaction_type == "H":
            # H类型使用酒店服务描述
            doc_number = self.hotel.generate_document_number()
            service_desc = self.hotel.generate_service_description(self.common.last_generated_amount)
        else:
            # 其他类型暂时使用空白填充
            doc_number = " " * 30  # 第6字段，30位
            service_desc = " " * 270  # 第49字段，270位
        
        # 3. 合并完整记录
        # 插入文档号到第6个位置（索引5）
        common_fields.insert(5, doc_number)
        # 插入服务描述到倒数第二个位置（50字段前）
        common_fields.insert(-1, service_desc)
        
        return "".join(common_fields)
