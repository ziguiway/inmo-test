from appium.webdriver.common.appiumby import AppiumBy

from base.base_page import BasePageAndroid


class FindRingPage(BasePageAndroid):

    def __init__(self, driver):
        super().__init__(driver)
        self.loc_find_ring = (
        AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().className('android.view.ViewGroup').instance(3)")

    def find_ring(self):
        self.base_click(self.loc_find_ring)
