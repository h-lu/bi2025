import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_marketing_dashboard(data):
    """创建营销效果仪表板"""
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
    
    try:
        # 计算ROI
        if all(col in marketing_df.columns for col in ['spend', 'revenue', 'channel']):
            roi_df = marketing_df.groupby('channel').agg({
                'spend': 'sum',
                'revenue': 'sum'
            }).reset_index()
            
            roi_df['roi'] = (roi_df['revenue'] - roi_df['spend']) / roi_df['spend']
            
            fig = px.bar(roi_df, x='channel', y='roi',
                        title='各渠道营销ROI',
                        labels={'channel': '渠道', 'roi': 'ROI'})
            
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"创建营销ROI图时出错: {str(e)}")
    
    try:
        # 时间趋势分析
        if all(col in marketing_df.columns for col in ['date', 'spend', 'conversions']):
            time_trend = marketing_df.groupby('date').agg({
                'spend': 'sum',
                'conversions': 'sum'
            }).reset_index()
            
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig.add_trace(
                go.Scatter(x=time_trend['date'], y=time_trend['spend'], name="支出"),
                secondary_y=False,
            )
            
            fig.add_trace(
                go.Scatter(x=time_trend['date'], y=time_trend['conversions'], name="转化"),
                secondary_y=True,
            )
            
            fig.update_layout(title_text="营销支出和转化趋势")
            fig.update_xaxes(title_text="日期")
            fig.update_yaxes(title_text="支出", secondary_y=False)
            fig.update_yaxes(title_text="转化", secondary_y=True)
            
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"创建营销趋势图时出错: {str(e)}")
    
    return None 