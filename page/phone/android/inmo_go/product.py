from selenium.webdriver.common.by import By

from base.base_page import BasePageAndroid
from common.logger_utils import LoggerSingleton


class ProductPage(BasePageAndroid):
    def __init__(self,driver):
        super().__init__(driver)

        self.__loc_logo = (By.ID, "com.inmo.inmoglasses:id/iv_logo")
        self.__loc_sidebar = (By.ID, "com.inmo.inmoglasses:id/iv_drawer_open")
        self.__loc_bt = (By.ID, "com.inmo.inmoglasses:id/tv_bt_connect_status")
        self.__loc_wifi = (By.ID, "com.inmo.inmoglasses:id/tv_wifi_status")
        self.__loc_brightness = (By.ID, "com.inmo.inmoglasses:id/seekbar_brightness")
        self.__loc_voice = (By.ID, "com.inmo.inmoglasses:id/seekbar_volume")
        self.__loc_ring = (By.ID, "com.inmo.inmoglasses:id/ll_ring_info")
        self.__loc_speaker_box = (By.ID, "com.inmo.inmoglasses:id/ll_speaker_info")
        self.__loc_bottom_product_btn = (By.ID, "com.inmo.inmoglasses:id/iv_product")
        self.__loc_bottom_translate_btn = (By.ID, "com.inmo.inmoglasses:id/iv_translate")

    def click_bt(self):
        self.base_click(self.__loc_bt)
        self.logger.info("点击了蓝牙")

    def click_wifi(self):
        self.base_click(self.__loc_wifi)
        self.logger.info("点击了wifi")

    def adjust_brightness(self,percent):
        self.base_move_seekbar(self.__loc_brightness,percent)
        self.logger.info(f"调节亮度到:{percent}%")

    def bt_status(self):
        text = self.base_get_text(self.__loc_bt)
        self.logger.info(f"获取了蓝牙连接状态:{text}")
        return text

    def wifi_status(self):
        text = self.base_get_text(self.__loc_wifi)
        self.logger.info(f"获取了wifi连接状态:{text}")
        return text

    def to_translate_page(self):
        self.base_click(self.__loc_bottom_translate_btn)
