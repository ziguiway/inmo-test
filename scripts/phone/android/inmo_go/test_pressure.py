from common.type import DriverType
from common.utils import DriverUtils, GlassesUtils
from page.phone.android.inmo_go.connect_glasses import ConnectGlassesPage
from page.phone.android.inmo_go.connect_wifi import ConnectWifiPage
from page.phone.android.inmo_go.custom_vocabulary import CustomVocabularyPage
from page.phone.android.inmo_go.product import ProductPage
from page.phone.android.inmo_go.tutorial_list import TutorialListPage
from page.phone.android.inmo_go.user_agreement import UserAgreementPage


class TestPressure:
    def setup_class(self):
        driver = DriverUtils.get_driver(DriverType.ANDROID)
        self.custom_vocabulary_page = CustomVocabularyPage(driver)
        self.user_agreement_page = UserAgreementPage(driver)
        self.tutorial_list_page = TutorialListPage(driver)
        self.product_page = ProductPage(driver)
        self.connect_glasses = ConnectGlassesPage(driver)
        self.connect_wifi_page = ConnectWifiPage(driver)

    def test_custom_vocabulary_add(self):
        self.user_agreement_page.allow_info()
        self.user_agreement_page.agree()
        self.tutorial_list_page.go2()
        self.tutorial_list_page.allow_location()
        self.tutorial_list_page.allow_find_device()
        self.tutorial_list_page.allow_read_app()
        self.product_page.click_bt()
        GlassesUtils.start_bluetooth_broadcast()
        self.connect_glasses.connect_glasses()

