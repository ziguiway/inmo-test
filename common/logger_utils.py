import logging
from logging.handlers import TimedRotatingFileHandler
from colorama import init, Fore, Style

from common.config import BASE_PATH


class LoggerSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._setup_logger()
            self._initialized = True

    def _setup_logger(self):
        init(autoreset=True)
        self.logger = logging.getLogger('inmo_test')
        self.logger.setLevel(logging.INFO)
        
        # 避免重复添加处理器
        if not self.logger.handlers:
            # 文件处理器，用于记录日志到文件
            file_handler = TimedRotatingFileHandler(
                filename=f"{BASE_PATH}/log/inmo_test.log",
                when="midnight",
                interval=1,
                encoding="utf-8",
                backupCount=2
            )
    
            # 控制台处理器，用于记录日志到控制台
            console_handler = logging.StreamHandler()
    
            # 日志格式
            fmt = "%(asctime)s %(levelname)s [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s"
    
            # 自定义日志格式器，用于控制台输出
            class ColoredFormatter(logging.Formatter):
                COLORS = {
                    'DEBUG': Fore.WHITE,
                    'INFO': Fore.GREEN,
                    'WARNING': Fore.YELLOW,
                    'ERROR': Fore.RED,
                    'CRITICAL': Fore.MAGENTA + Style.BRIGHT,
                }
    
                def format(self, record):
                    color = self.COLORS.get(record.levelname, Fore.WHITE)
                    message = super().format(record)
                    return f"{color}{message}{Style.RESET_ALL}"
    
            # 设置处理器格式
            console_handler.setFormatter(ColoredFormatter(fmt))
            file_handler.setFormatter(logging.Formatter(fmt))
    
            # 添加处理器到logger
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger