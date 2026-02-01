# 测试报告使用指南

## 概述

本项目已集成Allure测试报告功能，提供更丰富的测试结果展示和分析能力。

## 安装依赖

要使用Allure报告功能，您需要安装以下依赖：

```bash
pip install -r requirements.txt
```

此外，还需要安装Allure命令行工具：

### Windows
```bash
# 下载Allure命令行工具
# 从 https://github.com/allure-framework/allure2/releases 下载最新版本
# 解压并将bin目录添加到PATH环境变量中
```

或者使用Chocolatey安装：
```bash
choco install allure
```

## 运行测试

运行测试以生成Allure结果：

```bash
# 运行所有测试
pytest

# 或运行特定测试
pytest scripts/phone/android/inmo_go/test.py
```

测试结果将保存在 `./allure-results` 目录中。

## 生成和查看报告

### 实时查看报告
```bash
# 启动本地服务器并打开浏览器查看报告
allure serve allure-results
```

### 生成静态报告
```bash
# 生成静态HTML报告到指定目录
allure generate allure-results -o allure-report --clean
```

然后在浏览器中打开 `allure-report/index.html` 文件。

## Allure报告特性

### 1. 丰富的测试信息
- 测试标题和描述
- 测试标签（tag）
- 测试步骤详情
- 断言失败信息

### 2. 报告可视化
- 测试执行时间统计
- 测试结果分布
- 失败测试详细信息
- 测试执行趋势

### 3. 测试分类
- 按标签分类测试
- 按测试结果分类
- 按时间排序

## 在测试中使用Allure

### 添加装饰器
```python
import allure

@allure.title("测试标题")
@allure.description("测试描述")
@allure.tag("标签1", "标签2")
def test_example():
    with allure.step("执行步骤"):
        # 测试代码
        pass
```

### 添加测试步骤
```python
with allure.step("步骤描述"):
    # 步骤执行代码
    pass
```

## 报告分析

### 摘要页
- 显示总体测试结果
- 测试执行时间和统计信息
- 通过率和失败率

### 图表页
- 测试结果分布图表
- 测试执行时间趋势
- 缺陷分析

### 测试列表
- 按状态过滤测试（通过/失败/跳过）
- 按标签过滤测试
- 按时间排序测试

## 注意事项

1. 确保allure-results目录存在且可写入
2. 运行测试前确保所有依赖已安装
3. 如果遇到权限问题，请检查allure-results目录的访问权限
4. 生成报告时使用`--clean`参数可以清除之前的报告数据