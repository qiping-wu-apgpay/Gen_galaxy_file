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
        """初始化，加载IATA代码"""
        self.config_dir = config_dir
        self.iata_codes = self._load_iata_codes()

    def _load_iata_codes(self) -> list:
        """加载IATA代码"""
        iata_file = os.path.join(self.config_dir, "dictionaries", "IATA_code.yaml")
        with open(iata_file, 'r', encoding='utf-8') as f:
            iata_data = yaml.safe_load(f)
        return [code.strip() for code in iata_data['IATA_codes']]

    def _generate_dn_lcc_prefix(self, file_type: str) -> str:
        """生成DN_LCC_PREFIX(3位)
            如果文件类型是BSP:这个参数可能的组合是:
            1. 随机三位数的IATA航空公司代码
            2. 三个字符的ICAO航空公司代码
            3. 两个字符+1个空格
        如果文件类型是MA:
        随机生成3个字母
        """
        if file_type == "B":
            choice = random.randint(1, 3)
            if choice == 1:
                # IATA航空公司代码
                return random.choice(self.iata_codes)
            elif choice == 2:
                # ICAO航空公司代码（模拟生成）
                return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
            else:
                # 两个字符+1个空格
                return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=2)) + ' '
        else:
            # MA类型：随机生成3个字母
            return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))

    def _generate_dn_lcc_filekey(self, file_type: str) -> str:
        """生成DN_LCC_FILEKEY(8位)
        如果文件类型是BSP:这个参数数是:
            5-7位数字字符混合。用空格填充到右侧,长度为8
            如果文件类型是MA:
            随机5个数字+3个空格
        """
        if file_type == "B":
            # 生成5-7位数字字符混合
            length = random.randint(5, 7)
            chars = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=length))
            return chars + ' ' * (8 - length)
        else:
            # MA类型：随机5个数字+3个空格
            nums = ''.join(random.choices('0123456789', k=5))
            return nums + ' ' * 3

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
            prefix = self._generate_dn_lcc_prefix(file_type)
            filekey = self._generate_dn_lcc_filekey(file_type)
            filler = ' ' * 19  # DN_LCC_FILLER固定19个空格
            doc_number = prefix + filekey + filler
            return doc_number[:30]
        """【第6个参数,30位】生成文档号
        包含三个部分：
        1. DN_LCC_PREFIX: AN类型,3位
        2. DN_LCC_FILEKEY: AN类型,8位
        3. DN_LCC_FILLER: AN类型,19位空格
        """
        prefix = self._generate_dn_lcc_prefix(file_type)
        filekey = self._generate_dn_lcc_filekey(file_type)
        filler = ' ' * 19  # DN_LCC_FILLER固定19个空格
        doc_number = prefix + filekey + filler
        return doc_number

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
        """生成2位的税费类型
        从XF、MF中随机取一个
        """
        tax_type = random.choice(['XF', 'MF'])
        if len(tax_type) != 2:
            raise ValueError(f"税费类型长度错误: {len(tax_type)}, 应为2位")
        return tax_type

    def _generate_flight_number(self) -> str:
        """生成4位航班号
        格式:1个字母+3个数字
        """
        letter = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        numbers = ''.join(random.choices('0123456789', k=3))
        flight_number = letter + numbers
        if len(flight_number) != 4:
            raise ValueError(f"航班号长度错误: {len(flight_number)}, 应为4位")
        return flight_number

    def generate_service_description(self, amount: float) -> str:
        """
        【第49个参数,270位】生成服务描述

        为什么这里的长度会有问题？

        主要原因在于IATA_code.yaml中的IATA代码有可能不是3位，而是2位（如"ZH"），
        但本字段要求严格3位长度。如果直接用2位字符串填充，最终拼接的服务描述长度就会少1位，
        导致整体长度不足270位。

        解决方法：需要保证所有IATA相关字段（如出发地、目的地、航空公司）都严格为3位，
        如果不足3位则右侧补空格。

        下面代码已修正此问题。
        """
        fields = []

        # 1. SD_FLIGHT_DEPARTURE_DATE：8位，必须包含第一个航段的出发日期
        departure_date = datetime.now() + timedelta(days=random.randint(1, 30))
        fields.append(departure_date.strftime("%Y%m%d"))

        # 2. SD_FLIGHT_ORIGIN_LOCATION：3位，从IATA_code.yaml中随机取一个，需补足3位
        origin_code = random.choice(self.iata_codes)
        origin_code = origin_code.ljust(3)[:3]
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
        available_codes = [code for code in self.iata_codes if code != origin_code.strip()]
        dest_code = random.choice(available_codes)
        dest_code = dest_code.ljust(3)[:3]
        fields.append(dest_code)

        # 11. SD_FLIGHT_SEG_1_AIRLINE：3位，从IATA_code.yaml中随机取一个，需补足3位
        airline_code = random.choice(self.iata_codes)
        airline_code = airline_code.ljust(3)[:3]
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