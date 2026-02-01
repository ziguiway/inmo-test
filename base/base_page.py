import time
import os
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.remote.webelement import WebElement

from common.logger_utils import LoggerSingleton
from common.config import BASE_PATH

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.logger = LoggerSingleton().get_logger()
        self.timeout = 10  # 默认超时时间
        self.poll_frequency = 0.5  # 默认轮询频率

    def __base_find(self, loc, timeout, poll_frequency, multiple):
        self.logger.debug(f"正在查找元素: {loc}")
        wait = WebDriverWait(self.driver, timeout, poll_frequency)
        try:
            if multiple:
                elements = wait.until(EC.presence_of_all_elements_located(loc))
                self.logger.debug(f"找到 {len(elements)} 个元素: {loc}")
                return elements
            else:
                element = wait.until(EC.presence_of_element_located(loc))
                self.logger.debug(f"找到元素: {loc}")
                return element
        except TimeoutException:
            self.logger.error(f"查找元素超时: {loc}")
            raise TimeoutException(f"在 {timeout} 秒内未能找到元素: {loc}")

    def base_find_element(self, loc, timeout=None, poll_frequency=None):
        """
        查找单个元素
        :param loc: 元素定位器 (By.ID, "element_id")
        :param timeout: 超时时间，默认使用实例变量
        :param poll_frequency: 轮询频率，默认使用实例变量
        :return: WebElement
        """
        if timeout is None:
            timeout = self.timeout
        if poll_frequency is None:
            poll_frequency = self.poll_frequency
        return self.__base_find(loc, timeout, poll_frequency, multiple=False)

    def base_find_elements(self, loc, timeout=None, poll_frequency=None):
        """
        查找多个元素
        :param loc: 元素定位器 (By.ID, "element_id")
        :param timeout: 超时时间，默认使用实例变量
        :param poll_frequency: 轮询频率，默认使用实例变量
        :return: List[WebElement]
        """
        if timeout is None:
            timeout = self.timeout
        if poll_frequency is None:
            poll_frequency = self.poll_frequency
        return self.__base_find(loc, timeout, poll_frequency, multiple=True)

    def base_click(self, loc, timeout=None):
        """
        点击元素
        :param loc: 元素定位器
        :param timeout: 超时时间
        """
        if timeout is None:
            timeout = self.timeout
        try:
            element = self.wait_for_element_clickable(loc, timeout)
            element.click()
            self.logger.info(f"成功点击元素: {loc}")
        except Exception as e:
            self.logger.error(f"点击元素失败: {loc}, 错误: {str(e)}")
            self.base_save_screenshot(f"click_error_{int(time.time())}.png")
            raise

    def base_click_by_coordinates(self, x, y, pause=0):
        """
        在指定坐标位置点击。
        :param pause:
        :param x: X坐标
        :param y: Y坐标
        """
        driver = self.driver
        actions = ActionChains(driver)
        pointer = PointerInput(interaction.POINTER_TOUCH, "touch")
        actions.w3c_actions = ActionBuilder(driver, mouse=pointer)
        actions.w3c_actions.pointer_action.move_to_location(x, y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(pause)
        actions.w3c_actions.pointer_action.pointer_up()
        actions.perform()

    def base_input(self, loc, value, clear_first=True, timeout=None):
        """
        在元素中输入文本
        :param loc: 元素定位器
        :param value: 要输入的值
        :param clear_first: 是否先清空元素内容
        :param timeout: 超时时间
        """
        if timeout is None:
            timeout = self.timeout
        try:
            element = self.wait_for_element_clickable(loc, timeout)
            if clear_first:
                element.clear()
            element.send_keys(value)
            self.logger.info(f"成功在元素 {loc} 输入值: {value}")
        except Exception as e:
            self.logger.error(f"输入文本失败: {loc}, 错误: {str(e)}")
            self.base_save_screenshot(f"input_error_{int(time.time())}.png")
            raise

    def base_get_attribute(self, loc, attribute_name, timeout=None):
        """
        获取元素属性
        :param loc: 元素定位器
        :param attribute_name: 属性名称
        :param timeout: 超时时间
        :return: 属性值
        """
        if timeout is None:
            timeout = self.timeout
        try:
            element = self.base_find_element(loc, timeout)
            value = element.get_attribute(attribute_name)
            self.logger.debug(f"元素 {loc} 的属性 {attribute_name} 值为: {value}")
            return value
        except Exception as e:
            self.logger.error(f"获取元素属性失败: {loc}, 错误: {str(e)}")
            raise

    def base_save_screenshot(self, path=None):
        """
        保存截图
        :param path: 截图保存路径，如果为None则生成默认路径
        :return: 截图文件路径
        """
        if path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_dir = os.path.join(BASE_PATH, "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            path = os.path.join(screenshot_dir, f"screenshot_{timestamp}.png")
        
        result = self.driver.get_screenshot_as_file(path)
        self.logger.info(f"截图已保存至: {path}")
        return path

    def base_get_size(self, loc):
        self.logger.debug(f"正在获取元素:{loc}的大小")
        return self.base_find_element(loc).size

    def base_get_location(self, loc):
        self.logger.debug(f"正在获取元素:{loc}的位置")
        return self.base_find_element(loc).location

    def base_get_text(self, loc, timeout=None):
        """
        获取元素文本
        :param loc: 元素定位器
        :param timeout: 超时时间
        :return: 元素文本
        """
        if timeout is None:
            timeout = self.timeout
        try:
            element = self.base_find_element(loc, timeout)
            text = element.text
            self.logger.debug(f"元素 {loc} 的文本为: {text}")
            return text
        except Exception as e:
            self.logger.error(f"获取元素文本失败: {loc}, 错误: {str(e)}")
            raise

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

    def base_swipe_screen(self, start_x, start_y, end_x, end_y, duration=1000):
        """
        在屏幕上进行滑动操作。

        :param start_x: 滑动开始点的X坐标
        :param start_y: 滑动开始点的Y坐标
        :param end_x: 滑动结束点的X坐标
        :param end_y: 滑动结束点的Y坐标
        :param duration: 滑动操作的持续时间（毫秒），默认为1000ms
        """
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)

    def wait_for_element_clickable(self, loc, timeout=None):
        """
        等待元素可点击
        :param loc: 元素定位器
        :param timeout: 超时时间
        :return: WebElement
        """
        if timeout is None:
            timeout = self.timeout
        wait = WebDriverWait(self.driver, timeout, self.poll_frequency)
        try:
            element = wait.until(EC.element_to_be_clickable(loc))
            self.logger.debug(f"元素可点击: {loc}")
            return element
        except TimeoutException:
            self.logger.error(f"元素在 {timeout} 秒内不可点击: {loc}")
            raise TimeoutException(f"元素在 {timeout} 秒内不可点击: {loc}")

    def wait_for_element_visible(self, loc, timeout=None):
        """
        等待元素可见
        :param loc: 元素定位器
        :param timeout: 超时时间
        :return: WebElement
        """
        if timeout is None:
            timeout = self.timeout
        wait = WebDriverWait(self.driver, timeout, self.poll_frequency)
        try:
            element = wait.until(EC.visibility_of_element_located(loc))
            self.logger.debug(f"元素可见: {loc}")
            return element
        except TimeoutException:
            self.logger.error(f"元素在 {timeout} 秒内不可见: {loc}")
            raise TimeoutException(f"元素在 {timeout} 秒内不可见: {loc}")

    def is_element_present(self, loc, timeout=1):
        """
        检查元素是否存在（不等待）
        :param loc: 元素定位器
        :param timeout: 超时时间
        :return: bool
        """
        try:
            self.base_find_element(loc, timeout=timeout)
            return True
        except TimeoutException:
            return False

    def scroll_to_element(self, loc, direction="down", distance=1000):
        """
        滚动到指定元素
        :param loc: 元素定位器
        :param direction: 滚动方向 ("up", "down", "left", "right")
        :param distance: 滚动距离
        """
        # 先尝试查找元素
        try:
            element = self.base_find_element(loc, timeout=1)  # 短暂等待，看元素是否已存在
            self.logger.info(f"元素已存在，无需滚动: {loc}")
            return element
        except TimeoutException:
            # 元素不存在，开始滚动查找
            directions = {
                "down": (0, -distance),
                "up": (0, distance),
                "left": (distance, 0),
                "right": (-distance, 0)
            }
            
            if direction not in directions:
                raise ValueError(f"不支持的方向: {direction}")
            
            dx, dy = directions[direction]
            
            # 尝试滚动并查找元素
            for i in range(5):  # 最多尝试5次滚动
                try:
                    # Android原生滚动
                    self.driver.swipe(self.driver.get_window_size()['width'] // 2,
                                    self.driver.get_window_size()['height'] // 2,
                                    self.driver.get_window_size()['width'] // 2 + dx,
                                    self.driver.get_window_size()['height'] // 2 + dy, 500)
                    
                    # 检查元素是否出现
                    element = self.base_find_element(loc, timeout=2)
                    self.logger.info(f"滚动后找到元素: {loc}")
                    return element
                except TimeoutException:
                    self.logger.debug(f"第{i+1}次滚动未找到元素，继续滚动...")
                    time.sleep(0.5)
            
            raise TimeoutException(f"滚动查找元素失败: {loc}")

    def base_clear(self, loc, timeout=None):
        """
        清空元素内容
        :param loc: 元素定位器
        :param timeout: 超时时间
        """
        if timeout is None:
            timeout = self.timeout
        try:
            element = self.wait_for_element_clickable(loc, timeout)
            element.clear()
            self.logger.info(f"成功清空元素: {loc}")
        except Exception as e:
            self.logger.error(f"清空元素失败: {loc}, 错误: {str(e)}")
            raise

    def base_submit(self, loc, timeout=None):
        """
        提交表单
        :param loc: 元素定位器
        :param timeout: 超时时间
        """
        if timeout is None:
            timeout = self.timeout
        try:
            element = self.base_find_element(loc, timeout)
            element.submit()
            self.logger.info(f"成功提交表单元素: {loc}")
        except Exception as e:
            self.logger.error(f"提交表单失败: {loc}, 错误: {str(e)}")
            raise




class BasePageIos(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.platform = "iOS"
        self.logger.info("初始化iOS基础页面类")


class BasePageAndroid(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.platform = "Android"
        self.logger.info("初始化Android基础页面类")
    
    def swipe_up(self, duration=1000):
        """
        向上滑动
        :param duration: 滑动持续时间
        """
        window_size = self.driver.get_window_size()
        start_x = window_size['width'] // 2
        start_y = window_size['height'] * 0.8
        end_y = window_size['height'] * 0.2
        self.driver.swipe(start_x, start_y, start_x, end_y, duration)
        self.logger.debug("向上滑动")
    
    def swipe_down(self, duration=1000):
        """
        向下滑动
        :param duration: 滑动持续时间
        """
        window_size = self.driver.get_window_size()
        start_x = window_size['width'] // 2
        start_y = window_size['height'] * 0.2
        end_y = window_size['height'] * 0.8
        self.driver.swipe(start_x, start_y, start_x, end_y, duration)
        self.logger.debug("向下滑动")
    
    def swipe_left(self, duration=1000):
        """
        向左滑动
        :param duration: 滑动持续时间
        """
        window_size = self.driver.get_window_size()
        start_x = window_size['width'] * 0.8
        start_y = window_size['height'] // 2
        end_x = window_size['width'] * 0.2
        self.driver.swipe(start_x, start_y, end_x, start_y, duration)
        self.logger.debug("向左滑动")
    
    def swipe_right(self, duration=1000):
        """
        向右滑动
        :param duration: 滑动持续时间
        """
        window_size = self.driver.get_window_size()
        start_x = window_size['width'] * 0.2
        start_y = window_size['height'] // 2
        end_x = window_size['width'] * 0.8
        self.driver.swipe(start_x, start_y, end_x, start_y, duration)
        self.logger.debug("向右滑动")
