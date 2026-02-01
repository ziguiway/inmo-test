from appium.webdriver.common.appiumby import AppiumBy

from base.base_page import BasePageAndroid
from common.type import DriverType, WifiStatusType
from common.utils import DriverUtils, ElementUtils


class CustomVocabularyPage(BasePageAndroid):

    def __init__(self, driver):
        super().__init__(driver)
        self.__loc_add_button = (AppiumBy.ID,"com.inmo.inmoglasses:id/iv_add")

    def click_add_button(self):
        self.base_click(self.__loc_add_button)