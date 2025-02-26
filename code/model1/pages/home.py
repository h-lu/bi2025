import streamlit as st
from components.text_displays import show_info_card

def show():
    """显示首页内容"""
    st.header("商业智能数据采集与预处理")
    
    st.markdown("""
    欢迎使用商业智能数据采集与预处理应用，本应用旨在演示和教授数据采集、清洗和分析的基本技术。
    
    通过本应用，您可以了解：
    
    * 常见的数据源和获取方法
    * 网络爬虫的基本原理和实现
    * 数据清洗和转换技术
    * 文本处理和分析方法
    * 数据可视化技术
    
    请使用左侧边栏导航到各个功能模块。
    """)
    
    # 展示应用结构
    st.subheader("应用结构")
    
    col1, col2 = st.columns(2)
    
    with col1:
        show_info_card(
            "数据源与获取", 
            """
            * 各类数据源介绍
            * API数据获取
            * 文件数据导入
            * 数据格式概述
            """,
            icon="📊",
            is_expanded=True
        )
        
        show_info_card(
            "网络爬虫技术", 
            """
            * 爬虫基础知识
            * 静态网页抓取
            * 高级爬虫技术
            * 动态网页抓取
            """,
            icon="🕸️",
            is_expanded=True
        )
    
    with col2:
        show_info_card(
            "数据清洗与转换", 
            """
            * 数据质量评估
            * 缺失值处理
            * 异常值检测
            * 数据类型转换
            * 特征工程基础
            """,
            icon="🧹",
            is_expanded=True
        )
        
        show_info_card(
            "文本处理与分析", 
            """
            * 文本预处理技术
            * 分词与词频分析
            * 情感分析
            * 关键词提取
            * 文本分类
            """,
            icon="📝",
            is_expanded=True
        )
    
    # 数据流程图
    st.subheader("数据处理流程")
    
    st.markdown("""
    ```mermaid
    graph LR
        A[数据源] --> B[数据获取]
        B --> C[数据清洗]
        C --> D[数据转换]
        D --> E[特征工程]
        E --> F[数据分析与可视化]
        F --> G[结果解释]
    ```
    """)
    
    # 技术栈介绍
    st.subheader("技术栈")
    
    tech_col1, tech_col2, tech_col3 = st.columns(3)
    
    with tech_col1:
        st.markdown("**数据获取**")
        st.markdown("""
        * Requests
        * BeautifulSoup
        * Pandas
        * API接口
        """)
    
    with tech_col2:
        st.markdown("**数据处理**")
        st.markdown("""
        * Pandas
        * NumPy
        * Scikit-learn
        * NLTK/jieba
        """)
    
    with tech_col3:
        st.markdown("**数据可视化**")
        st.markdown("""
        * Matplotlib
        * Seaborn
        * Streamlit
        * Plotly
        """)
    
    # 版权信息
    st.markdown("---")
    st.markdown("© 2023 商业智能数据采集与预处理 | 版本 1.0")
    st.caption("本应用仅用于教育目的，所有示例数据均为模拟数据。")

if __name__ == "__main__":
    show() 