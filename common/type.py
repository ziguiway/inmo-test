from enum import Enum


class DriverType(Enum):
    IOS = 1
    ANDROID = 2
    GLASS = 3


class UdidType(Enum):
    HUAWEI = 'FMR0223B23029252'
    SIMULATOR = 'emulator-5554'
    GLASS = 'YM00SEC7B02551'
