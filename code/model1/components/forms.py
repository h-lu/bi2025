import streamlit as st
import pandas as pd
import numpy as np
import io
import re
import requests
from utils.parsers import load_html_file
from bs4 import BeautifulSoup

def url_input_form(label="请输入网址", placeholder="https://example.com", 
                  button_text="抓取数据", help_text=None):
    """显示URL输入表单，返回用户输入的URL"""
    with st.form(key="url_input_form"):
        url = st.text_input(label, placeholder=placeholder, help=help_text)
        submitted = st.form_submit_button(button_text)
    
    if submitted:
        # 验证URL格式
        if not url or not re.match(r'^https?://', url):
            st.error("请输入有效的URL，以http://或https://开头")
            return None
        return url
    return None

def fetch_url_content(url, timeout=10, user_agent=None):
    """抓取URL内容"""
    if user_agent is None:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    
    headers = {
        "User-Agent": user_agent
    }
    
    try:
        # 显示进度
        with st.spinner(f"正在抓取 {url}..."):
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()  # 如果状态码不是200系列，抛出异常
            
            # 检查内容类型
            content_type = response.headers.get('Content-Type', '')
            if 'text/html' in content_type:
                return response.text, "html"
            elif 'application/json' in content_type:
                return response.json(), "json"
            else:
                return response.content, "binary"
    
    except requests.exceptions.Timeout:
        st.error(f"抓取超时: {url}")
    except requests.exceptions.ConnectionError:
        st.error(f"连接错误: {url}")
    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP错误: {url} - {e}")
    except requests.exceptions.RequestException as e:
        st.error(f"抓取错误: {e}")
    except ValueError as e:
        st.error(f"解析错误: {e}")
    
    return None, None

def text_analysis_form(default_text=""):
    """文本分析表单，返回用户输入的文本"""
    with st.form(key="text_analysis_form"):
        text = st.text_area("请输入要分析的文本", value=default_text, height=200)
        col1, col2 = st.columns(2)
        
        with col1:
            options = st.multiselect(
                "分析选项",
                ["分词", "关键词提取", "情感分析", "文本统计", "词云"],
                default=["分词", "关键词提取", "情感分析"]
            )
        
        with col2:
            use_jieba = st.checkbox("使用结巴分词(中文文本)", value=True)
            remove_stopwords = st.checkbox("去除停用词", value=True)
        
        submitted = st.form_submit_button("分析")
    
    if submitted:
        if not text:
            st.error("请输入文本")
            return None, None, None, None
        return text, options, use_jieba, remove_stopwords
    return None, None, None, None

