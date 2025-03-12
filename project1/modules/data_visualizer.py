import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from modules.data_visualizer_sales import create_sales_dashboard
from modules.data_visualizer_customers import create_customer_dashboard
from modules.data_visualizer_products import create_product_dashboard
from modules.data_visualizer_marketing import create_marketing_dashboard
from modules.data_visualizer_channels import create_channel_dashboard

def create_dashboard(data):
    """
    创建交互式数据可视化仪表板
    
    Args:
        data (dict): 包含所有数据集的字典
    """
    # 添加仪表板选项
    dashboard_type = st.radio(
        "选择仪表板类型",
        ["销售概览", "客户分析", "产品分析", "营销效果", "渠道分析"],
        horizontal=True
    )
    
    # 根据选择显示不同的仪表板
    if dashboard_type == "销售概览":
        sales_dashboard(data)
    elif dashboard_type == "客户分析":
        customer_dashboard(data)
    elif dashboard_type == "产品分析":
        product_dashboard(data)
    elif dashboard_type == "营销效果":
        marketing_dashboard(data)
    elif dashboard_type == "渠道分析":
        channel_dashboard(data)

def sales_dashboard(data):
    """销售概览仪表板"""
    st.subheader("销售概览")
    
    # 准备数据
    transactions_df = data["transactions"]
    
    # 确保日期格式正确
    transactions_df['date'] = pd.to_datetime(transactions_df['date'])
    
    # 创建月度销售趋势图
    try:
        # 按日期汇总销售数据
        daily_sales = transactions_df.groupby('date')['total_amount'].sum().reset_index()
        daily_sales['month'] = daily_sales['date'].dt.strftime('%Y-%m')
        
        # 月度销售趋势
        monthly_sales = daily_sales.groupby('month')['total_amount'].sum().reset_index()
        
        fig = px.line(monthly_sales, x='month', y='total_amount', 
                     title='月度销售趋势',
                     labels={'month': '月份', 'total_amount': '销售额'})
        
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"创建销售趋势图时出错: {str(e)}")
    
    # 添加关键指标卡片
    try:
        st.subheader("销售关键指标")
        
        # 计算关键指标
        total_sales = transactions_df['total_amount'].sum()
        avg_order_value = transactions_df.groupby('transaction_id')['total_amount'].sum().mean()
        total_orders = transactions_df['transaction_id'].nunique()
        
        # 显示指标卡片
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("总销售额", f"¥{total_sales:,.2f}")
        with col2:
            st.metric("平均订单金额", f"¥{avg_order_value:,.2f}")
        with col3:
            st.metric("订单总数", f"{total_orders:,}")
    except Exception as e:
        st.error(f"显示销售指标时出错: {str(e)}")

def customer_dashboard(data):
    """客户分析仪表板"""
    st.subheader("客户分析")
    
    # 准备数据
    customers_df = data["customers"]
    
    try:
        # 创建客户区域分布图
        if 'region' in customers_df.columns:
            region_counts = customers_df['region'].value_counts().reset_index()
            region_counts.columns = ['region', 'count']
            
            fig = px.pie(region_counts, values='count', names='region',
                        title='客户区域分布')
            
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"创建客户区域分布图时出错: {str(e)}")
    
    try:
        # 创建客户年龄分布图
        if 'age' in customers_df.columns:
            fig = px.histogram(customers_df, x='age', nbins=20,
                              title='客户年龄分布',
                              labels={'age': '年龄', 'count': '客户数量'})
            
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"创建客户年龄分布图时出错: {str(e)}")

def product_dashboard(data):
    """产品分析仪表板"""
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

def marketing_dashboard(data):
    """营销效果仪表板"""
    st.subheader("营销效果分析")
    
    # 准备数据
    marketing_df = data["marketing"]
    
    try:
        # 创建渠道分布图
        if 'channel' in marketing_df.columns:
            channel_counts = marketing_df['channel'].value_counts().reset_index()
            channel_counts.columns = ['channel', 'count']
            
            fig = px.pie(channel_counts, values='count', names='channel',
                        title='营销渠道分布')
            
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"创建营销渠道分布图时出错: {str(e)}")
    
    try:
        # 创建支出和转化图
        if all(col in marketing_df.columns for col in ['spend', 'conversions', 'channel']):
            channel_metrics = marketing_df.groupby('channel').agg({
                'spend': 'sum',
                'conversions': 'sum'
            }).reset_index()
            
            fig = px.bar(channel_metrics, x='channel', y=['spend', 'conversions'],
                        title='各渠道支出和转化',
                        barmode='group',
                        labels={'channel': '渠道', 'value': '数值', 'variable': '指标'})
            
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"创建营销支出和转化图时出错: {str(e)}")

def channel_dashboard(data):
    """渠道分析仪表板"""
    st.subheader("渠道分析")
    
    # 准备数据
    traffic_df = data["traffic"]
    
    try:
        # 创建渠道流量分布图
        channels = ['organic_search', 'paid_search', 'social_media', 'email', 'direct', 'referral']
        valid_channels = [channel for channel in channels if channel in traffic_df.columns]
        
        if valid_channels:
            channel_traffic = traffic_df[valid_channels].sum().reset_index()
            channel_traffic.columns = ['channel', 'visits']
            
            fig = px.pie(channel_traffic, values='visits', names='channel',
                        title='渠道流量分布')
            
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"创建渠道流量分布图时出错: {str(e)}")
    
    try:
        # 创建转化率分析图
        if 'conversion_rate' in traffic_df.columns and 'date' in traffic_df.columns:
            traffic_df['date'] = pd.to_datetime(traffic_df['date'])
            traffic_df['month'] = traffic_df['date'].dt.strftime('%Y-%m')
            
            monthly_conversion = traffic_df.groupby('month')['conversion_rate'].mean().reset_index()
            
            fig = px.line(monthly_conversion, x='month', y='conversion_rate',
                         title='月度平均转化率趋势',
                         labels={'month': '月份', 'conversion_rate': '转化率'})
            
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"创建转化率分析图时出错: {str(e)}") 