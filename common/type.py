from enum import Enum


class DriverType(Enum):
    IOS = ""
    ANDROID = "SXQ0223511006353"
    GLASS = "28918606999183"


class WifiStatusType(Enum):
    CONNECTED = "已连接"
    UNCONNECTED = "未连接"
    CONNECTING = "连接中"
