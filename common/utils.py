import json
import logging
import time
import traceback
from datetime import datetime

import yaml
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.common import NoSuchElementException

from common.type import DriverType, UdidType
from config import BASE_PATH


class DriverUtils:
    __drivers = {
        DriverType.ANDROID: None,
        DriverType.IOS: None,
        DriverType.GLASS: None
    }

    @classmethod
    def __get_driver(cls, driver_type):
        if cls.__drivers[driver_type] is None:
            try:
                config = cls.__get_driver_config(driver_type)
                appium_server_url = config.get('serverUrl')
                options = UiAutomator2Options().load_capabilities(config)
                cls.__drivers[driver_type] = webdriver.Remote(appium_server_url, options=options)
                cls.__drivers[driver_type].implicitly_wait(30)
                logging.info(f'获取 {driver_type} Driver 成功')
            except Exception as e:
                logging.error(f'初始化 {driver_type} 驱动程序失败: {traceback.format_exc()}')
                cls.__drivers[driver_type] = None
        return cls.__drivers[driver_type]

    @classmethod
    def __quit_driver(cls, driver_type):
        driver = cls.__drivers[driver_type]
        if driver:
            driver.quit()
            logging.info(f'退出 {driver_type} driver 成功')
            cls.__drivers[driver_type] = None

    @classmethod
    def __get_driver_config(cls, driver_type):
        udid_map = {
            DriverType.ANDROID: UdidType.HUAWEI.value,
            DriverType.GLASS: UdidType.GLASS.value,
            # DriverType.IOS: UdidType.IOS.value  # 确保添加 iOS 对应的 udid
        }

        udid = udid_map.get(driver_type)

        config_list = FileUtils.load_yaml_config(f"{BASE_PATH}/config.yaml").get("appium").get('devices')
        for config in config_list:
            if config.get('udid') == udid:
                return {
                    "udid": config.get('udid'),
                    "platformName": config.get('platformName'),
                    "automationName": config.get('automationName'),
                    "deviceName": config.get('deviceName'),
                    "appPackage": config.get('appPackage'),
                    "appActivity": config.get('appActivity'),
                    "serverUrl": config.get('serverUrl'),
                    "noReset": config.get('noReset'),
                }
        raise ValueError(f"未找到适用于 {driver_type} 的配置")

    @classmethod
    def get_driver(cls, driver_type):
        return cls.__get_driver(driver_type)

    @classmethod
    def quit_driver(cls, driver_type):
        cls.__quit_driver(driver_type)


class TimeUtils:
    @staticmethod
    def get_current_timestamp():
        """获取当前时间的时间戳（浮点数）"""
        return time.time()

    @staticmethod
    def get_current_timestamp_int():
        """获取当前时间的时间戳（整数）"""
        return int(time.time())

    @staticmethod
    def format_timestamp(timestamp, format_str="%Y-%m-%d %H:%M:%S"):
        """将时间戳格式化为指定格式的时间字符串"""
        return datetime.fromtimestamp(timestamp).strftime(format_str)

    @staticmethod
    def parse_time_string(time_str, format_str="%Y-%m-%d %H:%M:%S"):
        """将时间字符串解析为时间对象"""
        return datetime.strptime(time_str, format_str)

    @staticmethod
    def get_time_difference(start_time, end_time):
        """计算两个时间之间的差值（秒）"""
        return (end_time - start_time).total_seconds()


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
    @staticmethod
    def is_screen_on(driver):
        try:
            screen_status = driver.execute_script("mobile: shell", {"command": "dumpsys power | grep 'mWakefulness'"})
            return 'Awake' in screen_status
        except Exception:  # 捕获更广泛的异常
            return False

    @classmethod
    def start_bluetooth_broadcast(cls):
        driver = DriverUtils.get_driver(DriverType.GLASS)
        is_on = cls.is_screen_on(driver)
        if is_on:
            driver.lock()
            driver.unlock()
        else:
            driver.unlock()

