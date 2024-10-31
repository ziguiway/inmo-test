import logging

from selenium.webdriver.common.by import By

from base.base_page import BasePageAndroid


class ProductPage(BasePageAndroid):
    def __init__(self):
        super().__init__()
        logging.info("进入产品页")
        self.__loc_logo = (By.ID, "com.inmo.inmoglasses:id/iv_logo")
        self.__loc_sidebar = (By.ID, "com.inmo.inmoglasses:id/iv_drawer_open")
        self.__loc_bt = (By.ID, "com.inmo.inmoglasses:id/tv_bt_connect_status")
        self.__loc_wifi = (By.ID, "com.inmo.inmoglasses:id/tv_wifi_status")
        self.__loc_brightness = (By.ID, "com.inmo.inmoglasses:id/seekbar_brightness")
        self.__loc_voice = (By.ID, "com.inmo.inmoglasses:id/seekbar_volume")
        self.__loc_ring = (By.ID, "com.inmo.inmoglasses:id/ll_ring_info")
        self.__loc_speaker_box = (By.ID, "com.inmo.inmoglasses:id/ll_speaker_info")

    def click_bt(self):
        self.base_click(self.__loc_bt)
        logging.info("点击了蓝牙")

    def click_wifi(self):
        self.base_click(self.__loc_wifi)
        logging.info("点击了wifi")

    def adjust_brightness(self):
        self.base_move_seekbar(self.__loc_brightness,99)


    def bt_status(self):
        text = self.base_get_text(self.__loc_bt)
        logging.info(f"获取了蓝牙连接状态:{text}")
        return text

    def wifi_status(self):
        text = self.base_get_text(self.__loc_wifi)
        logging.info(f"获取了wifi连接状态:{text}")
        return text


