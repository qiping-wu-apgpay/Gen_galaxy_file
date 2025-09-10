#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公共交易数据生成器
负责生成交易数据的公共部分：
1. 文件头部 (74位)
2. 交易记录的公共字段 (1-5, 7-48, 50字段)
3. 文件尾部 (7位)
"""

import os
import yaml
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any

from txn_errors import FileTypeError


class CommonTransaction:
    """公共交易数据生成器类"""
    
    def __init__(self, config_dir: str = "config"):
        """初始化生成器"""
        self.config_dir = config_dir
        self.load_configs()
        self.transaction_counter = 1
        self.last_generated_amount = 0.0
    
    def load_configs(self):
        """加载配置文件"""
        dict_dir = os.path.join(self.config_dir, "dictionaries")
        
        # 加载卡号信息
        with open(os.path.join(dict_dir, "card_numbers.yaml"), 'r', encoding='utf-8') as f:
            card_data = yaml.safe_load(f)
            # 文件类型为BSP的卡片信息
            b_card = card_data['card_partners']['B']['UATP']['card1']
            self.b_type_cards = [b_card['PAN']]
            self.b_type_expiry = b_card['Expiry']
            
            # 文件类型为MA的卡片信息
            m_card = card_data['card_partners']['MA']['MC_Card']['card1']
            self.m_type_cards = [m_card['PAN']]
            self.m_type_expiry = m_card['Expiry']
        
        # 加载旅客姓名
        with open(os.path.join(dict_dir, "traveller_names.yaml"), 'r', encoding='utf-8') as f:
            self.traveller_names = yaml.safe_load(f)['traveller_names']
    
    def generate_header(self, file_type: str) -> str:
        """生成公共文件头信息 (74位)"""
        fields = []
        fields.append("H")  # RECORD_TYPE (1位)
        fields.append(file_type)  # FILE_TYPE (1位)
        
        # PARTNER_ID (12位)
        partner_id = "999993243243" if file_type == "B" else "918171615141"
        fields.append(partner_id)
        fields.append(datetime.now().strftime("%Y%m%d"))  # PROCESSING_DATE (8位)
        fields.append("V01.01")  # VERSION (6位)
        fields.append("    ")  # RELEASE (4位)
        fields.append("AU ")  # COUNTRY_CODE (3位)
        fields.append("APGS")  # ACQUIRER_PREFIX (4位)
        fields.append("000")  # ACQUIRER_PROCESSING_PAGE (3位)
        fields.append("TP")  # CREDIT_CARD_IND (2位)
        fields.append("     ")  # BOS_ID (5位)
        
        # FILE_ID (25位)--当前时间戳取14位
        now = datetime.now()
        date_part = now.strftime("%Y%m%d")
        time_part = now.strftime("%H%M%S")
        fixed_part = "           "  # 11位空格
        file_id = f"{date_part}{time_part}{fixed_part}"
        fields.append(file_id)
        
        return "".join(fields)
    
    def generate_common_fields(self, file_type: str) -> list:
        """生成交易记录的公共字段(1-5, 7-48, 50字段)"""
        fields = []
        
        # 1. RECORD_TYPE (1位)
        fields.append("D")
        
        # 2. TRANSACTION_TYPE (1位)
        if file_type == "B":
            transaction_type = "F"  # B类型文件只能是F类型交易
        else:  # M类型文件可以有多种交易类型
            transaction_type = random.choice(["A", "C", "H", "F", "O", "S", "T"])
        fields.append(transaction_type)
        
        # 3. CARD_NUMBER (19位)
        if file_type == "B":
            card_number = "0000" + random.choice(self.b_type_cards)  # B类型卡号前缀4个0
            expiry = self.b_type_expiry
        else:
            card_number = "000" + random.choice(self.m_type_cards)   # M类型卡号前缀3个0
            expiry = self.m_type_expiry
        fields.append(card_number)
        
        # 4. EXPIRY_DATE (4位) - 从YYMM转为MMYY
        expiry_formatted = expiry[2:4] + expiry[0:2]
        fields.append(expiry_formatted)
        
        # 5. DOCUMENT_NUMBER_FORMAT (1位)
        doc_format = "1" if transaction_type == "F" else "3"
        fields.append(doc_format)
        
        # 7-48字段
        fields.extend(self._generate_fields_7_to_48())
        
        # 50. USAGE_CODE (1位)
        fields.append("0")
        
        return fields
    
    def _generate_fields_7_to_48(self) -> list:
        """生成7-48字段"""
        fields = []
        
        # 7. PURCHASE_DATE (8位)
        purchase_date = (datetime.now() - timedelta(days=random.randint(1, 7))).strftime("%Y%m%d")
        fields.append(purchase_date)
        
        # 8. TRAVELLER_NAME (30位)
        fields.append(random.choice(self.traveller_names).ljust(30))
        
        # 9. TRANSACTION_SERIAL_NUMBER (32位)
        current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
        serial_number = f"GALAXYSERIAL{current_datetime}{str(self.transaction_counter).zfill(3)}"
        fields.append(serial_number.ljust(32))
        self.transaction_counter += 1
        
        # 10-17. 金额相关字段
        fields.extend(self._generate_amount_fields())
        
        # 18-26. 固定69个0
        fields.append("0" * 69)
        
        # 27-48. 商户和代理相关字段
        fields.extend(self._generate_merchant_fields())
        
        return fields
    
    def _generate_amount_fields(self) -> list:
        """生成金额相关字段(10-17字段)"""
        fields = []
        
        # 10. TRANSACTION_CURRENCY_CODE (3位)
        fields.append("036")
        
        # 11. TRANSACTION_SIGN (1位)
        fields.append("+")
        
        # 12. TRANSACTION_AMOUNT (15位)，金额精确到分
        amount_str = f"{int(self.last_generated_amount * 100):015d}"
        fields.append(amount_str)
        
        # 13. NET_AMOUNT_NON_VATABLE (15位)
        fields.append(amount_str)
        
        # 14. NET_AMOUNT_VATABLE_1 (15位)
        vatable_amount = int(self.last_generated_amount * 100 * 0.9)
        fields.append(f"{vatable_amount:015d}")
        
        # 15. VAT_1_AMOUNT (9位)
        vat_amount = int(vatable_amount * 0.16)
        fields.append(f"{vat_amount:09d}")
        
        # 16. VAT_1_PERCENTAGE (5位)
        fields.append("00050")
        
        # 17. VAT_1_IND (1位)
        fields.append("1")
        
        return fields
    
    def _generate_merchant_fields(self) -> list:
        """生成商户和代理相关字段(27-48字段)"""
        fields = []
        
        # 27. APPROVAL_CODE (6位)
        fields.append("      ")
        
        # 28. MERCHANT_NAME (22位)
        fields.append("APG_QA".ljust(22))
        
        # 29. MERCHANT_CITY (13位)
        fields.append("Shanghai".ljust(13))
        
        # 30. MERCHANT_ZIP_CODE (5位)
        fields.append("     ")
        
        # 31. MERCHANT_STATE_CODE (3位)
        fields.append("   ")
        
        # 32. MERCHANT_IATA_NUMBER (8位)
        fields.append("12345678")
        
        # 33-35. MERCHANT相关字段 (17位各)
        for _ in range(3):
            fields.append(" " * 17)
        
        # 36. AGENCY_DOSSIER_NUMBER (20位)
        dossier_num = f"DOSSIER888{random.randint(10000, 99999)}     "
        fields.append(dossier_num[:20])
        
        # 37. AGENCY_DELIVERY_NOTE_NUMBER (20位)
        fields.append("DELIVERY10052025    ")
        
        # 38-47. DBI字段系列
        dbi_prefixes = ["PK", "DS", "KS", "AE", "IK", "BD", "PR", "AU", "AK", "RZ"]
        for prefix in dbi_prefixes:
            if prefix == "BD":
                # 10位：当前时间的年月日(8位) + 两位空格
                dbi_field = datetime.now().strftime("%Y%m%d") + "  "
                fields.append(dbi_field)
            else:
                dbi_field = f"{prefix}888{random.randint(10000, 99999)}       "
                fields.append(dbi_field[:17])
        
        # 48. FILLER (9位)
        fields.append("         ")
        
        return fields
    
    def generate_trailer(self, file_type: str, record_count: int) -> str:
        """生成公共文件尾信息 (7位)"""
        record_type = "T"  # RECORD_TYPE (1位)
        count_str = f"{record_count:05d}"  # RECORD_COUNT (5位)
        return record_type + file_type + count_str
    
    def generate_standard_filename(self, file_type: str) -> str:
        """生成标准格式的文件名"""
        now = datetime.now()
        year_2digit = now.strftime("%y")
        timestamp_12 = now.strftime(f"{year_2digit}%m%d%H%M%S")
        
        if file_type == "B":
            filename = f"APGPay.BSP_RECORD_AU-NZ-DEV.{timestamp_12}"
        else:
            filename = f"APGPay.MA_RECORD_AU-NZ-DEV.{timestamp_12}"
        
        return filename