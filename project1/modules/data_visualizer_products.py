import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_product_dashboard(data):
    """创建产品分析仪表板"""
    st.subheader("产品分析")
    
    # 准备数据
    products_df = data["products"]
    
    try:
        # 创建产品类别分布图
        if 'category' in products_df.columns:
            category_counts = products_df['category'].value_counts().reset_index()
            category_counts.columns = ['category', 'count']
            
            fig = px.bar(category_counts, x='category', y='count',
                        title='产品类别分布',
                        labels={'category': '类别', 'count': '产品数量'})
            
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"创建产品类别分布图时出错: {str(e)}")
    
    try:
        # 创建产品价格分布图
        if 'current_price' in products_df.columns:
            fig = px.histogram(products_df, x='current_price', nbins=20,
                              title='产品价格分布',
                              labels={'current_price': '价格', 'count': '产品数量'})
            
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"创建产品价格分布图时出错: {str(e)}")
    
    try:
        # 产品库存分析
        if 'inventory' in products_df.columns:
            fig = px.histogram(products_df, x='inventory', nbins=20,
                             title='产品库存分布',
                             labels={'inventory': '库存量', 'count': '产品数量'})
            
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"创建产品库存分布图时出错: {str(e)}")
    
    try:
        # 产品评分分析
        if 'rating' in products_df.columns:
            fig = px.box(products_df, x='category', y='rating',
                       title='各类别产品评分分布',
                       labels={'category': '类别', 'rating': '评分'})
            
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"创建产品评分分析图时出错: {str(e)}")
    
    return None 