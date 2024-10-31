import subprocess
from urllib.parse import urlparse

from common.utils import FileUtils
from config import BASE_PATH




class AppiumServer:
    """
    Appium Server
    疑似Windows权限导致命令不能执行
    """

    def __init__(self):
        self.processes = []

    def read_config(self):
        config = FileUtils.load_yaml_config(f"{BASE_PATH}/config.yaml")['appium']['devices']
        print(config)

    def extract_port(self, server_url):
        parsed_url = urlparse(server_url)
        return parsed_url.port

    def start_appium(self, port):
        # 确保 port 是字符串
        process = subprocess.Popen(['appium', '--allow-insecure=adb_shell', '-p', str(port)])
        self.processes.append(process)  # 将进程添加到列表中
        return process


# port = AppiumServer().extract_port("http://127.0.0.1:4723")
# AppiumServer().start_appium(port)
# subprocess.Popen(['start', 'cmd', '/K', 'appium --allow-insecure=adb_shell -p 4724'], shell=False)
# subprocess.Popen(['start', 'cmd'])