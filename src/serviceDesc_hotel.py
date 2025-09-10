#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
酒店服务描述生成器
Hotel Service Description Generator

负责生成酒店业务的特殊字段：
1. 第6个参数:文档号 (30位)
2. 第49个参数:服务描述 (270位)
"""

import os
import yaml
import random
from datetime import datetime, timedelta


class ServiceDescHotel:
    """酒店服务描述生成器类"""
    
    def __init__(self, config_dir: str = "config"):
        """初始化生成器"""
        dict_dir = os.path.join(config_dir, "dictionaries")
        
        # 加载酒店和城市信息
        with open(os.path.join(dict_dir, "hotel_names.yaml"), 'r', encoding='utf-8') as f:
            hotel_data = yaml.safe_load(f)
            self.hotel_names = hotel_data['hotel_names']
            self.city_names = hotel_data['city_names']
    
    def generate_document_number(self) -> str:
        """【第6个参数,30位】生成文档号"""
        # 生成规则：长度固定30，88+8位随机数字+20位空格
        doc_number = "888" + "".join([str(random.randint(0, 9)) for _ in range(7)]) + " " * 20
        return doc_number[:30]
    
    def generate_service_description(self, amount: float) -> str:
        """【第49个参数,270位】生成服务描述"""
        fields = []
        
        # 1. COMPANY_CODE公司代码 (2位)
        fields.append("  ")
        
        # 2. CONTRACT_NUMBER合同号 (30位)
        fields.append(datetime.now().strftime("%Y%m%d%H%M%S").ljust(30))
        
        # 3. SD_HOTEL_NAME酒店名称 (30位)
        fields.append(random.choice(self.hotel_names).ljust(30))
        
        # 4. CHECK_IN_REASON住宿原因指示符 (1位)
        fields.append(" ")
        
        # 5. CHECK_IN_DATE入住日期 (8位)
        fields.append(datetime.now().strftime("%Y%m%d"))
        
        # 6. CHECK_IN_TIME入住时间 (4位)
        fields.append("0000")
        
        # 7. LOCATION_CODE位置代码 (3位)
        fields.append("   ")
        
        # 8. LOCATION_CITY城市名称 (20位)
        fields.append(random.choice(self.city_names).ljust(20))
        
        # 9. CHECK_OUT_DATE退房日期 (8位)
        checkout_date = datetime.now() + timedelta(days=2)
        fields.append(checkout_date.strftime("%Y%m%d"))
        
        # 10. CHECK_OUT_TIME退房时间 (4位)
        fields.append("0000")
        
        # 11. NO_SHOW_IND未入住指示符 (1位)• “0”表示酒店服务已使用   # “1”表示未入住（酒店服务未使用） # “9”表示未知
        fields.append("0")
        
        # 12. ROOM_GUEST_COUNT客人数量 (3位)
        fields.append("001")
        
        # 13. ROOM_NIGHTS房间夜数 (3位)
        fields.append("002")
        
        # 14. ROOM_RATE_IND房价指示符 (1位)
        fields.append("9")
        
        # 15. INCLUDED_SERVICE_IND包含服务指示符 (1位)
        fields.append("9")
        
        # 16. NET_ROOM_AMOUNT房间净金额 (15位)
        fields.append("0" * 15)
        
        # 17. NET_ROOM_VAT_IND房间VAT指示符 (1位)
        fields.append("0")
        
        # 18-32. 服务1-5的代码、金额和VAT 
        for _ in range(5):
            fields.append("   ")  # 服务代码 (3位)
            fields.append("0" * 15)  # 服务金额 (15位)
            fields.append("0")  # 服务VAT指示符 (1位)
        
        # 33. 预付费用 (15位)
        fields.append("0" * 15)
        
        # 34. 酒店描述 (25位)
        fields.append(" Hotle_descript      end ")
        
        service_description = "".join(fields)
        
        # 确保长度正确
        if len(service_description) < 270:
            service_description = service_description.ljust(270)
        elif len(service_description) > 270:
            service_description = service_description[:270]
        
        return service_description
