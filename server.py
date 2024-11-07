import logging
import os
import subprocess
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
        command = f'start cmd /C "appium --allow-insecure=adb_shell -p {port}"'
        os.system(command)
        logging.info("在端口 %d 启动 Appium 服务器", port)
        # 启动后等待并检查状态
        if not self.is_running(port):
            logging.error("在端口 %d 启动的 Appium 服务器未能成功启动.", port)

    def start_all(self, port_list=None):
        if port_list is None:
            port_list = self.get_appium_server_ports()
        for port in port_list:
            self.start_by_port(port)
        if not self.are_all_running():
            logging.error("并非所有 Appium 服务器都已成功启动.")

    def is_running(self, port, check_interval=1, timeout=60):
        # 动态等待单个 Appium 服务启动
        return self.check_appium_status(port, timeout, check_interval)

    def are_all_running(self, check_interval=1, timeout=60):
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
                logging.warning("appium服务正在启动，连接失败，正在重试...")

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

    def get_connected_device_udid(self):
        try:
            # 调用 adb devices 命令
            result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # 检查命令是否成功
            if result.returncode == 0:
                # 处理输出，提取设备序列号
                lines = result.stdout.strip().split('\n')
                devices = []
                for line in lines[1:]:  # 跳过第一行标题
                    if line.strip():  # 确保行不为空
                        device_info = line.split('\t')
                        if len(device_info) > 0:
                            devices.append(device_info[0])  # 设备序列号
                return devices
            else:
                logging.error("错误: %s", result.stderr)
                return None
        except FileNotFoundError:
            logging.error("未找到 ADB。请先安装 ADB。")
            return None

    def is_device_connect(self):
        config_udid_list = []
        not_connect_list = []

        # 加载配置文件中的设备信息
        config_list = FileUtils.load_yaml_config(f"{BASE_PATH}/config.yaml")['appium']['devices']
        for config in config_list:
            udid = config.get('udid')
            config_udid_list.append(udid)

        # 获取实际连接的设备 UDID 列表
        actual_udid_list = self.get_connected_device_udid()
        logging.debug(f"实际连接的设备 UDID 列表: {actual_udid_list}")
        logging.debug(f"配置的设备 UDID 列表: {config_udid_list}")

        # 检查每个配置的 UDID 是否在实际连接的设备中
        for item in config_udid_list:
            if item not in actual_udid_list:
                not_connect_list.append(item)

        if not_connect_list:
            logging.error(f"请检查设备的连接后重试,未连接的设备: {not_connect_list}")
            return False

        logging.info(f"所有设备均已连接 UDID 列表: {config_udid_list}")
        return True
if __name__ == "__main__":
    appium_server = AppiumServer()
    # udids = appium_server.get_connected_device_udid()
    appium_server.is_device_connect()
