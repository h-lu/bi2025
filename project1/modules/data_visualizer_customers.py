import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def create_customer_dashboard(data):
    """客户分析仪表板"""
    st.subheader("客户分析")
    
    # 准备数据
    customers_df = data["customers"]
    transactions_df = data["transactions"]
    
    # 合并交易数据和客户数据
    customer_transactions = transactions_df.merge(
        customers_df[['customer_id', 'region', 'country', 'segment']], 
        on='customer_id', 
        how='left'
    )
    
    # 计算每个客户的消费金额
    customer_spending = customer_transactions.groupby('customer_id')['total_amount'].sum().reset_index()
    customer_spending = customer_spending.merge(
        customers_df[['customer_id', 'segment', 'region', 'age', 'gender', 'income']], 
        on='customer_id', 
        how='left'
    )
    
    # 计算区域消费分布
    region_spending = customer_transactions.groupby('region')['total_amount'].sum().reset_index()
    
    # 计算客户细分消费分布
    segment_spending = customer_transactions.groupby('segment')['total_amount'].sum().reset_index()
    
    # 图表1: 按区域的消费分布
    fig1 = px.pie(region_spending, values='total_amount', names='region',
                 title='按区域的消费分布')
    
    # 图表2: 按客户细分的消费分布
    fig2 = px.bar(segment_spending, x='segment', y='total_amount',
                 title='按客户细分的消费分布',
                 labels={'segment': '客户细分', 'total_amount': '消费金额'})
    
    # 布局
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.plotly_chart(fig2, use_container_width=True)
    
    # 图表3: 消费金额与年龄的关系
    fig3 = px.scatter(customer_spending, x='age', y='total_amount', color='gender',
                     title='消费金额与年龄的关系',
                     labels={'age': '年龄', 'total_amount': '消费金额', 'gender': '性别'})
    
    # 图表4: 消费金额与收入的关系
    fig4 = px.scatter(customer_spending, x='income', y='total_amount', color='segment',
                     title='消费金额与收入的关系',
                     labels={'income': '收入', 'total_amount': '消费金额', 'segment': '客户细分'})
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        st.plotly_chart(fig4, use_container_width=True)
    
    # 添加客户互动部分
    st.subheader("客户消费分布")
    
    # 计算每个客户的消费金额
    customer_order_counts = customer_transactions.groupby('customer_id')['transaction_id'].nunique().reset_index()
    customer_order_counts.columns = ['customer_id', 'order_count']
    
    # 合并消费金额和订单数量
    customer_metrics = customer_spending.merge(customer_order_counts, on='customer_id', how='left')
    
    # 添加平均订单金额
    customer_metrics['avg_order_value'] = customer_metrics['total_amount'] / customer_metrics['order_count']
    
    # 顶部和底部客户
    top_customers = customer_metrics.sort_values('total_amount', ascending=False).head(10)
    bottom_customers = customer_metrics.sort_values('total_amount').head(10)
    
    st.subheader("消费最高的10位客户")
    st.dataframe(top_customers[['customer_id', 'total_amount', 'order_count', 'avg_order_value', 'segment']])
    
    st.subheader("消费最低的10位客户")
    st.dataframe(bottom_customers[['customer_id', 'total_amount', 'order_count', 'avg_order_value', 'segment']])
    
    # RFM分析图
    st.subheader("客户RFM分析")
    
    # 准备RFM数据
    # R (Recency): 最近一次购买的时间
    # F (Frequency): 购买频率
    # M (Monetary): 消费金额
    
    # 计算最近一次购买时间
    transactions_df['date'] = pd.to_datetime(transactions_df['date'])
    latest_purchase = transactions_df.groupby('customer_id')['date'].max().reset_index()
    latest_purchase.columns = ['customer_id', 'latest_purchase']
    latest_purchase['recency'] = (pd.to_datetime('today') - latest_purchase['latest_purchase']).dt.days
    
    # 合并RFM数据
    rfm_data = customer_metrics.merge(latest_purchase[['customer_id', 'recency']], on='customer_id', how='left')
    
    # 创建RFM散点图
    fig5 = px.scatter_3d(rfm_data, x='recency', y='order_count', z='total_amount',
                        color='segment', size='total_amount',
                        title='RFM客户分析',
                        labels={'recency': '最近购买天数', 'order_count': '购买频率', 'total_amount': '消费金额'},
                        opacity=0.7)
    
    st.plotly_chart(fig5, use_container_width=True) 