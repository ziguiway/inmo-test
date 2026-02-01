# INMO-TEST自动化平台

## 项目简介

INMO-TEST是一个基于Appium和Selenium的移动端自动化测试框架，专门用于智能眼镜产品的端到端测试。该框架采用Page Object模式设计，具有良好的可维护性和扩展性。

### 设计模式

#### PO模式 (Page Object)

本项目采用POM（Page Object Model）的设计思想进行设计。PO模式是一种自动化测试设计模式，将页面定位和业务操作分开，把对象定位和测试脚本分离，从而提高代码的可维护性。PO模式将一个页面分为三层：对象库层、操作层、业务层。

#### 数据驱动

数据驱动（Data-Driven Testing, DDT）是一种自动化测试方法，通过将测试数据与测试逻辑分离，使相同的测试用例可以使用不同的数据进行多次执行。其核心思想是将测试数据从测试脚本中提取出来，并将数据存储在外部（如 CSV、Excel、数据库等），通过读取这些数据来执行相同的测试场景，以验证不同数据输入下系统的表现和稳定性。

### 架构流程

<img src=".\img\20260131-174202.jpg" alt="核心流程" style="zoom:67%;" />

### 目录结构

```
|-- inmo-test
    |-- base/           # 基类，封装页面公共方法
    |-- common/         # 存放工具类、枚举类
    |-- data/           # 存放测试数据文件
    |-- log/            # 存放日志信息
    |-- page/           # 操作层，封装页面元素操作
    |-- report/         # 存放测试报告
    |-- scripts/        # 业务层，组合操作完成业务功能
    |-- .gitignore      # Git忽略配置
    |-- config.py       # 项目配置
    |-- config.yaml     # Appium服务配置
    |-- main.py         # 项目主入口
    |-- pytest.ini      # Pytest配置文件
    |-- requirements.txt # 项目依赖库
    |-- server.py       # 项目服务
```

### 测试用例开发

在scripts包下找到对应的项目，编写测试用例即可。

**示例：使用inmo-go连接Go2**

首先，在page包中封装所需的页面元素和方法：

```python
import time

from selenium.webdriver.common.by import By

from base.base_page import BasePageAndroid
from common.logger_utils import LoggerSingleton

class ConnectGlassesPage(BasePageAndroid):

    def __init__(self, driver):
        super().__init__(driver)
        self.__loc_glasses_list = (By.ID, "com.inmo.inmoglasses:id/tv_device_add")

    def connect_glasses(self):
        glasses_list = self.base_find_elements(self.__loc_glasses_list)
        glasses_list[0].click()
        self.logger.info("点击了连接按钮")
```

然后，在scripts包中编写具体的测试用例。

## 测试报告

本项目集成了Allure测试报告功能，提供更丰富的测试结果展示和分析能力。

### 功能特性

- 丰富的测试信息（标题、描述、标签、步骤详情）
- 测试执行时间统计和结果分布
- 按状态、标签分类的测试过滤
- 失败测试的详细信息和堆栈跟踪
- 自动化截图展示

### 使用方法

1. 运行测试
   ```bash
   pytest
   ```

2. 生成Allure报告
   ```bash
   allure generate allure-results -o allure-report --clean
   ```

3. 查看报告
   ```bash
   allure serve allure-results
   ```

有关详细信息，请参见 TEST_REPORT_GUIDE.md 文件。

## 数据驱动测试

本项目支持数据驱动测试，允许从外部数据源（CSV、JSON、YAML等）读取测试数据，实现测试逻辑与测试数据的分离。

### 特性

- 支持多种数据格式（JSON、CSV、YAML、Excel）
- 数据与代码完全分离，便于维护
- 统一的数据加载接口
- 易于扩展新的数据源类型

### 使用方法

1. 创建测试数据文件（CSV、JSON或YAML格式）
2. 使用 DataProvider 类加载数据
3. 在测试中使用 @pytest.mark.parametrize 装饰器

示例：
```python
from common.data_provider import DataProvider

@pytest.mark.parametrize("test_data", 
    DataProvider.load_from_json("test_data.json"))
def test_example(self, test_data):
    # 测试逻辑
    pass
```

### 数据源支持

