#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
其他业务描述生成器
"""

import random

class ServiceDescOther:
    """其他业务描述生成器类"""

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

        # 1. SD_OTHER_FILLER：3位，固定3个空格
        fields.append(" " * 3)

        # 2. SD_OTHER_1：45位，OTHER_DESC+35个空格
        fields.append("OTHER_DESC" + " " * 35)

        # 3. SD_OTHER_2：45个空格
        fields.append(" " * 45)

        # 4. SD_OTHER_3：45个空格
        fields.append(" " * 45)

        # 5. SD_OTHER_MATCHING_CRITERIA：50个空格
        fields.append(" " * 50)

        # 6. SD_OTHER_FILLER：82个空格
        fields.append(" " * 82)

        service_description = "".join(fields)
        if len(service_description) != 270:
            raise ValueError(f"服务描述长度错误: {len(service_description)}, 应为270位")
        return service_description