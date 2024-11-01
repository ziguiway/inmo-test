import logging
import os
import time
from urllib.parse import urlparse

import psutil
import requests

from common.utils import FileUtils
from config import BASE_PATH


class AppiumServer:
    def get_appium_server_ports(self):
        # 读取配置文件获取所有 Appium 服务器的端口
        port_list = []
        config_list = FileUtils.load_yaml_config(f"{BASE_PATH}/config.yaml")['appium']['devices']
        for config in config_list:
            port = urlparse(config['serverUrl']).port
            port_list.append(port)
        return port_list

    def start_by_port(self, port=4723):
        command = f'start cmd /K "appium --allow-insecure=adb_shell -p {port}"'
        os.system(command)
        logging.info("在端口 %d 启动 Appium 服务器", port)

    def start_all(self, port_list=None):
        if port_list is None:
            port_list = self.get_appium_server_ports()

        # 检查所有 Appium 服务器是否已经运行
        if self.are_all_running():
            logging.info("所有 Appium 服务器已经在运行，无需重新启动.")
            return

        failed_ports = []  # 用于记录启动失败的端口

        for port in port_list:
            self.start_by_port(port)
            # 启动后检查服务器状态
            if not self.is_running(port):
                failed_ports.append(port)

        if failed_ports:
            logging.error("以下端口的 Appium 服务器未能成功启动: %s", ', '.join(map(str, failed_ports)))
        else:
            logging.info("所有 Appium 服务器已成功启动.")

    def is_running(self, port, check_interval=1, timeout=30):
        # 动态等待单个 Appium 服务启动
        return self.check_appium_status(port, timeout, check_interval)

    def are_all_running(self, check_interval=1, timeout=30):
        # 检查所有 Appium 服务器是否已启动
        port_list = self.get_appium_server_ports()
        all_running = True

        for port in port_list:
            if not self.check_appium_status(port, timeout, check_interval):
                all_running = False

        return all_running

    def check_appium_status(self, port, timeout, check_interval):
        # 检查指定端口的 Appium 服务状态
        start_time = time.time()
        while True:
            try:
                response = requests.get(f'http://127.0.0.1:{port}/status')
                if response.status_code == 200:
                    logging.info("Appium 服务器在端口 %d 已启动并运行.", port)
                    return True
            except requests.ConnectionError:
                logging.warning("连接失败，正在重试...")

            if time.time() - start_time > timeout:
                logging.error("等待 Appium 服务器在端口 %d 超时.", port)
                return False
            time.sleep(check_interval)

    def stop_all(self):
        # 停止所有启动的 Appium 进程
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'node.exe':
                proc.terminate()  # 终止进程
                logging.info("停止了 PID 为 %d 的 Appium 服务器", proc.info['pid'])


# 使用示例
if __name__ == "__main__":
    appium_server = AppiumServer()
    appium_server.start_all()