- CSV文件：表格形式的测试数据
- JSON文件：结构化测试数据
- YAML文件：配置式测试数据
- Excel文件：复杂测试数据（需要安装pandas）

测试数据存储在 `data/` 目录中，与测试代码完全分离，便于维护和管理。

有关详细信息，请参见 DATA_DRIVEN_TEST_GUIDE.md 文件。

## 基础页面类优化

基础页面类 (`base/base_page.py`) 已经进行了全面优化，提供了更多实用功能和更好的稳定性：

### 主要优化内容

- **增强的元素查找机制**：使用Expected Conditions提高元素定位可靠性
- **改进的错误处理**：完善的异常捕获和日志记录机制
- **自动截图功能**：测试失败时自动保存截图，便于调试分析
- **可配置参数**：支持自定义超时时间和轮询频率
- **平台特定方法**：针对Android和iOS平台的专属功能
- **等待策略优化**：智能等待机制，提升测试稳定性
- **滚动与交互**：增强的页面滚动和元素交互功能

### 核心特性

- **统一的日志记录**：集成LoggerSingleton，提供一致的日志输出
- **智能元素等待**：支持显式等待和隐式等待的灵活配置
- **批量操作支持**：提供单个和多个元素查找的统一接口
- **异常处理机制**：完善的异常捕获和错误报告
- **跨平台兼容**：支持Android和iOS双平台测试

### 使用示例

```python
from common.type import DriverType
from common.utils import DriverUtils, GlassesUtils
from page.phone.android.inmo_go.connect_glasses import ConnectGlassesPage
from page.phone.android.inmo_go.product import ProductPage
from page.phone.android.inmo_go.tutorial_list import TutorialListPage
from page.phone.android.inmo_go.user_agreement import UserAgreementPage
from page.phone.android.inmo_go.connect_wifi import ConnectWifiPage


class Test:
    def setup_method(self):
        driver = DriverUtils.get_driver(DriverType.ANDROID)
        self.user_agreement_page = UserAgreementPage(driver)
        self.tutorial_list_page = TutorialListPage(driver)
        self.product_page = ProductPage(driver)
        self.connect_glasses = ConnectGlassesPage(driver)
        self.connect_wifi_page = ConnectWifiPage(driver)

    def teardown_method(self):
        DriverUtils.quit_driver(DriverType.ANDROID)
        DriverUtils.quit_driver(DriverType.GLASS)

    def test_connect_glasses(self):
        self.user_agreement_page.allow_info()
        self.user_agreement_page.agree()
        self.tutorial_list_page.go2()
        self.tutorial_list_page.allow_location()
        self.tutorial_list_page.allow_find_device()
        self.tutorial_list_page.allow_read_app()
        self.product_page.click_bt()
        GlassesUtils.start_bluetooth_broadcast()
        self.connect_glasses.connect_glasses()
        bt_status = self.product_page.bt_status()
        assert bt_status in "眼镜已连接APP"
```

有关详细信息，请参见 BASE_PAGE_OPTIMIZATION.md 文件。

### 4.怎么执行测试用例？ 

#### 方式一（推荐）：运行main.py

打开PowerShell，进入项目的根路径，输入`python main.py`，回车

```python
python main.py
```

这种方式会自动启动appium服务，无需手动启动。

#### 方式二：手动执行

1. 手动启动appium服务

```shell
appium --allow-insecure=adb_shell -p {port}
```

> [!tip]
> 将 {port} 改成你要启动的端口，要与config.yaml文件一致

2. 在项目根路径下运行pytest

```shell
pytest
```

## 环境安装

> [!NOTE]
> 以下环境，如果已经安装过，可以自行跳过
> 
> ✅ nvm : 1.1.12
> 
> ✅ nodejs : 20.18.0
> 
> ✅ appium : 2.12.1
> 
> ✅ Android SDK : 24.4.1
> 
> ✅ uiautomator2 : 2.45.1
> 
> ✅ Java JDK : 17
> 
> ✅ Python：3.12
> 
> ✅ git

### 1.安装[nvm](https://github.com/coreybutler/nvm-windows/releases)和nodejs

