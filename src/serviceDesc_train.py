#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
火车票服务描述生成器
负责生成火车票业务的特殊字段：
1. 第6个参数:文档号 (30位)
2. 第49个参数:服务描述 (270位)
"""

import random
from datetime import datetime
import os
import yaml


class ServiceDescTrain:
    """火车票服务描述生成器类"""
    
    def generate_document_number(self) -> str:
        """【第6个参数,30位】生成文档号"""
        random_number = str(random.randint(10000000, 99999999))  # 8位随机数字
        doc_number = f"88{random_number}" + " " * 20
        return doc_number
    
    def generate_service_description(self, amount: float) -> str:
        """【第49个参数,270位】生成服务描述"""
        fields = []
        
        # 1. 火车公司名称 (15位)SD_TRAIN_COMPANY_NAME
        fields.append("CHINA CRH".ljust(15))
        
        # 2. 出发日期 (8位)SD_TRAIN_DEPARTURE_DATE
        fields.append(datetime.now().strftime("%Y%m%d"))
        
        # 3. 出发地代码 (3位)SD_TRAIN_ORIGIN_LOCATION_CODE
        fields.append("   ")
        
        # 4. 出发城市 (20位)SD_TRAIN_ORIGIN_CITY
        fields.append("Beijing".ljust(20))
        
        # 5. 乘客数量 (2位)SD_TRAIN_PASSENGER_COUNT
        fields.append(f"{random.randint(1, 99):02d}")
        
        # 6. 车票类型 (1位)SD_TRAIN_TICKET_TYPE
        fields.append("0")
           
        """目的地代码和目的地城市批量生成5个,读取city_number.yaml文件"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        city_yaml_path = os.path.join(current_dir, "..", "config", "dictionaries", "city_number.yaml")
        with open(city_yaml_path, "r", encoding="utf-8") as f:
            city_dict = yaml.safe_load(f)
        # city_dict格式: {'BEJ': 'Beijing', ...}
        city_codes = list(city_dict.keys())
        city_names = list(city_dict.values())
        # 随机选取5个不同的城市
        selected_indices = random.sample(range(len(city_codes)), 5)
        seg_city_codes = [city_codes[i] for i in selected_indices]
        seg_city_names = [city_dict[code] for code in seg_city_codes]

        # 7. 目的地代码 (3位) SD_TRAIN_SEG_1_DEST_CODE
        fields.append(seg_city_codes[0])
        
        # 8. 目的地城市 (20位) SD_TRAIN_SEG_1_DEST_CITY
        fields.append(seg_city_names[0].ljust(20))

        # 火车号批量生成5个
        train_number_base = random.randint(100, 995)
        train_numbers = [f"G{train_number_base + i}" + " " * (8 - len(f"G{train_number_base + i}")) for i in range(5)]
        
        # 9. 第一段火车号 (8位)
        fields.append(train_numbers[0])

        # 10. 座位等级 (1位) SD_TRAIN_SEG_1_CLASS
        fields.append(random.choice("ABCDFV"))

        # 11. 第二段目的地代码 (3位) SD_TRAIN_SEG_2_DEST_CODE
        fields.append(seg_city_codes[1])

        # 12. 第二段目的地城市 (20位) SD_TRAIN_SEG_2_DEST_CITY
        fields.append(seg_city_names[1].ljust(20))

        # 13. 第二段火车号 (8位) SD_TRAIN_SEG_2_TRAIN_NUMBER
        fields.append(train_numbers[1])

        # 14. 第二段座位等级 (1位) SD_TRAIN_SEG_2_CLASS
        fields.append(random.choice("ABCDFV"))

        # 15. 第三段目的地代码 (3位) SD_TRAIN_SEG_3_DEST_CODE
        fields.append(seg_city_codes[2])

        # 16. 第三段目的地城市 (20位) SD_TRAIN_SEG_3_DEST_CITY
        fields.append(seg_city_names[2].ljust(20))

        # 17. 第三段火车号 (8位) SD_TRAIN_SEG_3_TRAIN_NUMBER
        fields.append(train_numbers[2])

        # 18. 第三段座位等级 (1位) SD_TRAIN_SEG_3_CLASS
        fields.append(random.choice("ABCDFV"))

        # 19. 第四段目的地代码 (3位) SD_TRAIN_SEG_4_DEST_CODE
        fields.append(seg_city_codes[3])

        # 20. 第四段目的地城市 (20位) SD_TRAIN_SEG_4_DEST_CITY
        fields.append(seg_city_names[3].ljust(20))

        # 21. 第四段火车号 (8位) SD_TRAIN_SEG_4_TRAIN_NUMBER
        fields.append(train_numbers[3])

        # 22. 第四段座位等级 (1位) SD_TRAIN_SEG_4_CLASS
        fields.append(random.choice("ABCDFV"))

        # 23. 第五段目的地代码 (3位) SD_TRAIN_SEG_5_DEST_CODE
        fields.append(seg_city_codes[4])

        # 24. 第五段目的地城市 (20位) SD_TRAIN_SEG_5_DEST_CITY
        fields.append(seg_city_names[4].ljust(20))

        # 25. 第五段火车号 (8位) SD_TRAIN_SEG_5_TRAIN_NUMBER
        fields.append(train_numbers[4])

        # 26. 第五段座位等级 (1位) SD_TRAIN_SEG_5_CLASS
        fields.append(random.choice("ABCDFV"))

        # 27. 段溢出标志 (1位) SD_TRAIN_SEG_OVERFLOW（已超5个火车段，固定值为1）
        fields.append("1")
        
        # 28. 最终目的地代码 (3位) SD_TRAIN_FINAL_DEST_CODE
        fields.append("SHA")
        
        # 29. 最终目的地城市 (20位) SD_TRAIN_FINAL_DEST_CITY
        fields.append("Shanghai".ljust(20))
        
        # 30. 火车描述 (30位)SD_TRAIN_DESCRIPTION
        fields.append("Train__descript".ljust(30))
        
        # 31. 填充字段 (7位)SD_TRAIN_FILLER
        fields.append(" " * 7)
        
        service_description = "".join(fields)
        
        # 确保长度正确
        if len(service_description) != 270:
            raise ValueError(f"服务描述长度错误: {len(service_description)},应为270位")
        
        return service_description
