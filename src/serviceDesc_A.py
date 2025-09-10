#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
服务费业务描述生成器
"""

import random
from datetime import datetime

class ServiceDescA:
    """服务费业务描述生成器类"""

    def __init__(self):
        """初始化"""
        self._doc_counter = 0  # 用于生成自增的文档号

    def generate_document_number(self) -> str:
        """【第6个参数,30位】生成文档号
        格式:88 + 8位随机数字 + 20位空格
        """
        random_number = str(random.randint(10000000, 99999999))  # 8位随机数字
        doc_number = f"88{random_number}" + " " * 20
        return doc_number[:30]

    def generate_service_description(self, amount: float) -> str:
        """【第49个参数,270位】生成服务描述"""
        fields = []

        # 1. SD_FEE_ORIGINATOR：1位，在C、F、H、O、S、T里面随机取
        originator = random.choice("CFHOST")
        fields.append(originator)

        # 2. SD_FEE_SERVICE_QUALIFIER：3位
        # 当SD_FEE_ORIGINATOR=O时，固定为???，其他时，固定为3个空格
        fields.append("???" if originator == "O" else " " * 3)

        # 3. SD_FEE_DOC_NUMBER_FORMAT：1位
        fields.append(str(random.choice([0, 1])))

        # 4. SD_FEE_REL_DOC_NUMBER：30位
        # 根据0和1判断,前面8位是年月日 + 两位随机数 + 88 + 后面3位自增数 + 15个空格
        doc_number_format = int(fields[2])
        if doc_number_format == 0:
            rel_doc_number = " " * 30
        else:
            random_digits = "".join([str(random.randint(0, 9)) for _ in range(7)])
            rel_doc_number = "888" + random_digits + " " * 20
            rel_doc_number = rel_doc_number[:30]
        fields.append(rel_doc_number)

        # 5. SD_FEE_CRS：4位，空格
        fields.append(" " * 4)

        # 6. SD_FEE_TITLE：45位，DESCFEE+38位空格
        fields.append("DESCFEE" + " " * 38)

        # 7. SD_FEE_MATCHING_CRITERIA：50位空格
        fields.append(" " * 50)

        # 8. SD_FEE_FILLER：136位空格
        fields.append(" " * 136)

        service_description = "".join(fields)
        if len(service_description) != 270:
            raise ValueError(f"服务描述长度错误: {len(service_description)}, 应为270位")
        return service_description
