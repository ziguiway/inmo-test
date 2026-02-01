import time

from selenium.webdriver.common.by import By

from base.base_page import BasePageAndroid
from common.logger_utils import LoggerSingleton


class ConnectGlassesPage(BasePageAndroid):

    def __init__(self,driver):
        super().__init__(driver)
        self.__loc_glasses_list = (By.ID, "com.inmo.inmoglasses:id/tv_device_add")

    def connect_glasses(self):
        glasses_list = self.base_find_elements(self.__loc_glasses_list)
        glasses_list[0].click()
        self.logger.info("点击了连接按钮")



