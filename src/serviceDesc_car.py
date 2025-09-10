import random
from datetime import datetime, timedelta

class ServiceDescCar:
    """租车服务描述生成器类"""

    def generate_document_number(self) -> str:
        """【第6个参数,30位】生成文档号"""
        random_number = str(random.randint(10000000, 99999999))  # 8位随机数字
        doc_number = f"88{random_number}" + " " * 20
        return doc_number[:30]

    def generate_service_description(self, amount: float) -> str:
        """【第49个参数,270位】生成服务描述"""
        fields = []

        # 1. SD_CAR_RENTAL_COMPANY_CODE：2位，固定为EH
        fields.append("EH")

        # 2. SD_CAR_CONTRACT_NUMBER：15位，年月日+时间戳 12位 + 3位空格
        contract_number = datetime.now().strftime("%Y%m%d%H%M%S") + "   "
        fields.append(contract_number[:15])

        # 3. SD_CAR_VEHICLE_CLASS_CODE：1位，在C、E、X、F中随机1个
        fields.append(random.choice("CEXF"))

        # 4. SD_CAR_VEHICLE_TYP：30位，VERYGOOD+22个空格
        fields.append("VERYGOOD" + " " * 22)

        # 5. SD_CAR_PICK_UP_DATE：8位，YYYYMMDD
        pick_up_date = datetime.now()
        fields.append(pick_up_date.strftime("%Y%m%d"))

        # 6. SD_CAR_PICK_UP_TIME：4位，HHMM
        fields.append(pick_up_date.strftime("%H%M"))

        # 7. SD_CAR_PICK_UP_LOCATION_CODE：3位空格
        fields.append(" " * 3)

        # 8. SD_CAR_PICK_UP_LOCATION_CITY：20位，Beijing+13位空格
        fields.append("Beijing" + " " * 13)

        # 9. SD_CAR_RETURN_DATE：8位，YYYYMMDD，取提车日期+5天
        return_date = pick_up_date + timedelta(days=5)
        fields.append(return_date.strftime("%Y%m%d"))

        # 10. SD_CAR_RETURN_TIME：4位，HHMM
        fields.append(return_date.strftime("%H%M"))

        # 11. SD_CAR_RETURN_LOCATION_CODE：3位空格
        fields.append(" " * 3)

        # 12. SD_CAR_RETURN_LOCATION_CITY：20位，Shanghai+12位空格
        fields.append("Shanghai" + " " * 12)

        # 13. SD_CAR_RENTAL_DAYS：3位，固定：005
        fields.append("005")

        # 14. SD_CAR_MILEAGE_IND： 1位，固定：K
        fields.append(" ")

        # 15. SD_CAR_DRIVEN_DISTANCE：5位，固定00200
        fields.append("00000")

        # 16. SD_CAR_NO_SHOW_IND：1位，默认9
        fields.append("9")

        # 17. SD_CAR_NET_RENTAL_AMOUNT 15位
        fields.append("0" * 15)

        # 18. SD_CAR_NET_RENTAL_VAT_IND： 1位，写死1
        fields.append("0")

        # 19. SD_CAR_DISTRIBUTION_AMOUNT：15位
        fields.append("0" * 15)

        # 20. SD_CAR_DISTRIBUTION_VAT_IND：1位，写死0
        fields.append("0")

        # 21. SD_CAR_LIABLILITY_INS_AMOUNT：15位
        fields.append("0" * 15)

        # 22. SD_CAR_LIABLILITY_INS_VAT_IND：1位，写死1
        fields.append("0")

        # 23. SD_CAR_FULL_RISK_INS_AMOUNT：15位
        fields.append("0" * 15)

        # 24. SD_CAR_FULL_RISK_INS_VAT_IND：1位，写死1
        fields.append("0")

        # 25. SD_CAR_PASSENGER_INS_AMOUNT：15位
        fields.append("0" * 15)

        # 26. SD_CAR_PASSENGER_INS_VAT_IND：1位
        fields.append("0")

        # 27. SD_CAR_ADDITIONAL_INS_AMOUNT：15位
        fields.append("0" * 15)

        # 28. SD_CAR_ADDITIONAL_INS_VAT_IND：1位，写死0
        fields.append("0")

        # 29. SD_CAR_DISCOUNT_AMOUNT：15位
        fields.append("0" * 15)

        # 30. SD_CAR_DISCOUNT_VAT_IND：1位，写死1
        fields.append("0")

        # 31. SD_CAR_OTHERS_AMOUNT：15位
        fields.append("0" * 15)

        # 32. SD_CAR_OTHERS_VAT_IND,固定值1
        fields.append("0")

        # 33. SD_CAR_EXTRA_GAS_IND,固定值1
        fields.append("0")

        # 34. SD_CAR_LATE_RETURN_IND，固定值1
        fields.append("0")

        # 35. SD_CAR_EXTRA_MILEAGE_IND,固定值1
        fields.append("0")

        # 36. SD_CAR_ONE_WAY_IND,固定值1
        fields.append("0")

        # 37. SD_CAR_PARKING_VIOLATION_IND：1位，固定数为1
        fields.append("0")

        # 38. SD_CAR_DAMAGE_REPAIR_IND：1位，固定数为1
        fields.append("0")

        # 39. SD_CAR_FILLER：固定长度8个空格
        fields.append(" "*8)

        service_description = "".join(fields)
        if len(service_description) != 270:
            raise ValueError(f"服务描述长度错误: {len(service_description)},应为270位")
        return service_description
