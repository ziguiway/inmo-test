from selenium.webdriver.common.by import By

from base.base_page import BasePageAndroid
from common.logger_utils import LoggerSingleton


class UserAgreementPage(BasePageAndroid):
    def __init__(self,driver):
        super().__init__(driver)
        self.__loc_allow = (By.ID, 'com.android.permissioncontroller:id/permission_allow_button')
        self.__loc_deny = (By.ID, 'com.android.permissioncontroller:id/permission_deny_button')
        self.__loc_agree = (By.ID, 'com.inmo.inmoglasses:id/tv_reset_sure')
        self.__loc_disagree = (By.ID, 'com.inmo.inmoglasses:id/tv_cancel')

    def allow_info(self):
        self.base_click(self.__loc_allow)
        self.logger.info("点击允许通知")

    def deny_info(self):
        self.base_click(self.__loc_deny)
        self.logger.info('点击拒绝通知')

    def agree(self):
        self.base_click(self.__loc_agree)
        self.logger.info('点击同意并继续')

    def disagree(self):
        self.base_click(self.__loc_disagree)
        self.logger.info('点击不同意')