请参考[nvm安装和使用保姆级教程（详细）-CSDN博客](https://blog.csdn.net/weixin_38383877/article/details/143077797) 

### 2.安装appium

使用 `npm` 在全局范围内安装 Appium,在命令行输入`npm i -g appium@2.6.0`，耗时可能比较久，请耐心等待安装完成 ⏳

```shell
npm i -g appium@2.6.0
```

### 4.安装Android SDK

请参考[Android SDK安装教程（超详细），从零基础入门到实战，从看这篇开始-CSDN博客](https://blog.csdn.net/Z987421/article/details/131423050) 

### 5.安装Java JDK

请参考[超详细JDK下载与安装步骤（保姆级，含安装包）_jdk下载与安装教程-CSDN博客](https://blog.csdn.net/VA_AV/article/details/138508891) 

### 6.安装UiAutomator2 驱动

> [!IMPORTANT]
>
> 这一步十分重要，我在搭建时候，被折磨了很久 :sob: ，要是不指定版本，会有很多的兼容问题

命令行输入`appium driver install uiautomator2@3.9.0`，回车，等待安装完成。

```shell
appium driver install uiautomator2@3.9.0
```

### 7.安装python

请参考[Python安装教程，超详细！！！-CSDN博客](https://blog.csdn.net/maiya_yayaya/article/details/131450517) 

### 8.安装git

请参考[windows安装git（全网最详细，保姆教程）-CSDN博客](https://blog.csdn.net/weixin_42242910/article/details/136297201) 

## 三、快速开始 

### 1. 代码克隆与依赖安装

```shell
git clone https://github.com/ziguiway/inmo-test.git
cd inmo-test
pip install -r requirements.txt
```

### 2. 设备配置

> [!TIP]
> 使用`adb devices`查看udid

- 修改config.yaml文件中的udid为你设备对应的udid
- 修改common/type.py文件中DriverType为你的设备对应的udid

### 3. 执行测试用例

```shell
python main.py
```

## 四、可能遇到的问题 

### 报错一

> Original error: Appium Settings app is not running after 5000ms

#### 问题分析

眼镜的driver获取有概率会超时，就会报这个错误。起初我以为是SDK的版本不对应，才导致的启动慢导致获取超时，但是我试了很多的SDK版本都不行，还是会有这个问题。后面又怀疑是appium版本的问题，经过一番折腾，然并卵。经过不断地排查，最终我发现，关闭`anlink`投屏软件后，这个报错惊人的消失了！！！原来找了这么久的问题出在投屏身上😑

#### 解决办法

换一个投屏软件。目前推荐使用`Vysor`,在使用过程中比较稳定，没有出现报错。

### 报错二

> java.lang.SecurityException:Permissiondenial:writingtosettingsrequires:android.permission.WRITE_SECURE_SETTINGS

#### 解决办法

- 小米：在开发者选项里，把“USB调试（安全设置）"打开即可。 允许USB调试修改权限或模拟点击
- oppo：在开发者选项里，把"禁止权限监控"打开即可。

### 脚本点击速度很慢

> 脚本获取元素的速度慢，好几秒才点一次

#### 问题分析

电脑环境安装的SDK与手机系统版本不兼容，需要换SDK版本，推荐使用更高版本的SDK

#### 解决办法

参考[Android SDK安装教程（超详细），从零基础入门到实战，从看这篇开始-CSDN博客](https://blog.csdn.net/Z987421/article/details/131423050)，安装最新的SDK

## 五、问题反馈 

在使用`INMO-TEST`自动化测试框架的过程中，如果遇到任何问题，请随时向我反馈。反馈内容包括但不限于：

- **脚本报错** ：任何在运行测试脚本时遇到的错误或异常。
- **使用不便** ：如果框架的某些功能使用起来不直观或有困难。
- **性能问题** ：测试执行速度慢、资源消耗过高等性能相关问题。
- **功能需求** ：你希望框架添加或改进的功能。
- **用例覆盖** ：自动化的用例覆盖不全面。

此外，如果你有任何更好的技术实现方式或创新的思路，也欢迎与我讨论。我们的共同目标是让`INMO-TEST`自动化框架不断优化和提升，使其成为我们测试工作中的得力助手和利器 。

请提供详细的反馈，包括问题的描述、重现步骤、预期结果与实际结果、以及任何相关的环境信息。你的反馈是我们改进和完善`INMO-TEST`的关键力量 。
