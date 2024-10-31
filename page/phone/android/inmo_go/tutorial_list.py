import logging

from selenium.webdriver.common.by import By

from base.base_page import BasePageAndroid


class TutorialListPage(BasePageAndroid):
    def __init__(self):
        super().__init__()
        self.__loc_go2 = (By.ID, 'com.inmo.inmoglasses:id/iv_device_bg')

        self.__loc_allow_location = (
        By.ID, 'com.android.permissioncontroller:id/permission_allow_foreground_only_button')
        self.__loc_deny_location = (By.ID, 'com.android.permissioncontroller:id/permission_deny_button')

        self.__loc_allow_find_device = (By.ID, 'com.android.permissioncontroller:id/permission_allow_button')
        self.__loc_deny_find_device = (By.ID, 'com.android.permissioncontroller:id/permission_deny_button')

        self.__loc_allow_read_app = (By.ID, "com.android.permissioncontroller:id/permission_allow_button")
        self.__loc_deny_read_app = (By.ID, "com.android.permissioncontroller:id/permission_deny_button")

    def go2(self):
        self.base_click(self.__loc_go2)
        logging.info("点击go2")

    def allow_location(self):
        self.base_click(self.__loc_allow_location)
        logging.info("点击允许定位")

    def deny_location(self):
        self.base_click(self.__loc_deny_location)
        logging.info("点击拒绝定位")

    def allow_find_device(self):
        self.base_click(self.__loc_allow_find_device)
        logging.info("点击允许查找设备")

    def deny_find_device(self):
        self.base_click(self.__loc_deny_find_device)
        logging.info("点击拒绝查找设备")

    def allow_read_app(self):
        self.base_click(self.__loc_allow_read_app)
        logging.info("点击允许读取应用")

    def deny_read_app(self):
        self.base_click(self.__loc_deny_read_app)
        logging.info("点击拒绝读取应用")
