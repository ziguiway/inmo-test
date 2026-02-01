import json
import logging
import time
import traceback
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

import yaml
from appium import webdriver
from appium.options.android import UiAutomator2Options
from colorama import init, Fore, Style
from selenium.common import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from common.type import DriverType
from common.config import BASE_PATH
from common.logger_utils import LoggerSingleton

logger = LoggerSingleton().get_logger()

class DriverUtils:
    __drivers = {dt: None for dt in DriverType}
    __driver_creation_times = {dt: None for dt in DriverType}  # 记录驱动创建时间
    __max_retries = 3  # 最大重试次数
    __retry_delay = 2  # 重试间隔（秒）

    @classmethod
    def __handle_exception(cls, e, context):
        logger.error(f"{context}失败: {str(e)}\n{traceback.format_exc()}")
        return None

    @classmethod
    def __check_driver_health(cls, driver_type):
        """检查驱动是否健康"""
        driver = cls.__drivers[driver_type]
        if driver is None:
            return False
        
        try:
            # 尝试执行一个简单的操作来检查驱动状态
            driver.current_activity()
            return True
        except WebDriverException:
            logger.warning(f"{driver_type} 驱动连接异常，需要重建")
            return False

    @classmethod
    def __create_driver_with_retry(cls, driver_type, config):
        """带重试机制的驱动创建"""
        last_exception = None
        
        for attempt in range(cls.__max_retries):
            try:
                logger.info(f"尝试创建 {driver_type} 驱动 (尝试 {attempt + 1}/{cls.__max_retries})")
                
                appium_server_url = config.get('serverUrl')
                options = UiAutomator2Options().load_capabilities(config)
                driver = webdriver.Remote(appium_server_url, options=options)
                
                # 设置隐式等待时间
                implicit_wait = config.get('implicitWait', 10)
                driver.implicitly_wait(implicit_wait)
                
                logger.info(f"获取 {driver_type} Driver 成功")
                return driver
                
            except Exception as e:
                last_exception = e
                logger.warning(f"创建 {driver_type} 驱动失败 (尝试 {attempt + 1}/{cls.__max_retries}): {str(e)}")
                
                if attempt < cls.__max_retries - 1:  # 不是最后一次尝试
                    time.sleep(cls.__retry_delay)
        
        # 所有重试都失败了
        cls.__handle_exception(last_exception, f"初始化 {driver_type} 驱动程序，已重试 {cls.__max_retries} 次")
        return None

    @classmethod
    def __get_driver(cls, driver_type, is_reset):
        # 检查现有驱动是否健康
        if cls.__drivers[driver_type] is not None:
            if not cls.__check_driver_health(driver_type):
                logger.info(f"现有 {driver_type} 驱动不健康，准备重建")
                cls.__quit_driver(driver_type)  # 清理不健康的驱动

        if cls.__drivers[driver_type] is None:
            try:
                config = cls.__get_driver_config(driver_type, is_reset)
                driver = cls.__create_driver_with_retry(driver_type, config)
                
                if driver is not None:
                    cls.__drivers[driver_type] = driver
                    cls.__driver_creation_times[driver_type] = time.time()
                else:
                    logger.error(f"无法创建 {driver_type} 驱动，所有重试均已失败")
                    return None
                    
            except Exception as e:
                cls.__handle_exception(e, f"获取 {driver_type} 驱动时发生异常")
                return None

        return cls.__drivers[driver_type]

    @classmethod
    def __quit_driver(cls, driver_type):
        driver = cls.__drivers[driver_type]
        if driver:
            try:
                driver.quit()
                logger.info(f"退出 {driver_type} driver 成功")
            except Exception as e:
                logger.warning(f"退出 {driver_type} driver 时发生异常: {str(e)}")
            finally:
                cls.__drivers[driver_type] = None
                cls.__driver_creation_times[driver_type] = None

    @classmethod
    def __get_driver_config(cls, driver_type, is_reset):
        udid_map = {
            # 改成对应的udid
            DriverType.ANDROID: DriverType.ANDROID.value,
            DriverType.GLASS: DriverType.GLASS.value,
            # DriverType.IOS: DriverType.IOS.value
        }
        udid = udid_map.get(driver_type)
        config_list = FileUtils.load_yaml_config(f"{BASE_PATH}/config.yaml").get("appium").get('devices')
        for config in config_list:
            if config.get('udid') == udid:
                config['noReset'] = not is_reset
                # 设置默认的隐式等待时间
                if 'implicitWait' not in config:
                    config['implicitWait'] = 10
                return config
        raise ValueError(f"未找到适用于 {driver_type.value} 的配置")

    @classmethod
    def get_driver(cls, driver_type, is_reset=True):
        return cls.__get_driver(driver_type, is_reset)

    @classmethod
    def quit_driver(cls, driver_type):
        cls.__quit_driver(driver_type)

    @classmethod
    def quit_all_drivers(cls):
        """退出所有驱动"""
        for driver_type in DriverType:
            cls.quit_driver(driver_type)

    @classmethod
    def get_driver_uptime(cls, driver_type):
        """获取驱动运行时间（秒）"""
        creation_time = cls.__driver_creation_times[driver_type]
        if creation_time is None:
            return 0
        return time.time() - creation_time

    @classmethod
    def force_recreate_driver(cls, driver_type, is_reset=True):
        """强制重建驱动"""
        logger.info(f"强制重建 {driver_type} 驱动")
        cls.__quit_driver(driver_type)
        return cls.get_driver(driver_type, is_reset)

