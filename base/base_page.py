import logging

from selenium.webdriver.support.ui import WebDriverWait

from common.type import DriverType
from common.utils import DriverUtils


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def __base_find(self, loc, multiple=False):
        logging.debug(f"正在查找元素: {loc}")
        wait = WebDriverWait(self.driver, 10, 0.5)
        if multiple:
            return wait.until(lambda x: x.find_elements(*loc))
        return wait.until(lambda x: x.find_element(*loc))

    def base_find_element(self, loc):
        return self.__base_find(loc, multiple=False)

    def base_find_elements(self, loc):
        return self.__base_find(loc, multiple=True)

    def base_click(self, loc):
        logging.debug(f"正在点击元素:{loc}")
        self.base_find_element(loc).click()

    def base_input(self, loc, value):
        logging.debug(f"正在输入元素:{loc}, value:{value}")
        self.base_find_element(loc).send_keys(value)

    def base_get_attribute(self, loc, attribute_name):
        logging.debug(f"正在获取元素:{loc}, attribute_name:{attribute_name}")
        return self.base_find_element(loc).get_attribute(attribute_name)

    def base_save_screenshot(self, path):
        logging.debug(f"正在保存截图:{path}")
        self.driver.get_screenshot_as_file(path)

    def base_get_size(self, loc):
        logging.debug(f"正在获取元素:{loc}的大小")
        return self.base_find_element(loc).size

    def base_get_location(self, loc):
        logging.debug(f"正在获取元素:{loc}的位置")
        return self.base_find_element(loc).location

    def base_get_text(self, loc):
        logging.debug(f"正在获取元素:{loc}的文本")
        return self.base_find_element(loc).text

    def base_move_seekbar(self, loc, percent, time=100):
        """
        移动拖动条到指定的百分比位置。

        :param loc: 元素定位器
        :param percent: 目标位置的百分比（0 到 100 之间）
        :param time: 滑动时间，默认为100毫秒
        """
        if not (0 <= percent <= 100):
            raise ValueError("percent 参数必须在 0 到 100 之间")

        # 获取拖动条的元素
        element = self.base_find_element(loc)
        # 获取元素的宽度和位置
        width = element.size.get("width")
        x = element.location.get("x")
        y = element.location.get("y")

        # 计算目标坐标
        target_x = x + int(width * (percent / 100))

        # 执行滑动操作
        self.driver.swipe(x, y, target_x, y, time)




class BasePageIos(BasePage):
    def __init__(self,driver):
        super().__init__(driver)


class BasePageAndroid(BasePage):
    def __init__(self,driver):
        super().__init__(driver)
