import pytest

from common.logger_utils import LoggerSingleton
from server import AppiumServer

if __name__ == '__main__':
    logger = LoggerSingleton().get_logger()
    appium_server = AppiumServer()
    try:
        is_device_connect = appium_server.is_device_connect()
        if is_device_connect:
            appium_server.start_all()
            pytest.main()
        else:
            logger.error("设备未连接，无法启动测试")
    finally:
        # 确保Appium服务被停止
        appium_server.stop_all()