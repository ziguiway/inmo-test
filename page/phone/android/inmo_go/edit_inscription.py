from appium.webdriver.common.appiumby import AppiumBy

from base.base_page import BasePageAndroid


class EditInscriptionPage(BasePageAndroid):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.__loc_title = (AppiumBy.ID, 'com.inmo.inmoglasses:id/et_teleprompter_title')
        self.__loc_text_box = (AppiumBy.ID, 'com.inmo.inmoglasses:id/visible_area_edit')

    def input_title(self, title):
        self.base_input(self.__loc_title, title)

    def input_text_box(self, text):
        self.base_input(self.__loc_text_box, text)
