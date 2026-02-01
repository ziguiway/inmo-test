import os
import subprocess
import time
from urllib.parse import urlparse

from common.logger_utils import LoggerSingleton

import psutil
import requests

from common.utils import FileUtils
from common.config import BASE_PATH


class AppiumServer:
    def __init__(self):
        self.logger = LoggerSingleton().get_logger()
        
    def get_appium_server_ports(self):
        """读取配置文件获取所有 Appium 服务器的端口"""
        port_list = []
        config_list = FileUtils.load_yaml_config(f"{BASE_PATH}/config.yaml")['appium']['devices']
        for config in config_list:
            port = urlparse(config['serverUrl']).port
            port_list.append(port)
        return port_list

    def start_by_port(self, port=4723):
        """在指定端口启动 Appium 服务器"""
        command = f'start cmd /C "appium --allow-insecure=adb_shell -p {port}"'
        try:
            os.system(command)
            # 启动后等待并检查状态
            self.is_running(port)
        except Exception as e:
            self.logger.error("启动 Appium 服务器失败: %s", e)

    def start_all(self, port_list=None):
        """启动所有配置的 Appium 服务器"""
        if port_list is None:
            port_list = self.get_appium_server_ports()
        for port in port_list:
            self.start_by_port(port)
        self.are_all_running()

    def is_running(self, port, check_interval=1, timeout=60):
        """检查单个 Appium 服务是否启动"""
        return self.check_appium_status(port, timeout, check_interval)

    def are_all_running(self, check_interval=1, timeout=60):
        """检查所有 Appium 服务器是否已启动"""
        port_list = self.get_appium_server_ports()
        all_running = True

        for port in port_list:
            if not self.check_appium_status(port, timeout, check_interval):
                all_running = False

        if all_running:
            self.logger.info("所有 Appium 服务器均已成功启动.")
        return all_running

    def check_appium_status(self, port, timeout, check_interval):
        """检查指定端口的 Appium 服务状态"""
        start_time = time.time()
        server_started = False

        while True:
            try:
                response = requests.get(f'http://127.0.0.1:{port}/status')
                if response.status_code == 200:
                    if not server_started:
                        self.logger.info("Appium 服务器在端口 %d 已启动并运行.", port)
                        server_started = True
                    return True
                elif server_started:
                    # 如果已经启动，返回成功，不记录日志
                    return True
            except requests.ConnectionError:
                if not server_started:
                    self.logger.warning("Appium 服务正在启动，连接失败，正在重试...")

            if time.time() - start_time > timeout:
                self.logger.error("等待 Appium 服务器在端口 %d 超时.", port)
                return False
            time.sleep(check_interval)

    def stop_all(self):
        """停止所有启动的 Appium 进程"""
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                # 检查进程命令行是否包含appium关键字，确保只终止Appium相关进程
                if proc.info['name'] == 'node.exe' and proc.info['cmdline'] and any('appium' in cmd.lower() for cmd in proc.info['cmdline']):
                    proc.terminate()  # 终止进程
                    self.logger.info("停止了 PID 为 %d 的 Appium 服务器", proc.info['pid'])
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # 忽略访问权限问题或其他异常
                pass

    def get_connected_device_udid(self):
        """获取连接的设备 UDID 列表"""
        try:
            result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                devices = []
                for line in lines[1:]:  # 跳过第一行标题
                    if line.strip():
                        device_info = line.split('\t')
                        if len(device_info) > 0:
                            devices.append(device_info[0])  # 设备序列号
                return devices
            else:
                self.logger.error("错误: %s", result.stderr)
                return None
        except FileNotFoundError:
            self.logger.error("未找到 ADB。请先安装 ADB。")
            return None

    def is_device_connect(self):
        """检查所有配置的设备是否已连接"""
        config_udid_list = []
        not_connect_list = []

        # 加载配置文件中的设备信息
        config_list = FileUtils.load_yaml_config(f"{BASE_PATH}/config.yaml")['appium']['devices']
        for config in config_list:
            udid = config.get('udid')
            config_udid_list.append(udid)

        # 获取实际连接的设备 UDID 列表
        actual_udid_list = self.get_connected_device_udid()
        self.logger.debug(f"实际连接的设备 UDID 列表: {actual_udid_list}")
        self.logger.debug(f"配置的设备 UDID 列表: {config_udid_list}")

        # 检查每个配置的 UDID 是否在实际连接的设备中
        for item in config_udid_list:
            if item not in actual_udid_list:
                not_connect_list.append(item)

        if not_connect_list:
            self.logger.error(f"请检查设备的连接后重试, 未连接的设备: {not_connect_list}")
            return False

        self.logger.info(f"所有设备均已连接 UDID 列表: {config_udid_list}")
        return True


if __name__ == "__main__":
    # 用于测试AppiumServer功能
    appium_server = AppiumServer()
    appium_server.is_device_connect()