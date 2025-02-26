"""网络爬虫模块，包含基础、高级和动态爬虫技术"""

from .basics import show_basics
from .advanced import show_advanced
from .dynamic import show_dynamic

def show():
    """网络爬虫主页面，提供子模块导航"""
    import streamlit as st
    
    st.header("网络爬虫技术")
    
    # 介绍
    st.markdown("""
    网络爬虫是一种自动从互联网获取数据的技术。通过模拟浏览器行为，爬虫可以访问网页、提取结构化数据，
    并将其保存为便于分析的格式，如CSV、JSON或数据库记录。
    
    在本模块中，我们将学习：
    """)
    
    # 创建页面内导航
    tab1, tab2, tab3 = st.tabs(["基础爬虫", "高级爬虫", "动态爬虫"])
    
    with tab1:
        st.markdown("""
        ### 爬虫基础
        
        * HTTP基础知识
        * 使用Requests发送请求
        * 使用BeautifulSoup解析HTML
        * 提取网页数据
        * 简单爬虫实例
        """)
        
        if st.button("进入基础爬虫", key="btn_basics"):
            st.session_state.scraping_subpage = "basics"
            st.experimental_rerun()
    
    with tab2:
        st.markdown("""
        ### 高级爬虫
        
        * 设置请求头和代理
        * 处理网站反爬机制
        * 会话和Cookie管理
        * 处理表单和登录
        * 高级数据提取技术
        """)
        
        if st.button("进入高级爬虫", key="btn_advanced"):
            st.session_state.scraping_subpage = "advanced"
            st.experimental_rerun()
    
    with tab3:
        st.markdown("""
        ### 动态网页爬虫
        
        * 理解动态网页加载
        * XHR请求和Ajax抓取
        * API接口分析
        * 浏览器自动化技术
        * 渲染网页内容抓取
        """)
        
        if st.button("进入动态爬虫", key="btn_dynamic"):
            st.session_state.scraping_subpage = "dynamic"
            st.experimental_rerun()
    
    # 检查是否需要显示子页面
    if "scraping_subpage" in st.session_state:
        subpage = st.session_state.scraping_subpage
        
        if subpage == "basics":
            show_basics()
        elif subpage == "advanced":
            show_advanced()
        elif subpage == "dynamic":
            show_dynamic()
        
        # 添加返回按钮
        if st.button("返回爬虫主页"):
            st.session_state.pop("scraping_subpage")
            st.experimental_rerun()
    
    # 注意事项
    st.markdown("---")
    st.warning("""
    **合法合规注意事项**：进行网络爬虫时请遵守以下原则：
    
    1. 阅读并遵守网站的robots.txt文件
    2. 合理控制爬取速度，避免对目标服务器造成过大负担
    3. 尊重网站的服务条款和数据使用协议
    4. 获取的数据仅用于分析研究，避免侵犯版权和数据隐私
    """)

if __name__ == "__main__":
    show()
