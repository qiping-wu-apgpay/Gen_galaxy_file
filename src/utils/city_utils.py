#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
城市工具类
提供城市相关的公共方法，如获取城市三字码、城市名称等
"""

import os
import random
import yaml
from typing import List, Tuple, Optional

class CityUtils:
    """城市工具类"""
    _instance = None
    _initialized = False

    def __new__(cls, config_dir: str = "config"):
        """单例模式，确保只有一个实例"""
        if cls._instance is None:
            cls._instance = super(CityUtils, cls).__new__(cls)
        return cls._instance

    def __init__(self, config_dir: str = "config"):
        """初始化，加载城市数据
        使用单例模式，避免重复加载城市数据
        """
        if not self._initialized:
            self.config_dir = config_dir
            self._city_data = self._load_city_data()
            self._city_pairs = self._parse_city_pairs()
            CityUtils._initialized = True

    def _load_city_data(self) -> dict:
        """加载城市数据文件"""
        city_file = os.path.join(self.config_dir, "dictionaries", "city_number.yaml")
        with open(city_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _parse_city_pairs(self) -> List[Tuple[str, str]]:
        """解析城市数据为(三字码, 城市名)对的列表"""
        city_pairs = []
        for code, value in self._city_data.items():
            # value 格式可能是 "Shanghai  # 上海"
            city_name = value.split('#')[0].strip()
            if city_name:
                city_pairs.append((code, city_name))
        return city_pairs

    def get_random_city(self) -> Tuple[str, str]:
        """随机获取一个城市的三字码和名称
        Returns:
            Tuple[str, str]: (城市三字码, 城市名称)，如 ("SHA", "Shanghai")
        """
        return random.choice(self._city_pairs)

    def get_random_cities(self, count: int = 2) -> List[Tuple[str, str]]:
        """随机获取指定数量的不重复城市
        Args:
            count: 需要获取的城市数量
        Returns:
            List[Tuple[str, str]]: [(城市三字码1, 城市名称1), (城市三字码2, 城市名称2), ...]
        """
        return random.sample(self._city_pairs, min(count, len(self._city_pairs)))

    def get_city_by_code(self, code: str) -> Optional[str]:
        """根据城市三字码获取城市名称
        Args:
            code: 城市三字码
        Returns:
            Optional[str]: 城市名称，如果找不到则返回 None
        """
        value = self._city_data.get(code)
        if value:
            return value.split('#')[0].strip()
        return None

    def get_code_by_city(self, city_name: str) -> Optional[str]:
        """根据城市名称获取城市三字码
        Args:
            city_name: 城市名称
        Returns:
            Optional[str]: 城市三字码，如果找不到则返回 None
        """
        city_name = city_name.strip()
        for code, value in self._city_data.items():
            if value.split('#')[0].strip() == city_name:
                return code
        return None

    def get_all_cities(self) -> List[Tuple[str, str]]:
        """获取所有城市的三字码和名称
        Returns:
            List[Tuple[str, str]]: 所有城市的三字码和名称列表
        """
        return self._city_pairs.copy()

    def format_city_name(self, city_name: str, width: int = 20) -> str:
        """格式化城市名称，使其固定宽度（右侧补空格）
        Args:
            city_name: 城市名称
            width: 需要的宽度
        Returns:
            str: 格式化后的城市名称
        """
        return city_name.ljust(width)
