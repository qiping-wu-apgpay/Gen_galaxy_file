#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
机票业务描述生成器
"""
import random
import yaml
import os
from datetime import datetime, timedelta
from typing import Tuple

class ServiceDescFlight:
    """机票业务描述生成器类"""
    
    def __init__(self, config_dir: str = "config"):
        """初始化机票业务描述生成器"""
        # 加载IATA代码
        iata_codes_path = os.path.join(config_dir, "dictionaries/IATA_code.yaml")
        with open(iata_codes_path, "r", encoding="utf-8") as f:
            self.iata_codes = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]
    
    def generate_document_number(self, file_type: str = "B") -> str:
        """
        【第6个参数,30位】生成文档号
        - 如果文件类型是M: 888+10位随机数+17个空格
        - 否则: DN_LCC_PREFIX(3位) + DN_LCC_FILEKEY(8位) + 19位空格
        """
        if file_type == "M":
            random_digits = ''.join(random.choices('0123456789', k=10))
            doc_number = "888" + random_digits + " " * 17
            return doc_number[:30]
        else:
            # doc_number: 3位IATA+8位filekey+19位空格，总共30位
            
            # 从已加载的IATA代码中随机取一个3位IATA
            valid_codes = [code for code in self.iata_codes if len(code.strip()) == 3]
            if not valid_codes:
                # 如果没有找到合适的代码，生成一个随机的3位代码
                prefix = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
            else:
                prefix = random.choice(valid_codes).strip()
            if file_type == "B":
                # 生成8位filekey
                next7 = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=7))
                filekey = next7 + ' '  # 8位
            else:
                # 生成8位filekey，仅数字
                filekey = ''.join(random.choices('0123456789', k=8))
            filler = ' ' * 19
            doc_number = prefix + filekey + filler
            return doc_number[:30]

    def _generate_random_tax_amount(self) -> str:
        """生成13位的税费金额
        格式:由10为0 + 3个随机数字组成
        """
        amount = ''.join(random.choices('0123456789', k=3))
        tax_amount = '0' * 10 + amount
        if len(tax_amount) != 13:
            raise ValueError(f"税费金额长度错误: {len(tax_amount)}, 应为13位")
        return tax_amount

    def _generate_tax_type(self) -> str:
        """生成2位的税费类型、从XF、MF中随机取一个"""
        tax_type = random.choice(['XF', 'MF'])
        if len(tax_type) != 2:
            raise ValueError(f"税费类型长度错误: {len(tax_type)}, 应为2位")
        return tax_type

    def _generate_flight_number(self) -> str:
        """生成4位航班号,格式:1个字母+3个数字
        """
        letter = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        numbers = ''.join(random.choices('0123456789', k=3))
        flight_number = letter + numbers
        if len(flight_number) != 4:
            raise ValueError(f"航班号长度错误: {len(flight_number)}, 应为4位")
        return flight_number

    def generate_service_description(self, amount: float) -> str:
        """第49个参数,270位】生成服务描述"""   
        fields = []

        # 1. SD_FLIGHT_DEPARTURE_DATE：8位，必须包含第一个航段的出发日期
        departure_date = datetime.now() + timedelta(days=random.randint(1, 30))
        fields.append(departure_date.strftime("%Y%m%d"))

        # 2. SD_FLIGHT_ORIGIN_LOCATION：3位，从IATA_code.yaml中随机取一个，需补足3位
        valid_codes = [code for code in self.iata_codes if len(code.strip()) == 3]
        if not valid_codes:
            # 如果没有找到合适的出发地代码，生成一个随机的3位代码
            origin_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
        else:
            origin_code = random.choice(valid_codes).strip()
        fields.append(origin_code)

        # 3. SD_FLIGHT_CRS：4位，默认4个空格
        fields.append(" " * 4)

        # 4. SD_FLIGHT_PASSENGER_COUNT：2位，01-10之间随机取值
        passenger_count = f"{random.randint(1,10):02d}"
        if len(passenger_count) != 2:
            raise ValueError(f"乘客数量长度错误: {len(passenger_count)}, 应为2位")
        fields.append(passenger_count)

        # 5-9. 五组税费金额和类型
        for _ in range(5):
            fields.append(self._generate_random_tax_amount())  # TAX_N_AMOUNT：13位
            fields.append(self._generate_tax_type())          # TAX_N_TYPE：2位

        # 10. SD_FLIGHT_SEG_1_DESTINATION：3位，从IATA_code.yaml中随机取一个（不能与出发地相同），需补足3位
        valid_codes = [code for code in self.iata_codes if len(code.strip()) == 3 and code.strip() != origin_code]
        if not valid_codes:
            # 如果没有找到合适的目的地代码，生成一个随机的3位代码
            dest_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
        else:
            dest_code = random.choice(valid_codes).strip()
        fields.append(dest_code)

        # 11. SD_FLIGHT_SEG_1_AIRLINE：3位，从IATA_code.yaml中随机取一个，需补足3位
        valid_codes = [code for code in self.iata_codes if len(code.strip()) == 3]
        if not valid_codes:
            # 如果没有找到合适的航空公司代码，生成一个随机的3位代码
            airline_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
        else:
            airline_code = random.choice(valid_codes).strip()
        fields.append(airline_code)

        # 12. SD_FLIGHT_SEG_1_FLIGHT：4位，生成航班号
        fields.append(self._generate_flight_number())

        # 13. SD_FLIGHT_SEG_1_CLASS：1位，随机取一个舱位代码（字母）
        class_code = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        if len(class_code) != 1:
            raise ValueError(f"舱位代码长度错误: {len(class_code)}, 应为1位")
        fields.append(class_code)

        # 14. 中间有19到64号字段，这里用空格填充
        # 计算需要的空格数：当前已有13个字段，还需要填充到第64个字段
        # 每个字段的长度：8+3+4+2+(13+2)*5+3+3+4+1 = 89
        # 需要填充的空格数：270-89-3-15-3 = 160
        fields.append(" " * 147)

        # 15. SD_FLIGHT_SEG_OVERFLOW：1位，写0
        fields.append("0")

        # 16. SD_FLIGHT_TICKET_IND：在U和E里面随机选一个
        fields.append(random.choice("UE"))

        # 17. SD_FLIGHT_TOUR_CODE：15位空格
        fields.append(" " * 15)

        # 18. SD_FLIGHT_FILLER：3位空格
        fields.append(" " * 3)

        service_description = "".join(fields)
        if len(service_description) != 270:
            # 打印每个字段的内容和长度以便调试
            field_lengths = [len(field) for field in fields]
            field_contents = [f"'{field}'" for field in fields]
            expected_lengths = [8, 3, 4, 2, 13, 2, 13, 2, 13, 2, 13, 2, 13, 2, 3, 3, 4, 1, 147, 1, 1, 15, 3]
            field_names = [
                "出发日期", "出发地", "CRS", "乘客数", 
                "税费1金额", "税费1类型", "税费2金额", "税费2类型",
                "税费3金额", "税费3类型", "税费4金额", "税费4类型",
                "税费5金额", "税费5类型", 
                "目的地", "航空公司", "航班号", "舱位",
                "中间填充", "溢出标志", "票据标志", "行程代码", "结尾填充"
            ]
            print("\n字段长度检查:")
            for i, (name, content, actual, expected) in enumerate(zip(field_names, field_contents, field_lengths, expected_lengths)):
                print(f"{name}: 内容={content}, 实际长度={actual}, 期望长度={expected}")
                if actual != expected:
                    print(f">>> 字段 {name} 长度错误! <<<")
            raise ValueError(f"服务描述长度错误: {len(service_description)}, 应为270位")
        return service_description