from enum import Enum


class DriverType(Enum):
    IOS = ""
    ANDROID = "FMR0223B23029252"
    GLASS = "YM00SEC7B02551"


class WifiStatusType(Enum):
    CONNECTED = "已连接"
    UNCONNECTED = "未连接"
    CONNECTING = "连接中"