def file_upload_form(file_types=None, label="上传文件"):
    """文件上传表单，返回上传的文件"""
    if file_types is None:
        file_types = ["csv", "xlsx", "txt", "json", "html"]
    
    # 构建文件类型描述
    type_desc = {
        "csv": "CSV",
        "xlsx": "Excel",
        "txt": "文本",
        "json": "JSON",
        "html": "HTML",
        "xml": "XML",
        "pdf": "PDF",
        "jpg": "图片",
        "png": "图片",
        "jpeg": "图片"
    }
    description = ", ".join([type_desc.get(t, t.upper()) for t in file_types])
    
    # 构建文件类型参数
    types_param = []
    for t in file_types:
        if t in ["jpg", "png", "jpeg"]:
            types_param.append(f"image/{t}")
        else:
            if t == "xlsx":
                types_param.append("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            else:
                types_param.append(f"{type_desc.get(t, 'application').lower()}/{t}")
    
    # 显示上传控件
    uploaded_file = st.file_uploader(f"{label} ({description})", type=file_types)
    
    if uploaded_file is not None:
        # 根据文件类型进行处理
        file_type = uploaded_file.name.split(".")[-1].lower()
        
        try:
            if file_type == "csv":
                encoding_options = ["utf-8", "gbk", "latin1"]
                encoding = st.selectbox("选择文件编码", options=encoding_options)
                separator = st.selectbox("选择分隔符", options=[",", ";", "\t", "|"], format_func=lambda x: "Tab" if x == "\t" else x)
                df = pd.read_csv(uploaded_file, encoding=encoding, sep=separator)
                return df, file_type
            
            elif file_type == "xlsx":
                sheet_name = st.text_input("工作表名称 (留空将读取第一个工作表)", "")
                if not sheet_name:
                    sheet_name = 0
                df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
                return df, file_type
            
            elif file_type == "txt":
                content = uploaded_file.read().decode("utf-8")
                return content, file_type
            
            elif file_type == "json":
                return pd.read_json(uploaded_file), file_type
            
            elif file_type == "html":
                content = uploaded_file.read().decode("utf-8")
                soup = BeautifulSoup(content, "html.parser")
                return soup, file_type
            
            else:
                return uploaded_file, file_type
                
        except Exception as e:
            st.error(f"读取文件时出错: {e}")
            return None, None
    
    return None, None

def data_cleaning_form(df):
    """数据清洗表单，返回清洗选项"""
    with st.form(key="data_cleaning_form"):
        st.subheader("数据清洗选项")
        
        # 选择数值列处理
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if numeric_cols:
            st.write("数值列处理:")
            selected_numeric_cols = st.multiselect(
                "选择要处理的数值列",
                options=numeric_cols
            )
            
            if selected_numeric_cols:
                handle_missing_numeric = st.selectbox(
                    "处理缺失值方式",
                    options=["mean", "median", "mode", "drop", "zero"],
                    format_func=lambda x: {
                        "mean": "均值填充", 
                        "median": "中位数填充", 
                        "mode": "众数填充", 
                        "drop": "删除缺失行", 
                        "zero": "填充为0"
                    }.get(x, x)
                )
                
                handle_outliers = st.checkbox("处理异常值", value=True)
        else:
            selected_numeric_cols = []
            handle_missing_numeric = "mean"
            handle_outliers = False
        
        # 选择文本列处理
        text_cols = df.select_dtypes(include=['object']).columns.tolist()
        if text_cols:
            st.write("文本列处理:")
            selected_text_cols = st.multiselect(
                "选择要处理的文本列",
                options=text_cols
            )
            
            if selected_text_cols:
                lower_case = st.checkbox("转为小写", value=True)
                remove_punctuation = st.checkbox("移除标点", value=True)
                remove_numbers = st.checkbox("移除数字", value=False)
                remove_html = st.checkbox("移除HTML标签", value=True)
                remove_extra_spaces = st.checkbox("移除多余空格", value=True)
        else:
            selected_text_cols = []
            lower_case = True
            remove_punctuation = True
            remove_numbers = False
            remove_html = True
            remove_extra_spaces = True
        
        # 其他通用处理
        remove_dupes = st.checkbox("移除重复行", value=True)
        
        submitted = st.form_submit_button("应用清洗")
    
    if submitted:
        return {
            "numeric_cols": selected_numeric_cols,
            "handle_missing_numeric": handle_missing_numeric,
            "handle_outliers": handle_outliers,
            "text_cols": selected_text_cols,
            "lower_case": lower_case,
            "remove_punctuation": remove_punctuation,
            "remove_numbers": remove_numbers,
            "remove_html": remove_html,
            "remove_extra_spaces": remove_extra_spaces,
            "remove_dupes": remove_dupes
        }
    
    return None

def visualization_form(df):
    """数据可视化表单，返回可视化选项"""
    with st.form(key="visualization_form"):
        st.subheader("数据可视化选项")
        
        # 选择可视化类型
        viz_type = st.selectbox(
            "选择可视化类型",
            options=["bar", "line", "scatter", "histogram", "box", "pie", "heatmap", "time_series"],
            format_func=lambda x: {
                "bar": "条形图",
                "line": "折线图",
                "scatter": "散点图",
                "histogram": "直方图",
                "box": "箱线图",
                "pie": "饼图",
                "heatmap": "热力图",
                "time_series": "时间序列图"
            }.get(x, x)
        )
        
        # 根据可视化类型选择参数
        if viz_type in ["bar", "pie"]:
            x_col = st.selectbox("选择分类列", options=df.columns)
            y_col = st.selectbox("选择值列 (可选)", options=["无"] + df.select_dtypes(include=['number']).columns.tolist())
            y_col = None if y_col == "无" else y_col
            
        elif viz_type in ["line", "time_series"]:
            x_col = st.selectbox("选择X轴列", options=df.columns)
            y_col = st.selectbox("选择Y轴列", options=df.select_dtypes(include=['number']).columns.tolist())
            
        elif viz_type == "scatter":
            x_col = st.selectbox("选择X轴列", options=df.select_dtypes(include=['number']).columns.tolist())
            y_col = st.selectbox("选择Y轴列", options=df.select_dtypes(include=['number']).columns.tolist())
            color_col = st.selectbox("颜色分类列 (可选)", options=["无"] + df.columns.tolist())
            color_col = None if color_col == "无" else color_col
            
        elif viz_type == "histogram":
            x_col = st.selectbox("选择列", options=df.select_dtypes(include=['number']).columns.tolist())
            bins = st.slider("分箱数量", min_value=5, max_value=50, value=20)
            
        elif viz_type == "box":
            y_col = st.selectbox("选择数值列", options=df.select_dtypes(include=['number']).columns.tolist())
            x_col = st.selectbox("选择分组列 (可选)", options=["无"] + df.columns.tolist())
            x_col = None if x_col == "无" else x_col
            
        elif viz_type == "heatmap":
            corr_cols = st.multiselect(
                "选择用于计算相关性的列",
                options=df.select_dtypes(include=['number']).columns.tolist(),
                default=df.select_dtypes(include=['number']).columns.tolist()[:min(5, len(df.select_dtypes(include=['number']).columns))]
            )
            x_col = corr_cols  # 使用corr_cols作为x_col传递
            y_col = None
            
        
        # 通用参数
        title = st.text_input("图表标题", value=f"{viz_type.capitalize()} Chart")
        
        submitted = st.form_submit_button("生成图表")
    
    if submitted:
        params = {
            "viz_type": viz_type,
            "title": title
        }
        
        if viz_type == "bar":
            params.update({"x_col": x_col, "y_col": y_col})
        elif viz_type == "pie":
            params.update({"column": x_col})
        elif viz_type in ["line", "scatter"]:
            params.update({"x_col": x_col, "y_col": y_col})
            if viz_type == "scatter" and "color_col" in locals():
                params.update({"color_col": color_col})
        elif viz_type == "histogram":
            params.update({"column": x_col, "bins": bins})
        elif viz_type == "box":
            params.update({"y_col": y_col, "x_col": x_col})
        elif viz_type == "heatmap":
            params.update({"columns": x_col})
        elif viz_type == "time_series":
            params.update({"date_col": x_col, "value_col": y_col})
        
        return params
    
    return None 