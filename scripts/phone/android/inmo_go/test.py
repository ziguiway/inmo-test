import time

import allure
from common.type import DriverType
from common.utils import DriverUtils,GlassesUtils
from page.phone.android.inmo_go.connect_glasses import ConnectGlassesPage
from page.phone.android.inmo_go.product import ProductPage
from page.phone.android.inmo_go.tutorial_list import TutorialListPage
from page.phone.android.inmo_go.user_agreement import UserAgreementPage
from page.phone.android.inmo_go.connect_wifi import ConnectWifiPage


class Test:
    @allure.title("设置测试环境")
    def setup_method(self):
        with allure.step("初始化驱动"):
            driver = DriverUtils.get_driver(DriverType.ANDROID)
        with allure.step("初始化页面对象"):
            self.user_agreement_page = UserAgreementPage(driver)
            self.tutorial_list_page = TutorialListPage(driver)
            self.product_page = ProductPage(driver)
            self.connect_glasses = ConnectGlassesPage(driver)
            self.connect_wifi_page = ConnectWifiPage(driver)

    @allure.title("清理测试环境")
    def teardown_method(self):
        with allure.step("关闭ANDROID驱动"):
            DriverUtils.quit_driver(DriverType.ANDROID)
        with allure.step("关闭GLASS驱动"):
            DriverUtils.quit_driver(DriverType.GLASS)

    @allure.title("测试连接眼镜")
    @allure.description("测试手机APP与眼镜的连接功能")
    @allure.tag("连接测试", "功能测试")
    def test_connect_glasses(self):
        with allure.step("允许通知"):
            self.user_agreement_page.allow_info()
        with allure.step("同意用户协议"):
            self.user_agreement_page.agree()
        with allure.step("选择GO2设备"):
            self.tutorial_list_page.go2()
        with allure.step("允许定位权限"):
            self.tutorial_list_page.allow_location()
        with allure.step("允许查找设备权限"):
            self.tutorial_list_page.allow_find_device()
        with allure.step("允许读取应用权限"):
            self.tutorial_list_page.allow_read_app()
        with allure.step("点击蓝牙连接"):
            self.product_page.click_bt()
        with allure.step("启动蓝牙广播"):
            GlassesUtils.start_bluetooth_broadcast()
        with allure.step("执行眼镜连接"):
            self.connect_glasses.connect_glasses()
        with allure.step("验证连接状态"):
            bt_status = self.product_page.bt_status()
            assert bt_status in "眼镜已连接APP", f"期望连接状态包含'眼镜已连接APP'，但实际是'{bt_status}'"

    @allure.title("测试连接WiFi")
    @allure.description("测试连接WiFi功能，前提是眼镜已连接")
    @allure.tag("WiFi测试", "功能测试")
    def test_connect_wifi(self):
        with allure.step("先完成眼镜连接"):
            self.test_connect_glasses()
        with allure.step("点击WiFi连接"):
            self.product_page.click_wifi()
        with allure.step("连接指定WiFi"):
            self.connect_wifi_page.connect_wifi("inmoglass","20210108")

    @allure.title("测试进入翻译功能")
    @allure.description("测试进入翻译功能页面")
    @allure.tag("翻译测试", "功能测试")
    def test_enter_translation(self):
        self.test_connect_glasses()


