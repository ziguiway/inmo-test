import pytest

from config import LoggerSingleton
from server import AppiumServer

if __name__ == '__main__':
    logger = LoggerSingleton.get_instance().get_logger()
    appium_server = AppiumServer()
    appium_server.start_all()
    pytest.main()
    # appium_server.stop_all()