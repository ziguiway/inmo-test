import logging
import os
from logging.handlers import TimedRotatingFileHandler

from colorama import Fore, Style, init

# 项目根路径
BASE_PATH = os.path.dirname(__file__)

# appium服务地址
APPIUM_SERVER_URL = 'http://127.0.0.1:4723'


# 日志的配置

def basic_log_config():
    init(autoreset=True)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

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
    logger.addHandler(lht)
    logger.addHandler(ls)
