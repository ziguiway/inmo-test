from appium.webdriver.common.appiumby import AppiumBy

from base.base_page import BasePageAndroid
from common.type import DriverType
from common.utils import DriverUtils


class CustomTranslationPage(BasePageAndroid):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

        self.__loc_iv_add = (AppiumBy.ID, "com.inmo.inmoglasses:id/iv_add")
        self.__loc_table_name = (AppiumBy.ID, "com.inmo.inmoglasses:id/et_vocabulary")
        self.__loc_change_model = (AppiumBy.ID, "com.inmo.inmoglasses:id/iv_language_changed")
        self.__loc_create_btn = (AppiumBy.ID, "com.inmo.inmoglasses:id/tv_create")
        self.__loc_identify_language = (AppiumBy.ID, "com.inmo.inmoglasses:id/et_identify_language")
        self.__loc_translate_to = (AppiumBy.ID, "com.inmo.inmoglasses:id/et_translate_to")
        self.__loc_back_btn = (AppiumBy.ID, "com.inmo.inmoglasses:id/iv_back")
        self.__loc_upload_btn = (AppiumBy.ID, "com.inmo.inmoglasses:id/tv_upload_all")




    def add_word_list(self, table_name, word_list, model):
        self.base_click(self.__loc_iv_add)
        self.base_input(self.__loc_table_name, table_name)
        if model:
            self.base_click(self.__loc_change_model)
        self.base_click(self.__loc_create_btn)
        for i, word in enumerate(word_list):
            self.base_input(self.__loc_identify_language, word[0])
            self.base_input(self.__loc_translate_to, word[1])
            if i == len(word_list) - 1:
                break
            self.base_click(self.__loc_iv_add)
        self.base_click(self.__loc_back_btn)
        self.base_click(self.__loc_upload_btn)

if __name__ == '__main__':
    driver = DriverUtils.get_driver(DriverType.ANDROID, False)
    custom_translation_page = CustomTranslationPage(driver)
    custom_translation_page.add_word_list("测试1", [("test1", "测试1"), ("test2", "测试2"), ("test3", "测试3")], True)
