import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_sales_dashboard(data):
    """销售概览仪表板"""
    st.subheader("销售概览")
    
    # 准备数据
    transactions_df = data["transactions"]
    
    # 确保日期格式正确
    transactions_df['date'] = pd.to_datetime(transactions_df['date'])
    
    # 按日期汇总销售数据
    daily_sales = transactions_df.groupby('date')['total_amount'].sum().reset_index()
    daily_sales['month'] = daily_sales['date'].dt.strftime('%Y-%m')
    
    # 月度销售趋势
    monthly_sales = daily_sales.groupby('month')['total_amount'].sum().reset_index()
    
    # 创建时间序列图表
    fig1 = px.line(monthly_sales, x='month', y='total_amount', 
                  title='月度销售趋势',
                  labels={'month': '月份', 'total_amount': '销售额'})
    
    # 创建按支付方式的销售额饼图
    payment_sales = transactions_df.groupby('payment_method')['total_amount'].sum().reset_index()
    fig2 = px.pie(payment_sales, values='total_amount', names='payment_method', 
                 title='按支付方式的销售额分布')
    
    # 创建按设备类型的销售额柱状图
    device_sales = transactions_df.groupby('device')['total_amount'].sum().reset_index()
    fig3 = px.bar(device_sales, x='device', y='total_amount', 
                 title='按设备类型的销售额',
                 labels={'device': '设备类型', 'total_amount': '销售额'})
    
    # 创建按产品类别的销售额柱状图
    category_sales = transactions_df.groupby('product_category')['total_amount'].sum().reset_index()
    fig4 = px.bar(category_sales, x='product_category', y='total_amount', 
                 title='按产品类别的销售额',
                 labels={'product_category': '产品类别', 'total_amount': '销售额'})
    
    # 布局
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        st.plotly_chart(fig2, use_container_width=True)
        st.plotly_chart(fig4, use_container_width=True)
    
    # 添加关键指标卡片
    st.subheader("销售关键指标")
    
    # 计算关键指标
    total_sales = transactions_df['total_amount'].sum()
    avg_order_value = transactions_df.groupby('transaction_id')['total_amount'].sum().mean()
    total_orders = transactions_df['transaction_id'].nunique()
    completed_orders = transactions_df[transactions_df['status'] == 'Completed']['transaction_id'].nunique()
    completion_rate = completed_orders / total_orders if total_orders > 0 else 0
    
    # 显示指标卡片
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("总销售额", f"¥{total_sales:,.2f}")
    with col2:
        st.metric("平均订单金额", f"¥{avg_order_value:,.2f}")
    with col3:
        st.metric("订单总数", f"{total_orders:,}")
    with col4:
        st.metric("订单完成率", f"{completion_rate:.1%}")
    
    # 增加交互式日期筛选器
    st.subheader("按日期范围筛选销售数据")
    
    # 计算日期范围
    min_date = transactions_df['date'].min()
    max_date = transactions_df['date'].max()
    
    # 创建日期选择器
    date_range = st.date_input(
        "选择日期范围",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        
        # 筛选数据
        filtered_transactions = transactions_df[(transactions_df['date'] >= start_date) & 
                                               (transactions_df['date'] <= end_date)]
        
        # 计算筛选后的销售数据
        filtered_daily_sales = filtered_transactions.groupby('date')['total_amount'].sum().reset_index()
        
        # 显示筛选后的销售趋势
        fig5 = px.line(filtered_daily_sales, x='date', y='total_amount',
                      title=f'从 {start_date.strftime("%Y-%m-%d")} 到 {end_date.strftime("%Y-%m-%d")} 的日销售额',
                      labels={'date': '日期', 'total_amount': '销售额'})
        st.plotly_chart(fig5, use_container_width=True)
        
        # 显示筛选后的关键指标
        filtered_total_sales = filtered_transactions['total_amount'].sum()
        filtered_avg_order_value = filtered_transactions.groupby('transaction_id')['total_amount'].sum().mean()
        filtered_total_orders = filtered_transactions['transaction_id'].nunique()
        
        st.subheader("所选日期范围的关键指标")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("筛选后总销售额", f"¥{filtered_total_sales:,.2f}")
        with col2:
            st.metric("筛选后平均订单金额", f"¥{filtered_avg_order_value:,.2f}")
        with col3:
            st.metric("筛选后订单总数", f"{filtered_total_orders:,}") 