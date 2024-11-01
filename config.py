import logging
import os
from logging.handlers import TimedRotatingFileHandler

from colorama import init, Fore, Style

# 项目根路径
BASE_PATH = os.path.dirname(__file__)



# 日志的配置
class LoggerSingleton:
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


# 使用示例
if __name__ == "__main__":
    logger = LoggerSingleton.get_instance().get_logger()
    logger.info("日志配置完成")
