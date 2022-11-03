import os
import sys

# 项目跟目录加入 path搜索中
hp = os.path.join(os.path.dirname(__file__), '..')
hp = os.path.abspath(hp)
sys.path.append(hp)