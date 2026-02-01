# 数据驱动测试使用指南

## 概述

本项目已集成数据驱动测试功能，允许从外部数据源（CSV、JSON、YAML等）读取测试数据，实现测试逻辑与测试数据的分离。

## 核心功能

### 1. 数据源支持
- **CSV文件**：支持从CSV文件读取表格形式的测试数据
- **JSON文件**：支持从JSON文件读取结构化测试数据
- **YAML文件**：支持从YAML文件读取配置式测试数据
- **Excel文件**：支持从Excel文件读取复杂测试数据（需要安装pandas）

### 2. 数据类型自动转换
- 字符串 → 整数
- 字符串 → 浮点数
- 字符串 → 布尔值
- 自动处理空值

## 使用方法

### 1. 创建数据文件

#### CSV格式示例 (test_data.csv)
```csv
wifi_name,password,description
inmoglass,20210108,公司主WiFi
inmoglass_backup,20210108,公司备用WiFi
TestNetwork,Test123456,测试网络
```

#### JSON格式示例 (test_data.json)
```json
[
  {
    "wifi_name": "inmoglass",
    "password": "20210108",
    "description": "公司主WiFi",
    "expected_result": "连接成功"
  },
  {
    "wifi_name": "TestNetwork", 
    "password": "Test123456",
    "description": "测试网络",
    "expected_result": "连接成功"
  }
]
```

#### YAML格式示例 (test_data.yaml)
```yaml
- wifi_name: "inmoglass"
  password: "20210108"
  description: "公司主WiFi"
  expected_result: "连接成功"
- wifi_name: "TestNetwork"
  password: "Test123456" 
  description: "测试网络"
  expected_result: "连接成功"
```

### 2. 在测试中使用数据

#### 基本用法
```python
from common.data_provider import DataProvider

# 从CSV文件加载数据
csv_data = DataProvider.load_from_csv("test_data.csv")

# 从JSON文件加载数据
json_data = DataProvider.load_from_json("test_data.json")

# 从YAML文件加载数据
yaml_data = DataProvider.load_from_yaml("test_data.yaml")
```

#### 参数化测试用法
```python
import pytest
from common.data_provider import DataProvider

class TestDataDriven:
    @pytest.mark.parametrize("test_data", 
        DataProvider.load_from_json("test_data.json"),
        ids=lambda x: x["description"])  # 使用description作为测试ID
    def test_wifi_connection(self, test_data):
        wifi_name = test_data["wifi_name"]
        password = test_data["password"]
        expected_result = test_data["expected_result"]
        
        # 执行测试逻辑
        # ...
```

### 3. 实际测试示例

在 `scripts/phone/android/inmo_go/test_data_driven.py` 文件中提供了完整的数据驱动测试示例。

## 目录结构

```
inmo-test/
├── common/
│   └── data_provider.py                    # 数据提供者类
├── data/                                   # 测试数据目录
│   ├── wifi_test_data.csv
│   ├── glasses_connection_test_data.json
│   └── translation_test_data.yaml
├── scripts/
│   └── phone/
│       └── android/
│           └── inmo_go/
│               ├── test_data_driven.py                    # 数据驱动测试示例
│               ├── test_glasses_connection_data_driven.py # 眼镜连接数据驱动测试
│               └── test_translation_data_driven.py        # 翻译功能数据驱动测试
└── DATA_DRIVEN_TEST_GUIDE.md              # 本指南
```

## 最佳实践

### 1. 数据文件管理
- 将测试数据文件存放在 `data/` 目录中
- 使用有意义的文件名
- 为敏感数据使用占位符或环境变量

### 2. 数据结构设计
- 使用一致的字段名
- 为每个测试数据添加描述字段
- 包含优先级字段用于测试排序

### 3. 错误处理
- 验证数据文件是否存在
- 处理数据格式错误
- 提供有意义的错误消息

## 运行测试

### 运行所有数据驱动测试
```bash
pytest scripts/phone/android/inmo_go/test_data_driven.py
```

### 运行特定的数据驱动测试
```bash
pytest scripts/phone/android/inmo_go/test_data_driven.py::TestDataDriven::test_connect_wifi_with_csv_data
```

## 与Allure报告集成

数据驱动测试完全兼容Allure报告功能：

```python
@allure.title("数据驱动的WiFi连接测试")
@allure.description("使用外部数据源测试WiFi连接功能")
@allure.tag("WiFi测试", "数据驱动", "功能测试")
@pytest.mark.parametrize("test_data", [...])
def test_wifi_connection(self, test_data):
    with allure.step(f"使用数据: {test_data['description']}"):
        # 测试逻辑
        pass
```

## 扩展功能

### 1. 数据验证
在使用测试数据前进行验证：

```python
def validate_test_data(data):
    required_fields = ['wifi_name', 'password']
    for item in data:
        for field in required_fields:
            if field not in item:
                raise ValueError(f"缺少必需字段: {field}")
```

### 2. 动态数据生成
结合随机数据生成库创建动态测试数据：

```python
import random
import string

def generate_test_data(count=5):
    data = []
    for i in range(count):
        data.append({
            "wifi_name": f"TestWiFi_{i}",
            "password": ''.join(random.choices(string.ascii_letters + string.digits, k=8)),
            "description": f"随机生成的WiFi测试数据 {i+1}"
        })
    return data
```

## 注意事项

1. **依赖项**：使用Excel数据源需要安装pandas和openpyxl
2. **性能**：大量测试数据可能影响测试执行时间
3. **维护**：确保测试数据文件与测试逻辑保持同步
4. **安全性**：避免在数据文件中存储真实密码等敏感信息

## 价值

通过数据驱动测试，项目获得了：

- **可维护性**：测试数据与测试逻辑分离，便于维护
- **可扩展性**：轻松添加新的测试数据而无需修改代码
- **可重用性**：相同的测试逻辑可用于不同的测试数据
- **覆盖率**：通过多样化的测试数据提高测试覆盖率
- **效率**：减少重复代码，提高开发效率