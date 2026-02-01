import pytest

from common.logger_utils import LoggerSingleton
from server import AppiumServer
from common.utils import DriverUtils

if __name__ == '__main__':
    logger = LoggerSingleton().get_logger()
    appium_server = AppiumServer()
    try:
        is_device_connect = appium_server.is_device_connect()
        if is_device_connect:
            server_started = appium_server.start_all()
            if server_started:
                logger.info("开始执行测试...")
                pytest.main()
            else:
                logger.error("Appium服务器未能成功启动，无法执行测试")
        else:
            logger.error("设备未连接，无法启动测试")
    except KeyboardInterrupt:
        logger.info("用户中断了测试执行")
    except Exception as e:
        logger.error(f"执行测试过程中发生错误: {e}")
    finally:
        # 确保Appium服务被停止
        appium_server.stop_all()
        # 清理所有驱动
        DriverUtils.quit_all_drivers()
        logger.info("已清理所有资源")