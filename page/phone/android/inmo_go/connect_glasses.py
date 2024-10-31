import logging
import time

from selenium.webdriver.common.by import By

from base.base_page import BasePageAndroid


class ConnectGlassesPage(BasePageAndroid):

    def __init__(self):
        super().__init__()
        self.__loc_glasses_list = (By.ID, "com.inmo.inmoglasses:id/tv_device_add")

    def connect_glasses(self):
        glasses_list = self.base_find_elements(self.__loc_glasses_list)
        glasses_list[0].click()
        logging.info("点击了连接按钮")



