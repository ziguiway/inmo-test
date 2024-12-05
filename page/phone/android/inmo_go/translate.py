from venv import logger

from appium.webdriver.common.appiumby import AppiumBy

from base.base_page import BasePageAndroid
from common.type import DriverType
from common.utils import DriverUtils


class TranslatePage(BasePageAndroid):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.__loc_translate_btn = (AppiumBy.ID,
                                    "com.inmo.inmoglasses:id/tv_go_to_translation")
        self.__loc_setting = (AppiumBy.ID, "com.inmo.inmoglasses:id/iv_setting")

        self.__loc_custom_translation = (AppiumBy.ID, "com.inmo.inmoglasses:id/cl_custom_translation")


    def click_translate_btn(self):
        self.base_click(self.__loc_translate_btn)
        logger.info("点击了“进入翻译”按钮")

    def click_setting(self):
        self.base_click(self.__loc_setting)

    def to_custom_translation(self):
        self.driver.swipe(2100, 1086, 2100, 250)
        self.base_click(self.__loc_custom_translation)




if __name__ == '__main__':
    driver = DriverUtils.get_driver(DriverType.ANDROID,False)
    translate_page = TranslatePage(driver)
    translate_page.to_custom_translation()
