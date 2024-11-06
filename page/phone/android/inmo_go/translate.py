from appium.webdriver.common.appiumby import AppiumBy

from base.base_page import BasePageAndroid
from common.type import DriverType
from common.utils import DriverUtils


class TranslatePage(BasePageAndroid):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.__loc_translate_btn = (AppiumBy.XPATH,
                                    "//android.widget.TextView[@resource-id='com.inmo.inmoglasses:id/tv_translate' and @text='translate']")
        self.__loc_setting = (AppiumBy.ID, "com.inmo.inmoglasses:id/iv_setting")

    def click_translate_btn(self):
        self.base_click(self.__loc_translate_btn)

    def click_setting(self):
        self.base_click(self.__loc_setting)

    def scroll_to_translate_btn(self):
        self.driver.swipe(2100, 1199, 2100, 70)



if __name__ == '__main__':
    driver = DriverUtils.get_driver(DriverType.ANDROID,False)
    translate_page = TranslatePage(driver)
    translate_page.click_translate_btn()