class TimeUtils:
    @staticmethod
    def get_current_timestamp():
        return time.time()

    @staticmethod
    def format_timestamp(timestamp, format_str="%Y-%m-%d %H:%M:%S"):
        return datetime.fromtimestamp(timestamp).strftime(format_str)


class FileUtils:
    @classmethod
    def yaml_to_json(cls, file_path):
        """
        读取 YAML 文件并转换为 JSON
        :param file_path: YAML 文件路径
        :return: JSON 字符串
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as yaml_file:
                # 将 YAML 转换为 Python 对象
                yaml_data = yaml.safe_load(yaml_file)
                # 将 Python 对象转换为 JSON 字符串
                json_data = json.dumps(yaml_data, ensure_ascii=False, indent=2)
                return json_data
        except Exception as e:
            logger.error(f"转换过程出错: {e}")
            return None

    @classmethod
    def load_yaml_config(cls, file_path):
        """
        读取 YAML 配置文件并返回内容。

        :param file_path: YAML 文件的路径
        :return: 配置字典
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                config = yaml.safe_load(file)
            return config
        except Exception as e:
            logger.error(f"读取 YAML 配置出错: {e}")
            return None


class GlassesUtils:

    @classmethod
    def is_screen_on(cls):
        """
        检查屏幕是否处于激活状态
        :return: bool
        """
        driver = DriverUtils.get_driver(DriverType.GLASS)
        try:
            screen_status = driver.execute_script("mobile: shell",
                                                  {"command": "dumpsys power | grep 'mWakefulness'"})
            return 'Awake' in screen_status
        except Exception as e:  # 捕获异常并记录
            logger.error(f"Error checking screen status: {e}")
            return False

    @classmethod
    def start_bluetooth_broadcast(cls, is_reset=False):
        """
        发起蓝牙广播
        :return:
        """
        driver = DriverUtils.get_driver(DriverType.GLASS, is_reset)
        if driver is None:
            logger.error("获取驱动失败")
        else:
            logger.info("开始发起蓝牙广播")
            driver.unlock()
            logger.info("成功发起蓝牙广播")

    @classmethod
    def get_battery_info(cls, is_reset=False):
        """
        获取眼镜电池信息
        :return:
        """
        driver = DriverUtils.get_driver(DriverType.ANDROID, is_reset)
        logger.info("开始获取眼镜电池信息")
        battery_info = driver.execute_script('mobile: batteryInfo')
        logger.info("获取眼镜电池信息成功")
        return battery_info

    @classmethod
    def screenshot(cls, path):
        driver = DriverUtils.get_driver(DriverType.GLASS)
        print(driver)
        driver.save_screenshot(path)


class ElementUtils:

    @classmethod
    def is_el_exist_by_text(cls,driver_type, key_text, timeout=3, poll_frequency=0.5):
        try:
            xpath_str = f"//*[@text='{key_text}']"
            driver = DriverUtils.get_driver(driver_type)
            WebDriverWait(driver, timeout=timeout, poll_frequency=poll_frequency).until(
                EC.presence_of_element_located((By.XPATH, xpath_str))
            )
            return True  # 找到元素，返回 True
        except TimeoutException:
            logger.error(f"元素未找到，[key_text: {key_text}]，超时")
            return False  # 未找到元素，返回 False
        except Exception as e:
            logger.error(f"获取文本元素失败, [key_text: {key_text}], 异常信息: {e}")
            return False  # 其他异常情况也返回 False


class AndroidUtils:
    pass

if __name__ == '__main__':
    # info = GlassesUtils.get_battery_info()
    # print(info)
    GlassesUtils.screenshot("a.png")
