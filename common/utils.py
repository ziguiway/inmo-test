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
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from common.type import DriverType
from config import BASE_PATH


class DriverUtils:
    __drivers = {dt: None for dt in DriverType}

    @classmethod
    def __handle_exception(cls, e, context):
        logging.error(f"{context}失败: {traceback.format_exc()}")
        return None

    @classmethod
    def __get_driver(cls, driver_type, is_reset):
        if cls.__drivers[driver_type] is None:
            try:
                config = cls.__get_driver_config(driver_type, is_reset)
                appium_server_url = config.get('serverUrl')
                options = UiAutomator2Options().load_capabilities(config)
                cls.__drivers[driver_type] = webdriver.Remote(appium_server_url, options=options)
                cls.__drivers[driver_type].implicitly_wait(30)
                logging.info(f"获取 {driver_type} Driver 成功")
            except Exception as e:
                cls.__handle_exception(e, f"初始化 {driver_type} 驱动程序")
        return cls.__drivers[driver_type]

    @classmethod
    def __quit_driver(cls, driver_type):
        driver = cls.__drivers[driver_type]
        if driver:
            driver.quit()
            logging.info(f"退出 {driver_type} driver 成功")
            cls.__drivers[driver_type] = None

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
                return config
        raise ValueError(f"未找到适用于 {driver_type.value} 的配置")

    @classmethod
    def get_driver(cls, driver_type, is_reset=True):
        return cls.__get_driver(driver_type, is_reset)

    @classmethod
    def quit_driver(cls, driver_type):
        cls.__quit_driver(driver_type)


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
            logging.error(f"转换过程出错: {e}")
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
            logging.error(f"读取 YAML 配置出错: {e}")
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
            logging.error(f"Error checking screen status: {e}")
            return False

    @classmethod
    def start_bluetooth_broadcast(cls):
        """
        发起蓝牙广播
        :return:
        """
        driver = DriverUtils.get_driver(DriverType.GLASS)
        if driver is None:
            logging.error("获取驱动失败")
        else:
            logging.info("开始发起蓝牙广播")
            driver.unlock()
            logging.info("成功发起蓝牙广播")

    @classmethod
    def get_battery_info(cls):
        """
        获取眼镜电池信息
        :return:
        """
        driver = DriverUtils.get_driver(DriverType.ANDROID)
        logging.info("开始获取眼镜电池信息")
        battery_info = driver.execute_script('mobile: batteryInfo')
        logging.info("获取眼镜电池信息成功")
        return battery_info

    @classmethod
    def screenshot(cls, path):
        driver = DriverUtils.get_driver(DriverType.GLASS)
        print(driver)
        driver.save_screenshot(path)

class LoggerUtils:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
            cls._instance.init_logger()
        return cls._instance

    def init_logger(self):
        init(autoreset=True)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        # 文件处理器，用于记录日志到文件
        lht = TimedRotatingFileHandler(
            filename=f"{BASE_PATH}/log/inmo_test.log",
            when="midnight",
            interval=1,
            encoding="utf-8",
            backupCount=2
        )

        # 控制台处理器，用于记录日志到控制台
        ls = logging.StreamHandler()

        # 自定义日志格式器，用于控制台输出
        class ColoredFormatter(logging.Formatter):
            COLORS = {
                'DEBUG': Fore.WHITE,
                'INFO': Fore.GREEN,
                'WARNING': Fore.YELLOW,
                'ERROR': Fore.RED,
                'CRITICAL': Fore.MAGENTA + Style.BRIGHT,  # 紫色
                'TRACE': Fore.CYAN,  # 可选的浅蓝色
            }

            def format(self, record):
                color = self.COLORS.get(record.levelname, Fore.WHITE)
                message = super().format(record)
                return f"{color}{message}{Style.RESET_ALL}"

        # 日志格式
        fmt = "%(asctime)s %(levelname)s [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s"

        # 控制台格式器，带颜色
        colored_formatter = ColoredFormatter(fmt)
        ls.setFormatter(colored_formatter)

        # 文件格式器，不带颜色
        file_formatter = logging.Formatter(fmt)
        lht.setFormatter(file_formatter)

        # 将处理器添加到记录器
        self.logger.addHandler(lht)
        self.logger.addHandler(ls)

    def get_logger(self):
        return self.logger


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
            logging.error(f"元素未找到，[key_text: {key_text}]，超时")
            return False  # 未找到元素，返回 False
        except Exception as e:
            logging.error(f"获取文本元素失败, [key_text: {key_text}], 异常信息: {e}")
            return False  # 其他异常情况也返回 False


class AndroidUtils:
    pass

if __name__ == '__main__':
    # info = GlassesUtils.get_battery_info()
    # print(info)
    GlassesUtils.screenshot("a.png")
