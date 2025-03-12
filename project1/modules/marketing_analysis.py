import streamlit as st
import pandas as pd
import numpy as np

# 导入子模块
from modules.marketing.basic_analysis import perform_basic_analysis
from modules.marketing.channel_analysis import perform_channel_analysis
from modules.marketing.roi_analysis import perform_roi_analysis

def analyze_marketing(data):
    """
    执行营销效果分析
    
    Args:
        data (dict): 包含所有数据集的字典
    """
    # 添加分析选项
    analysis_type = st.radio(
        "选择营销分析类型",
        ["基础营销指标", "渠道效果分析", "ROI和投资回报分析"],
        horizontal=True
    )
    
    # 根据选择执行不同的分析
    if analysis_type == "基础营销指标":
        perform_basic_analysis(data)
    elif analysis_type == "渠道效果分析":
        perform_channel_analysis(data)
    elif analysis_type == "ROI和投资回报分析":
        perform_roi_analysis(data) 