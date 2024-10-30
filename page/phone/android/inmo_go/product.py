import logging

from selenium.webdriver.common.by import By

from base.base_page import BasePageAndroid


class ProductPage(BasePageAndroid):
    def __init__(self):
        super().__init__()
        logging.info("进入产品页")
        self.__loc_logo = (By.ID, "com.inmo.inmoglasses:id/iv_logo")
        self.__loc_sidebar = (By.ID, "com.inmo.inmoglasses:id/iv_drawer_open")
        self.__loc_bt = (By.ID, "com.inmo.inmoglasses:id/ll_bt_connect")
        self.__loc_wifi = (By.ID, "com.inmo.inmoglasses:id/ll_wifi_status")
        self.__loc_brightness = (By.ID, "com.inmo.inmoglasses:id/seekbar_brightness")
        self.__loc_voice = (By.ID, "com.inmo.inmoglasses:id/seekbar_volume")
        self.__loc_ring = (By.ID, "com.inmo.inmoglasses:id/ll_ring_info")
        self.__loc_speaker_box = (By.ID, "com.inmo.inmoglasses:id/ll_speaker_info")

    def bt(self):
        self.base_click(self.__loc_bt)
        logging.info("点击了蓝牙")

    def wifi(self):
        self.base_click(self.__loc_wifi)
        logging.info("点击了wifi")
