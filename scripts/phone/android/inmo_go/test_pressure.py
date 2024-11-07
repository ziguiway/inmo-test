import logging

from common.type import DriverType
from common.utils import DriverUtils
from page.phone.android.inmo_go.custom_vocabulary import CustomVocabularyPage
from page.phone.android.inmo_go.edit_inscription import EditInscriptionPage


class TestPressure:
    def setup_method(self):
        self.driver = DriverUtils.get_driver(DriverType.ANDROID, False)
        self.custom_vocabulary_page = CustomVocabularyPage(driver=self.driver)
        self.edit_inscription_page = EditInscriptionPage(driver=self.driver)

    def teardown_method(self):
        DriverUtils.quit_driver(DriverType.ANDROID)

    def test_custom_vocabulary_add(self):
        for i in range(100000):
            self.custom_vocabulary_page.click_add_button()
            logging.info(f"这是第{i}次点击")

    def test_edit_inscription(self):
        ones = '1' * 10001
        logging.info(len(ones))
        # 输出结果
        self.edit_inscription_page.input_text_box(ones)
        # self.edit_inscription_page.input_text_box("好好好")
