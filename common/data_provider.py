"""
数据驱动测试工具类
提供从不同数据源读取测试数据的功能
"""
import json
import csv
import yaml
from typing import List, Dict, Any
from pathlib import Path


class DataProvider:
    """
    数据驱动测试数据提供类
    支持从多种数据源读取测试数据
    """

    @staticmethod
    def load_from_csv(file_path: str, encoding: str = 'utf-8') -> List[Dict[str, Any]]:
        """
        从CSV文件加载测试数据
        :param file_path: CSV文件路径
        :param encoding: 文件编码
        :return: 测试数据列表
        """
        data_list = []
        with open(file_path, 'r', encoding=encoding) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # 将字符串类型的值转换为适当的类型
                converted_row = {}
                for key, value in row.items():
                    converted_row[key] = DataProvider._convert_value(value)
                data_list.append(converted_row)
        return data_list

    @staticmethod
    def load_from_json(file_path: str) -> List[Dict[str, Any]]:
        """
        从JSON文件加载测试数据
        :param file_path: JSON文件路径
        :return: 测试数据列表
        """
        with open(file_path, 'r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                # 如果是字典，将其包装成列表
                return [data]
            else:
                raise TypeError(f"JSON文件应包含数组或对象，但得到了 {type(data)}")

    @staticmethod
    def load_from_yaml(file_path: str) -> List[Dict[str, Any]]:
        """
        从YAML文件加载测试数据
        :param file_path: YAML文件路径
        :return: 测试数据列表
        """
        with open(file_path, 'r', encoding='utf-8') as yamlfile:
            data = yaml.safe_load(yamlfile)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                # 如果是字典，将其包装成列表
                return [data]
            else:
                raise TypeError(f"YAML文件应包含数组或对象，但得到了 {type(data)}")

    @staticmethod
    def load_from_excel(file_path: str, sheet_name: str = None) -> List[Dict[str, Any]]:
        """
        从Excel文件加载测试数据
        :param file_path: Excel文件路径
        :param sheet_name: 工作表名称
        :return: 测试数据列表
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("需要安装pandas和openpyxl: pip install pandas openpyxl")
        
        # 读取Excel文件
        if sheet_name:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
        else:
            df = pd.read_excel(file_path)
        
        # 转换为字典列表
        data_list = df.to_dict('records')
        
        # 转换NaN值为None
        for record in data_list:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
                else:
                    record[key] = DataProvider._convert_value(str(value))
        
        return data_list

    @staticmethod
    def parametrize_test(test_data: List[Dict[str, Any]]) -> List[tuple]:
        """
        将测试数据转换为pytest.param格式
        :param test_data: 测试数据列表
        :return: pytest.param格式的元组列表
        """
        params = []
        for idx, data in enumerate(test_data):
            # 使用第一个键值对作为ID，如果没有则使用索引
            id_value = data.get(list(data.keys())[0], idx) if data.keys() else idx
            params.append((data, id_value))
        return params

    @staticmethod
    def _convert_value(value: str) -> Any:
        """
        尝试将字符串值转换为适当的类型
        :param value: 字符串值
        :return: 转换后的值
        """
        # 尝试转换为布尔值
        if value.lower() in ('true', 'false'):
            return value.lower() == 'true'
        
        # 尝试转换为整数
        try:
            return int(value)
        except ValueError:
            pass
        
        # 尝试转换为浮点数
        try:
            return float(value)
        except ValueError:
            pass
        
        # 返回字符串
        return value


# 示例用法
if __name__ == "__main__":
    # 示例：如何使用DataProvider
    # data = DataProvider.load_from_csv("test_data.csv")
    # print(data)
    pass