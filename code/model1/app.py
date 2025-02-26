import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 导入子模块
from pages import (
    home, 
    data_sources, 
    web_scraping_basics, 
    advanced_scraping, 
    dynamic_scraping, 
    data_cleaning, 
    text_processing, 
    project_demo,
    data_visualization  # 添加新的数据可视化模块
)

# 页面配置
st.set_page_config(
    page_title="商业智能数据采集与预处理",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 设置应用标题
st.title("商业智能数据采集与预处理")

# 侧边栏导航
st.sidebar.title("导航")
pages = {
    "首页": home,
    "数据源": data_sources,
    "网络爬虫基础": web_scraping_basics,
    "高级爬虫技术": advanced_scraping,
    "动态网页抓取": dynamic_scraping,
    "数据清洗与转换": data_cleaning,
    "文本处理": text_processing,
    "数据可视化": data_visualization,  # 添加新页面到导航
    "项目演示": project_demo
}

# 选择页面
selection = st.sidebar.radio("选择一个页面", list(pages.keys()))

# 显示选定的页面内容
pages[selection].show()

# 添加侧边栏底部信息
st.sidebar.markdown("---")
st.sidebar.info(
    "本应用用于演示数据采集与预处理的各种技术和方法。"
    "所有数据均为模拟数据，仅供学习使用。"
) 