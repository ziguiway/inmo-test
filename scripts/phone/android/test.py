from common.type import DriverType
from common.utils import DriverUtils
from page.phone.android.inmo_go.product import ProductPage
from page.phone.android.inmo_go.tutorial_list import TutorialListPage
from page.phone.android.inmo_go.user_agreement import UserAgreementPage


class Test:
    def setup_method(self):
        self.user_agreement_page = UserAgreementPage()
        self.tutorial_list_page = TutorialListPage()
        self.product_page = ProductPage()

    def teardown_method(self):
        DriverUtils.quit_driver(DriverType.ANDROID)

    def test_agree(self):
        self.user_agreement_page.allow_info()
        self.user_agreement_page.agree()
        self.tutorial_list_page.go2()
        self.tutorial_list_page.allow_location()
        self.tutorial_list_page.allow_find_device()
        self.tutorial_list_page.allow_read_app()
        self.product_page.bt()

    # def test_disagree(self):
    #     self.user_agreement_page.disagree()
    #     sleep(2)
