import os

# 项目根路径
BASE_PATH = os.path.dirname(os.path.dirname(__file__))  # 获取项目根目录

if __name__ == "__main__":
    print(f"项目根路径: {BASE_PATH}")