import logging

from appium.webdriver.common.appiumby import AppiumBy

from base.base_page import BasePageAndroid
from common.type import DriverType, WifiStatusType
from common.utils import ElementUtils, DriverUtils


class ConnectWifiPage(BasePageAndroid):

    def __init__(self, driver):
        super().__init__(driver)
        self.loc_wifi_list = (AppiumBy.ID, "com.inmo.inmoglasses:id/tv_wifi_name")
        self.loc_password = (AppiumBy.ID, "com.inmo.inmoglasses:id/et_password")
        self.loc_connect_btn = (AppiumBy.ID, "com.inmo.inmoglasses:id/tv_reset_sure")
        self.loc_cancel_btn = (AppiumBy.ID, "com.inmo.inmoglasses:id/tv_cancel")
        self.loc_custom_net_config_btn = (AppiumBy.ID, "com.inmo.inmoglasses:id/tv_custom_network")
        self.loc_custom_wifi_name = (AppiumBy.ID, "com.inmo.inmoglasses:id/et_ssid")
        self.loc_custom_wifi_password = (AppiumBy.ID, "com.inmo.inmoglasses:id/et_password")
        self.loc_refresh_btn = (AppiumBy.ID, "com.inmo.inmoglasses:id/iv_start_discovery")
        self.loc_back_btn = (AppiumBy.ID, "com.inmo.inmoglasses:id/iv_back")
        self.loc_wifi_connect_status = (AppiumBy.ID, "com.inmo.inmoglasses:id/tv_wifi_connect_state")

    def get_wifi_list(self):
        """
        获取WiFi列表
        :return:
        """
        wifi_list = self.base_find_elements(self.loc_wifi_list)
        return wifi_list

    def connect_wifi(self, wifi_name, wifi_password):
        """
        连接wifi
        :param wifi_name:
        :param wifi_password:
        :return:
        """
        wifi_list = self.get_wifi_list()
        status, current_wifi_name = self.get_current_wifi_status()
        if status == WifiStatusType.CONNECTED and current_wifi_name == wifi_name:
            logging.info(f"当前已连接wifi：{wifi_name}")
            return
        if wifi_name not in [element.text for element in wifi_list]:
            logging.info(f"找不到：{wifi_name}")
            return
        for wifi in wifi_list:
            if wifi_name == wifi.text:
                wifi.click()
                break
        self.base_input(self.loc_password, wifi_password)
        self.base_click(self.loc_connect_btn)
        logging.info(f"开始连接wifi:{wifi_name}")
        wifi_status = self.get_current_wifi_status()
        if wifi_status == WifiStatusType.CONNECTED:
            logging.info(f"wifi:{wifi_name}已连接")

    def custom_net_config(self, wifi_name, wifi_password):
        """
        自定义配网
        :param wifi_name:
        :param wifi_password:
        :return:
        """
        self.base_click(self.loc_custom_net_config_btn)
        self.base_input(self.loc_custom_wifi_name, wifi_name)
        self.base_input(self.loc_custom_wifi_password, wifi_password)
        self.base_click(self.loc_connect_btn)

    def is_wifi_connected(self, wifi_name):
        pass

    def refresh_wifi_list(self):
        """
        刷新WiFi列表
        :return:
        """
        self.base_click(self.loc_refresh_btn)

    def get_current_wifi_status(self):
        """
        获取当前wifi状态
        :return:
        """
        is_connected = ElementUtils.is_el_exist_by_text(DriverType.ANDROID, WifiStatusType.CONNECTED.value, timeout=5)
        if is_connected:
            current_wifi = self.get_wifi_list()[0]
            logging.info(f"当前连接的wifi是：{current_wifi.text}")
            return WifiStatusType.CONNECTED, current_wifi.text
        else:
            logging.info("当前未连接wifi")
            return WifiStatusType.UNCONNECTED, None


if __name__ == '__main__':
    driver = DriverUtils.get_driver(DriverType.ANDROID, False)
    connect_wifi_page = ConnectWifiPage(driver)
    connect_wifi_page.connect_wifi("inmoglass-5G", "20210108")
