# INMO-TEST自动化平台

## 一、项目的介绍 

### 1.PO模式

本项目采用POM的设计思想进行设计。PO模式是一种自动化测试设计模式，将页面定位和业务操作分开，也就是把对象定位和测试脚本分开，从而提供可维护性。PO模式可以把一个页面分为三层，对象库层、操作层、业务层。

### 2.数据驱动

数据驱动（Data-Driven Testing, DDT） 是一种自动化测试方法，通过将测试数据与测试逻辑分开，使得相同的测试用例可以使用不同的数据进行多次执行。其核心思想是将测试数据从测试脚本中提取出来，并将数据存储在外部（如 CSV、Excel、数据库等），通过读取这些数据来执行相同的测试场景，以验证不同数据输入下系统的表现和稳定性。

### 3.目录结构 

```
|-- inmo-test
    |-- base
    |-- common
    |-- log
    |-- page
    |-- report
    |-- scripts
    |-- .gitignore
    |-- config.py
    |-- config.yaml
    |-- main.py
    |-- pytest.ini
    |-- requirements.txt
    |-- server.py
```

- base：基类，封装page 页面一些公共的方法
- common：存放工具类，枚举类
- log：存放日志信息
- page：操作层，封装对元素的操作，一个页面封装成一个对象
- report：存放测试报告
- scripts：业务层，将一个或多个操作组合起来完成一个业务功能
- .gitignore：告诉 Git 哪些文件或目录应该被忽略，不纳入版本控制
- config.py：存放项目的配置
- config.yaml：存放appium服务的配置
- main.py：项目的主入口
- pytest.ini：pytest 的配置文件
- requirements.txt：项目运行所需的库
- server.py：提供项目所需的服务

### 3.在哪里写测试用例？ 

在scripts包下找到对应的项目，编写测试用例即可

例如：使用inmo-go连接Go2

首先，在page包中封装所需的页面元素和方法

```python
import logging
import time

from selenium.webdriver.common.by import By

from base.base_page import BasePageAndroid


class ConnectGlassesPage(BasePageAndroid):

    def __init__(self, driver):
        super().__init__(driver)
        self.__loc_glasses_list = (By.ID, "com.inmo.inmoglasses:id/tv_device_add")

    def connect_glasses(self):
        glasses_list = self.base_find_elements(self.__loc_glasses_list)
        glasses_list[0].click()
        logging.info("点击了连接按钮")
```

然后，在scripts包中编写具体的测试用例

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

### 4.怎么执行测试用例？ 

#### 方式一（推荐）：运行main.py

打开powershell,进入项目的根路径,输入`python main.py`，回车

``` python
python main.py
```

这种方式会自动的启动appium服务，无需手动启动

#### 方式二：手动

1.打开powershell

``` shell
appium --allow-insecure=adb_shell -p {port}
```

> [!tip]
>
> 把 {port} 改成你要启动的端口，要与config.yaml文件一致

2.在项目的根路径下,输入`pytest`，回车

``` shell
pytest
```

## 

## 二、环境的安装

> [!NOTE]
>
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

### 1.将代码clone到本地并安装行所需的库

```shell
git clone https://github.com/ziguiway/inmo-test.git
cd inmo-test
pip install -r requirements.txt
```

### 2.修改udid 

> [!TIP]
>
> 使用`adb devices`查看udid

- 把config.yaml文件中为udid改成你设备对应的udid
- 把common/type.py文件中为DriverType改成你设备对应的udid

### 3.执行测试用例

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
