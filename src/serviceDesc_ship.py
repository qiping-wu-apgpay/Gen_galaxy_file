import random
from datetime import datetime, timedelta
from utils.city_utils import CityUtils

class ServiceDescShip:
    """邮轮服务描述生成器类"""

    def __init__(self, config_dir: str = "config"):
        """初始化"""
        self.city_utils = CityUtils(config_dir)

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

        # 1. SD_SHIP_COMPANY_NAME：30位，DREAM SEA+22个空格
        fields.append("DREAMSEA" + " " * 22)

        # 2. SD_SHIP_DEPARTURE_DATE：8位，YYYYMMDD
        fields.append(datetime.now().strftime("%Y%m%d"))

        # 3. SD_SHIP_ORIGIN_LOCATION_CODE：3位，固定为3个空格
        fields.append(" " * 3)

        # 4. SD_SHIP_ORIGIN_CITY：20位，从字典取值+补空格
        # 获取出发和到达城市
        origin_city, dest_city = self.city_utils.get_random_cities(2)
        origin_code, origin_name = origin_city
        fields.append(self.city_utils.format_city_name(origin_name))

        # 5. SD_SHIP_PASSENGER_COUNT：2位，01-99随机
        fields.append(f"{random.randint(1, 99):02d}")

        # 6. SD_SHIP_ARRIVAL_DATE：8位，出发日期+3天
        arrival_date = datetime.now() + timedelta(days=3)
        fields.append(arrival_date.strftime("%Y%m%d"))

        # 7. SD_SHIP_ARRIVAL_LOCATION_CODE：3位，固定为3个空格
        fields.append(" " * 3)

        # 8. SD_SHIP_ARRIVAL_CITY：20位
        dest_code, dest_name = dest_city
        fields.append(self.city_utils.format_city_name(dest_name))

        # 9. SD_SHIP_1：45位，VERYGOOD+37空格
        fields.append("VERYGOOD" + " " * 37)

        # 10. SD_SHIP_2：45位，补全45个空格
        fields.append(" " * 45)

        # 11. SD_SHIP_3：45位，补全45个空格
        fields.append(" " * 45)

        # 12. SD_SHIP_FILLER：41位，补全41个空格
        fields.append(" " * 41)

        service_description = "".join(fields)
        if len(service_description) != 270:
            raise ValueError(f"服务描述长度错误: {len(service_description)}, 应为270位")
        return service_description
