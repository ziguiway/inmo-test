import pytest

from server import AppiumServer

if __name__ == '__main__':
    from config import LoggerSingleton

    logger = LoggerSingleton.get_instance().get_logger()

    appium_server = AppiumServer()
    appium_server.start_all()
    pytest.main()