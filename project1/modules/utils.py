import streamlit as st
import pandas as pd
import os
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 检查数据是否已生成
def check_data_generated():
    """检查所需的数据文件是否已存在"""
    # 获取当前脚本的绝对路径
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    required_files = [
        os.path.join(current_dir, "data", "customers.csv"),
        os.path.join(current_dir, "data", "products.csv"),
        os.path.join(current_dir, "data", "transactions.csv"),
        os.path.join(current_dir, "data", "marketing_campaigns.csv"),
        os.path.join(current_dir, "data", "website_traffic.csv")
    ]
    
    return all(os.path.exists(file) for file in required_files)

# 显示数据集信息
def display_dataset_info(df, dataset_name):
    """显示数据集的基本信息"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("行数", df.shape[0])
    
    with col2:
        st.metric("列数", df.shape[1])
    
    with col3:
        st.metric("缺失值比例", f"{(df.isnull().sum().sum() / (df.shape[0] * df.shape[1]) * 100):.2f}%")
    
    # 根据数据集类型显示特定信息
    if dataset_name == "客户数据":
        display_customer_overview(df)
    elif dataset_name == "产品数据":
        display_product_overview(df)
    elif dataset_name == "交易数据":
        display_transaction_overview(df)
    elif dataset_name == "营销活动数据":
        display_marketing_overview(df)
    elif dataset_name == "网站流量数据":
        display_traffic_overview(df)

def display_customer_overview(df):
    """显示客户数据的概览"""
    col1, col2 = st.columns(2)
    
    with col1:
        # 区域分布图
        if 'region' in df.columns:
            fig = px.pie(df, names='region', title='客户地区分布')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 客户细分图
        if 'segment' in df.columns:
            # 修复列名问题：value_counts().reset_index()后，列名为'segment'和'count'
            segment_counts = df['segment'].value_counts().reset_index()
            segment_counts.columns = ['segment', 'count']  # 明确重命名列
            
            fig = px.bar(segment_counts, 
                         x='segment', y='count', 
                         labels={'segment': '客户细分', 'count': '数量'},
                         title='客户细分分布')
            st.plotly_chart(fig, use_container_width=True)

def display_product_overview(df):
    """显示产品数据的概览"""
    col1, col2 = st.columns(2)
    
    with col1:
        # 产品类别分布
        if 'category' in df.columns:
            # 修复列名问题
            category_counts = df['category'].value_counts().reset_index()
            category_counts.columns = ['category', 'count']  # 明确重命名列
            
            fig = px.bar(category_counts, 
                         x='category', y='count', 
                         labels={'category': '产品类别', 'count': '数量'},
                         title='产品类别分布')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 价格分布
        if 'current_price' in df.columns:
            fig = px.histogram(df, x='current_price', nbins=20,
                              title='产品价格分布')
            st.plotly_chart(fig, use_container_width=True)

def display_transaction_overview(df):
    """显示交易数据的概览"""
    col1, col2 = st.columns(2)
    
    with col1:
        # 交易状态分布
        if 'status' in df.columns:
            fig = px.pie(df, names='status', title='交易状态分布')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 支付方式分布
        if 'payment_method' in df.columns:
            # 修复列名问题：value_counts().reset_index()后，列名为'payment_method'和'count'
            payment_counts = df['payment_method'].value_counts().reset_index()
            payment_counts.columns = ['payment_method', 'count']  # 明确重命名列
            
            fig = px.bar(payment_counts, 
                         x='payment_method', y='count', 
                         labels={'payment_method': '支付方式', 'count': '数量'},
                         title='支付方式分布')
            st.plotly_chart(fig, use_container_width=True)

def display_marketing_overview(df):
    """显示营销活动数据的概览"""
    col1, col2 = st.columns(2)
    
    with col1:
        # 营销渠道分布
        if 'channel' in df.columns:
            fig = px.pie(df, names='channel', title='营销渠道分布')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # 营销目标分布
        if 'objective' in df.columns:
            # 修复列名问题
            objective_counts = df['objective'].value_counts().reset_index()
            objective_counts.columns = ['objective', 'count']  # 明确重命名列
            
            fig = px.bar(objective_counts, 
                         x='objective', y='count', 
                         labels={'objective': '营销目标', 'count': '数量'},
                         title='营销目标分布')
            st.plotly_chart(fig, use_container_width=True)

def display_traffic_overview(df):
    """显示网站流量数据的概览"""
    if 'date' in df.columns and 'total_visits' in df.columns:
        # 转换日期列为日期类型
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.strftime('%Y-%m')
        
        # 按月聚合流量
        monthly_traffic = df.groupby('month')['total_visits'].sum().reset_index()
        
        # 绘制流量趋势图
        fig = px.line(monthly_traffic, x='month', y='total_visits',
                     labels={'month': '月份', 'total_visits': '总访问量'},
                     title='月度网站流量趋势')
        st.plotly_chart(fig, use_container_width=True)

# 创建可视化辅助函数
def create_timeseries(df, x, y, title):
    """创建时间序列图表"""
    fig = px.line(df, x=x, y=y, title=title)
    fig.update_layout(xaxis_title=x, yaxis_title=y)
    return fig

def create_bar_chart(df, x, y, title):
    """创建条形图"""
    fig = px.bar(df, x=x, y=y, title=title)
    fig.update_layout(xaxis_title=x, yaxis_title=y)
    return fig

def create_pie_chart(df, names, title):
    """创建饼图"""
    fig = px.pie(df, names=names, title=title)
    return fig

def create_scatter_plot(df, x, y, color=None, size=None, title=None):
    """创建散点图"""
    fig = px.scatter(df, x=x, y=y, color=color, size=size, title=title)
    fig.update_layout(xaxis_title=x, yaxis_title=y)
    return fig

def create_heatmap(df, x, y, z, title=None):
    """创建热力图"""
    fig = px.density_heatmap(df, x=x, y=y, z=z, title=title)
    fig.update_layout(xaxis_title=x, yaxis_title=y)
    return fig 