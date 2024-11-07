from common.type import DriverType
from common.utils import DriverUtils,GlassesUtils
from page.phone.android.inmo_go.connect_glasses import ConnectGlassesPage
from page.phone.android.inmo_go.product import ProductPage
from page.phone.android.inmo_go.tutorial_list import TutorialListPage
from page.phone.android.inmo_go.user_agreement import UserAgreementPage
from page.phone.android.inmo_go.connect_wifi import ConnectWifiPage


class Test:
    def setup_method(self):
        driver = DriverUtils.get_driver(DriverType.ANDROID)
        self.user_agreement_page = UserAgreementPage(driver)
        self.tutorial_list_page = TutorialListPage(driver)
        self.product_page = ProductPage(driver)
        self.connect_glasses = ConnectGlassesPage(driver)
        self.connect_wifi_page = ConnectWifiPage(driver)

    def teardown_method(self):
        DriverUtils.quit_driver(DriverType.ANDROID)
        DriverUtils.quit_driver(DriverType.GLASS)

    def test_connect_glasses(self):
        self.user_agreement_page.allow_info()
        self.user_agreement_page.agree()
        self.tutorial_list_page.go2()
        self.tutorial_list_page.allow_location()
        self.tutorial_list_page.allow_find_device()
        self.tutorial_list_page.allow_read_app()
        self.product_page.click_bt()
        GlassesUtils.start_bluetooth_broadcast()
        self.connect_glasses.connect_glasses()
        bt_status = self.product_page.bt_status()
        assert bt_status in "眼镜已连接APP"

    def test_connect_wifi(self):
        self.test_connect_glasses()
        self.product_page.click_wifi()
        self.connect_wifi_page.connect_wifi("inmoglass-5G","20210108")

    def test_enter_translation(self):
        self.test_connect_glasses()


