from common.type import DriverType
from common.utils import DriverUtils
from page.phone.android.inmo_go.custom_translation import CustomTranslationPage
from page.phone.android.inmo_go.translate import TranslatePage


class TestTranslation:

    def setup_method(self):
        self.driver = DriverUtils.get_driver(DriverType.ANDROID, False)
        self.translate_page = TranslatePage(self.driver)
        self.custom_translation_page = CustomTranslationPage(self.driver)

    def teardown_method(self):
        DriverUtils.quit_driver(DriverType.ANDROID)

    def test_add_custom_translation(self):
        self.translate_page.click_translate_btn()
        self.translate_page.click_setting()
        self.translate_page.to_custom_translation()
        self.custom_translation_page.add_word_list("test",
                                                   [("test1", "测试1"), ("test2", "测试2"), ("test3", "测试3"),
                                                    ("test4", "测试4"), ("test5", "测试5")]
                                                   , False)
