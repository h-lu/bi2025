import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_channel_dashboard(data):
    """创建渠道分析仪表板"""
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
    
    try:
        # 创建不同渠道的跳出率比较
        if 'bounce_rate' in traffic_df.columns and any(channel in traffic_df.columns for channel in channels):
            # 计算每个渠道的平均跳出率
            bounce_rates = []
            
            for channel in valid_channels:
                # 使用加权平均来计算每个渠道的跳出率
                if channel in traffic_df.columns:
                    weighted_sum = (traffic_df[channel] * traffic_df['bounce_rate']).sum()
                    total_visits = traffic_df[channel].sum()
                    
                    if total_visits > 0:
                        bounce_rates.append({
                            'channel': channel,
                            'bounce_rate': weighted_sum / total_visits
                        })
            
            if bounce_rates:
                bounce_df = pd.DataFrame(bounce_rates)
                
                fig = px.bar(bounce_df, x='channel', y='bounce_rate',
                            title='各渠道跳出率比较',
                            labels={'channel': '渠道', 'bounce_rate': '跳出率'})
                
                st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"创建渠道跳出率比较图时出错: {str(e)}")
    
    try:
        # 创建渠道趋势图
        if 'date' in traffic_df.columns and valid_channels:
            traffic_df['date'] = pd.to_datetime(traffic_df['date'])
            traffic_df['month'] = traffic_df['date'].dt.strftime('%Y-%m')
            
            monthly_traffic = traffic_df.groupby('month')[valid_channels].sum().reset_index()
            
            fig = px.line(monthly_traffic, x='month', y=valid_channels,
                         title='月度渠道流量趋势',
                         labels={'month': '月份', 'value': '访问量', 'variable': '渠道'})
            
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"创建渠道趋势图时出错: {str(e)}")
    
    return None 