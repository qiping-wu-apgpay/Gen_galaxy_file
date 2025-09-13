# Transaction Data Generator 交易数据生成器

## 项目简介

这是一个用于生成交易数据文件的Python工具，支持多种业务类型的交易数据生成。可以在单个文件中包含多个业务类型的交易记录，根据指定的业务规则和格式生成标准的纯文本交易数据文件。

## 项目结构

```
Transaction_Data_Generator/
├── config/                    # 配置文件目录
│   ├── business_types/        # 业务类型配置
│   │   └── hotel.yaml        # 酒店业务配置
│   ├── dictionaries/          # 字典文件
│   │   ├── card_numbers.yaml  # 卡号字典
│   │   ├── hotel_names.yaml   # 酒店名称字典
│   │   └── traveller_names.yaml # 旅客姓名字典
│   └── generator_config.yaml  # 主配置文件
├── src/                       # 源代码目录
│   ├── transaction_generator.py # 主生成器
│   └── logger.py             # 日志记录模块
├── output/                    # 输出文件目录
├── log/                       # 日志文件目录
├── generate_data.py           # 命令行生成工具
├── sample_config.json         # 示例配置文件
└── README.md                  # 说明文档
```

## 文件格式规范

### 1. 文件头信息 (74字符)
- RECORD_TYPE: H (固定值)
- FILE_TYPE: B或M (业务类型)
- PARTNER_ID: 读取配置文件
- PROCESSING_DATE: 当前日期 (YYYYMMDD)
- VERSION: V01.01 (固定值)
- 其他固定字段...

### 2. 交易信息 (850字符)
- 前48个字段 (579字符): 公共交易信息
- 第49个字段 (270字符): SERVICE_DESCRIPTION (酒店业务详细信息)
- 第50个字段 (1字符): USAGE_CODE (固定为0)

### 3. 文件尾信息 (7字符)
- RECORD_TYPE: T (固定值)
- FILE_TYPE: B或M (与头部一致)
- RECORD_COUNT: 总记录数 (5位数字)

## 使用方法

### 方法1: 命令行工具 (推荐)

#### 1.1 创建配置文件并生成
```bash
# 创建示例配置文件
python3 generate_data.py --create-sample

# 使用配置文件生成
python3 generate_data.py --config sample_config.json
```

#### 1.2 直接使用命令行参数
```bash
# 生成单一业务类型
python3 generate_data.py --type M --business hotel:5 --output my_data

# 生成多个业务类型组合
python3 generate_data.py --type M --business hotel:3 --business hotel:2
```

#### 1.3 查看帮助信息
```bash
python3 generate_data.py --help
```

### 方法2: 编程调用

```python
from src.transaction_generator import TransactionDataGenerator

generator = TransactionDataGenerator(config_dir="config")
filepath = generator.generate_file(
    business_type="hotel",
    file_type="M",
    transaction_count=5,
    amount_range=(200.0, 800.0)
)
```

### 方法3: 多业务类型混合生成

```python
from generate_data import MultiBusinessGenerator

generator = MultiBusinessGenerator()
business_configs = [
    {"business_type": "hotel", "count": 3},
    {"business_type": "hotel", "count": 2}
]
filepath = generator.generate_mixed_file("M", business_configs, "mixed_data")
```

## 配置说明

### 主配置文件 (config/generator_config.yaml)
包含默认的PARTNER_ID和各种字段的配置规则。

### 酒店业务配置 (config/business_types/hotel.yaml)
定义酒店业务的特殊字段结构，包括34个子字段的详细配置。

### 字典文件
- `card_numbers.yaml`: B类型和M类型的卡号列表
- `hotel_names.yaml`: 酒店名称和城市名称列表
- `traveller_names.yaml`: 旅客姓名列表

## 配置文件格式

### JSON配置文件示例（支持注释）
```json
{
  // 文件类型：B (Business Type B) 或 M (Business Type M)
  "file_type": "M",
  
  // 业务类型配置列表
  "business_types": [
    {
      // 业务类型名称 (目前支持: hotel)
      "business_type": "hotel",
      // 交易记录数量
      "count": 3
    },
    {
      // 第二批酒店交易配置
      "business_type": "hotel", 
      "count": 2
    }
  ]
  
  // 使用说明：
  // 支持 // 风格的注释，方便配置文件的维护和理解
}
```

**注意**: 
- 我们的生成器支持在JSON配置文件中使用 `//` 风格的注释，这样可以更好地说明每个配置项的含义
- 交易金额会自动在100-2000澳元范围内随机生成，无需手动配置

## 生成示例

生成的文件格式示例：
```
HM91817161514120250909V01.01    AU APGS000TP     2025090900000000000000001
DA000551234567890123408323DOC202509091131487314...
DC000561234567890123408323DOC202509091131488147...
DT000441234567890123408323DOC202509091131485245...
TM00005
```

## 命令行使用示例

```bash
# 1. 创建示例配置
python3 generate_data.py --create-sample

# 2. 使用配置文件生成 (自动文件名)
python3 generate_data.py --config sample_config.json
# 生成文件: APGPay.MA_RECORD.250909115700

# 3. 命令行快速生成 (B类型，自动文件名)
python3 generate_data.py --type B --business hotel:5
# 生成文件: APGPay.BSP_RECORD.250909115725

# 4. 使用自定义文件名
python3 generate_data.py --type M --business hotel:3 --output my_hotel_data
# 生成文件: my_hotel_data.txt

# 5. 混合多种配置 (注意：每个业务类型需要单独的--business参数)
python3 generate_data.py --type M --business hotel:3 --business hotel:2
# 生成文件: APGPay.MA_RECORD.250909115730

# 6. 查看帮助
python3 generate_data.py --help
```

### 文件命名规则说明
- **无自定义文件名时**: 自动使用标准格式 `APGPay.{业务类型}_RECORD.{时间戳}`
- **有自定义文件名时**: 使用用户指定的名称（自动添加.txt扩展名）
- **时间戳格式**: YYMMDDHHMMSS (12位，年份使用后2位)

## 注意事项

1. 确保Python 3.6+环境
2. 需要安装PyYAML: `pip install pyyaml`
3. 输出文件会自动保存到output目录
4. **标准文件名格式**:
   - B类型: `APGPay.BSP_RECORD_AU-NZ-DEV.{12位时间戳}` (如: APGPay.BSP_RECORD_AU-NZ-DEV.250909115700)
   - M类型: `APGPay.MA_RECORD_AU-NZ-DEV.{12位时间戳}` (如: APGPay.MA_RECORD_AU-NZ-DEV.250909115700)
   - 时间戳格式: YYMMDDHHMMSS (年取后2位，如2025年显示25)
   - 自定义文件名: 使用 `--output` 参数可指定自定义名称
5. 每次运行会生成新文件，不会覆盖现有文件
6. **交易金额自动随机生成**：范围为100-2000澳元，无需手动配置
7. **日志记录**：
   - 所有操作都会记录到log目录下的日志文件中
   - 日志文件格式：`transaction_generator_YYYYMMDD.log`
   - 记录内容包括：文件生成信息、格式验证结果、错误信息等

## 扩展其他业务类型

要添加新的业务类型，需要：
1. 在`config/business_types/`目录下创建新的YAML配置文件
2. 定义该业务类型的特殊字段结构
3. 如需要，添加对应的字典文件

## 问题排查

如果遇到问题：
1. 检查Python版本是否为3.6+
2. 确认所有配置文件格式正确
3. 查看控制台输出的详细错误信息
4. 检查文件权限，确保可以写入output目录
