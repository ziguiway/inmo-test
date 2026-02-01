# 测试数据目录

## 概述

此目录包含所有用于数据驱动测试的外部数据文件。通过将测试数据与测试代码分离，我们实现了更好的可维护性和灵活性。

## 数据文件说明

### 1. WiFi测试数据
- **文件**: `wifi_test_data.csv`
- **用途**: 存储WiFi连接测试的各种网络配置
- **字段**:
  - `wifi_name`: WiFi网络名称
  - `password`: WiFi密码
  - `description`: 测试场景描述
  - `expected_result`: 预期连接结果

### 2. 眼镜连接测试数据
- **文件**: `glasses_connection_test_data.json`
- **用途**: 存储眼镜连接测试的场景和步骤
- **字段**:
  - `test_case_id`: 测试用例ID
  - `test_case`: 测试用例名称
  - `steps`: 执行步骤列表
  - `expected_result`: 预期结果
  - `priority`: 优先级（high/medium/low）
  - `description`: 测试描述

### 3. 翻译功能测试数据
- **文件**: `translation_test_data.yaml`
- **用途**: 存储翻译功能测试的输入输出对
- **字段**:
  - `test_case_id`: 测试用例ID
  - `test_case`: 测试用例名称
  - `source_language`: 源语言
  - `target_language`: 目标语言
  - `input_text`: 输入文本
  - `expected_output`: 预期输出
  - `priority`: 优先级
  - `description`: 测试描述

## 最佳实践

### 1. 数据文件命名
- 使用有意义的文件名
- 使用统一的命名约定
- 包含功能模块名称

### 2. 数据格式选择
- **CSV**: 适用于表格型数据，易于编辑和维护
- **JSON**: 适用于结构化数据，支持复杂嵌套结构
- **YAML**: 适用于配置型数据，具有良好的可读性

### 3. 数据验证
- 确保数据格式正确
- 验证必要字段的存在
- 使用合理的数据类型

### 4. 数据安全
- 不要在数据文件中存储真实的敏感信息
- 使用占位符或环境变量替代敏感数据
- 定期审查数据内容

## 维护指南

### 添加新测试数据
1. 确定合适的数据格式（CSV/JSON/YAML）
2. 按照现有格式创建新数据条目
3. 确保所有必要字段都已填写
4. 验证数据的有效性

### 更新现有数据
1. 备份原有数据文件
2. 修改数据内容
3. 测试数据驱动的测试用例以确保兼容性
4. 记录变更原因和影响

## 与测试代码集成

测试代码通过 `DataProvider` 类从这些文件中读取数据：

```python
from common.data_provider import DataProvider

# 从CSV读取
csv_data = DataProvider.load_from_csv("data/wifi_test_data.csv")

# 从JSON读取
json_data = DataProvider.load_from_json("data/glasses_connection_test_data.json")

# 从YAML读取
yaml_data = DataProvider.load_from_yaml("data/translation_test_data.yaml")
```

这种分离使得非开发人员也能参与测试数据的维护，提高了团队协作效率。