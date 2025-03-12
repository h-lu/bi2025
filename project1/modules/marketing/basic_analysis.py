import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def perform_basic_analysis(data):
    """
    执行基础营销指标分析
    
    Args:
        data (dict): 包含所有数据集的字典
    """
    st.subheader("营销基础指标分析")
    
    # 准备数据
    marketing_df = data["marketing"]
    transactions_df = data["transactions"]
    traffic_df = data["traffic"]
    
    # 确保日期格式正确
    marketing_df['start_date'] = pd.to_datetime(marketing_df['start_date'])
    marketing_df['end_date'] = pd.to_datetime(marketing_df['end_date'])
    
    # 展示营销活动概览
    st.write("### 营销活动概览")
    
    # 显示所有营销活动
    st.write("全部营销活动列表：")
    
    # 格式化活动数据用于展示
    display_columns = ['campaign_id', 'name', 'channel', 'start_date', 'end_date', 
                      'budget', 'spend', 'impressions', 'clicks', 'conversions', 
                      'target_region', 'target_category', 'objective']
    
    # 格式化日期列
    formatted_campaigns = marketing_df[display_columns].copy()
    formatted_campaigns['start_date'] = formatted_campaigns['start_date'].dt.strftime('%Y-%m-%d')
    formatted_campaigns['end_date'] = formatted_campaigns['end_date'].dt.strftime('%Y-%m-%d')
    
    # 显示活动列表
    st.dataframe(formatted_campaigns, use_container_width=True)
    
    # 计算基础指标
    total_campaigns = marketing_df.shape[0]
    total_budget = marketing_df['budget'].sum()
    total_spend = marketing_df['spend'].sum()
    budget_utilization = (total_spend / total_budget) * 100 if total_budget > 0 else 0
    
    total_impressions = marketing_df['impressions'].sum()
    total_clicks = marketing_df['clicks'].sum()
    total_conversions = marketing_df['conversions'].sum()
    
    avg_ctr = (total_clicks / total_impressions) * 100 if total_impressions > 0 else 0
    avg_conversion_rate = (total_conversions / total_clicks) * 100 if total_clicks > 0 else 0
    avg_cpa = total_spend / total_conversions if total_conversions > 0 else 0
    
    # 显示关键指标
    st.write("### 关键营销指标")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("营销活动总数", f"{total_campaigns}")
        st.metric("总预算", f"¥{total_budget:,.2f}")
    
    with col2:
        st.metric("总支出", f"¥{total_spend:,.2f}")
        st.metric("预算使用率", f"{budget_utilization:.1f}%")
    
    with col3:
        st.metric("总展示次数", f"{total_impressions:,}")
        st.metric("平均点击率(CTR)", f"{avg_ctr:.2f}%")
    
    with col4:
        st.metric("总转化次数", f"{total_conversions:,}")
        st.metric("平均转化率", f"{avg_conversion_rate:.2f}%")
    
    # 投放目标分析
    st.write("### 营销目标分析")
    
    # 按目标汇总活动
    objective_summary = marketing_df.groupby('objective').agg({
        'campaign_id': 'count',
        'budget': 'sum',
        'spend': 'sum',
        'conversions': 'sum'
    }).reset_index()
    
    objective_summary.columns = ['营销目标', '活动数量', '总预算', '总支出', '总转化']
    
    # 计算每个目标的转化成本
    objective_summary['转化成本(CPA)'] = objective_summary['总支出'] / objective_summary['总转化']
    
    # 显示按目标汇总的数据
    st.dataframe(objective_summary, use_container_width=True)
    
    # 可视化营销目标分布
    fig1 = px.pie(
        objective_summary, 
        values='活动数量', 
        names='营销目标',
        title='营销活动目标分布'
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # 目标区域分析
    st.write("### 目标区域分析")
    
    # 按区域汇总活动
    region_summary = marketing_df.groupby('target_region').agg({
        'campaign_id': 'count',
        'budget': 'sum',
        'spend': 'sum',
        'conversions': 'sum'
    }).reset_index()
    
    region_summary.columns = ['目标区域', '活动数量', '总预算', '总支出', '总转化']
    
    # 计算每个区域的转化成本
    region_summary['转化成本(CPA)'] = region_summary['总支出'] / region_summary['总转化']
    
    # 区域投放占比
    fig2 = px.bar(
        region_summary,
        x='目标区域',
        y='总支出',
        color='活动数量',
        title='各区域营销投放情况',
        labels={'总支出': '营销支出', '活动数量': '活动数量'},
        color_continuous_scale=px.colors.sequential.Viridis
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # 目标产品类别分析
    st.write("### 目标产品类别分析")
    
    # 按产品类别汇总活动
    category_summary = marketing_df.groupby('target_category').agg({
        'campaign_id': 'count',
        'budget': 'sum',
        'spend': 'sum',
        'conversions': 'sum'
    }).reset_index()
    
    category_summary.columns = ['目标类别', '活动数量', '总预算', '总支出', '总转化']
    
    # 计算每个类别的转化成本
    category_summary['转化成本(CPA)'] = category_summary['总支出'] / category_summary['总转化']
    
    # 产品类别投放占比
    fig3 = px.bar(
        category_summary,
        x='目标类别',
        y=['总预算', '总支出'],
        title='各产品类别营销投放情况',
        barmode='group',
        labels={'value': '金额', 'variable': '类型'}
    )
    st.plotly_chart(fig3, use_container_width=True)
    
    # 营销活动时间线
    st.write("### 营销活动时间线")
    
    # 按月汇总活动数量
    marketing_df['month_start'] = marketing_df['start_date'].dt.strftime('%Y-%m')
    monthly_campaigns = marketing_df.groupby('month_start').size().reset_index()
    monthly_campaigns.columns = ['月份', '活动数量']
    
    # 按月汇总营销支出
    monthly_spend = marketing_df.groupby('month_start')['spend'].sum().reset_index()
    monthly_spend.columns = ['月份', '总支出']
    
    # 合并月度数据
    monthly_data = monthly_campaigns.merge(monthly_spend, on='月份')
    
    # 创建双Y轴图表
    fig4 = make_subplots(specs=[[{"secondary_y": True}]])
    
    # 添加活动数量线
    fig4.add_trace(
        go.Scatter(x=monthly_data['月份'], y=monthly_data['活动数量'], name="活动数量"),
        secondary_y=False,
    )
    
    # 添加支出柱状图
    fig4.add_trace(
        go.Bar(x=monthly_data['月份'], y=monthly_data['总支出'], name="总支出"),
        secondary_y=True,
    )
    
    # 更新布局
    fig4.update_layout(
        title_text="月度营销活动数量和支出",
        xaxis_title="月份",
    )
    
    # 更新y轴标题
    fig4.update_yaxes(title_text="活动数量", secondary_y=False)
    fig4.update_yaxes(title_text="总支出", secondary_y=True)
    
    st.plotly_chart(fig4, use_container_width=True)
    
    # 选择特定活动进行详细分析
    st.write("### 单个活动详细分析")
    
    # 选择活动
    selected_campaign = st.selectbox(
        "选择要分析的营销活动",
        options=marketing_df['name'].unique()
    )
    
    # 获取选定活动的详情
    campaign_data = marketing_df[marketing_df['name'] == selected_campaign].iloc[0]
    
    # 显示活动详情
    st.write(f"#### {selected_campaign} 活动详情")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**活动ID**: {campaign_data['campaign_id']}")
        st.write(f"**渠道**: {campaign_data['channel']}")
        st.write(f"**开始日期**: {campaign_data['start_date'].strftime('%Y-%m-%d')}")
        st.write(f"**结束日期**: {campaign_data['end_date'].strftime('%Y-%m-%d')}")
        st.write(f"**预算**: ¥{campaign_data['budget']:,.2f}")
        st.write(f"**支出**: ¥{campaign_data['spend']:,.2f}")
    
    with col2:
        st.write(f"**目标区域**: {campaign_data['target_region']}")
        st.write(f"**目标类别**: {campaign_data['target_category']}")
        st.write(f"**目标受众**: {campaign_data['target_audience']}")
        st.write(f"**营销目标**: {campaign_data['objective']}")
        st.write(f"**展示次数**: {campaign_data['impressions']:,}")
        st.write(f"**点击次数**: {campaign_data['clicks']:,}")
    
    # 计算活动效果指标
    ctr = campaign_data['clicks'] / campaign_data['impressions'] * 100 if campaign_data['impressions'] > 0 else 0
    conversion_rate = campaign_data['conversions'] / campaign_data['clicks'] * 100 if campaign_data['clicks'] > 0 else 0
    cpa = campaign_data['spend'] / campaign_data['conversions'] if campaign_data['conversions'] > 0 else 0
    
    # 显示活动效果指标
    st.write("#### 活动效果指标")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("点击率(CTR)", f"{ctr:.2f}%")
    
    with col2:
        st.metric("转化率", f"{conversion_rate:.2f}%")
    
    with col3:
        st.metric("每次获客成本(CPA)", f"¥{cpa:.2f}")
    
    with col4:
        # 计算并显示ROI
        if isinstance(campaign_data['roi'], (int, float)) and not pd.isna(campaign_data['roi']):
            roi_value = campaign_data['roi'] * 100 if campaign_data['roi'] < 1 else campaign_data['roi']
            st.metric("投资回报率(ROI)", f"{roi_value:.2f}%")
        else:
            st.metric("投资回报率(ROI)", "N/A")
    
    # 分析活动期间的销售和流量趋势
    st.write("#### 活动期间的销售和流量趋势")
    
    # 获取活动前后的销售数据
    pre_campaign_start = campaign_data['start_date'] - pd.Timedelta(days=7)
    post_campaign_end = campaign_data['end_date'] + pd.Timedelta(days=7)
    
    # 确保交易和流量数据日期格式一致
    transactions_df['date'] = pd.to_datetime(transactions_df['date'])
    
    if 'date' in traffic_df.columns:
        traffic_df['date'] = pd.to_datetime(traffic_df['date'])
        
        # 筛选时间范围内的交易和流量数据
        period_transactions = transactions_df[(transactions_df['date'] >= pre_campaign_start) & 
                                            (transactions_df['date'] <= post_campaign_end)]
        period_traffic = traffic_df[(traffic_df['date'] >= pre_campaign_start) & 
                                (traffic_df['date'] <= post_campaign_end)]
        
        # 按日期汇总数据
        daily_sales = period_transactions.groupby('date')['total_amount'].sum().reset_index()
        daily_traffic = period_traffic[['date', 'total_visits']].copy()
        
        # 合并销售和流量数据
        daily_metrics = pd.merge(daily_sales, daily_traffic, on='date', how='outer').fillna(0)
        
        # 添加标记活动期间的列
        daily_metrics['is_campaign_period'] = (daily_metrics['date'] >= campaign_data['start_date']) & (daily_metrics['date'] <= campaign_data['end_date'])
        
        # 创建图表
        fig5 = make_subplots(specs=[[{"secondary_y": True}]])
        
        # 添加销售数据
        fig5.add_trace(
            go.Scatter(x=daily_metrics['date'], y=daily_metrics['total_amount'], name="销售额"),
            secondary_y=False,
        )
        
        # 添加流量数据
        fig5.add_trace(
            go.Scatter(x=daily_metrics['date'], y=daily_metrics['total_visits'], name="网站访问量"),
            secondary_y=True,
        )
        
        # 添加活动期间的阴影区域
        fig5.add_vrect(
            x0=campaign_data['start_date'],
            x1=campaign_data['end_date'],
            fillcolor="LightSalmon",
            opacity=0.5,
            layer="below",
            line_width=0,
            annotation_text="活动期间",
            annotation_position="top left"
        )
        
        # 更新布局
        fig5.update_layout(
            title=f"营销活动 '{selected_campaign}' 前后的销售和流量趋势",
            xaxis_title="日期",
            hovermode="x unified"
        )
        
        # 更新y轴标题
        fig5.update_yaxes(title_text="销售额", secondary_y=False)
        fig5.update_yaxes(title_text="网站访问量", secondary_y=True)
        
        st.plotly_chart(fig5, use_container_width=True)
        
        # 计算活动期间和非活动期间的平均值
        campaign_period = daily_metrics[daily_metrics['is_campaign_period']]
        non_campaign_period = daily_metrics[~daily_metrics['is_campaign_period']]
        
        # 计算平均值
        avg_sales_during_campaign = campaign_period['total_amount'].mean()
        avg_sales_outside_campaign = non_campaign_period['total_amount'].mean()
        
        avg_traffic_during_campaign = campaign_period['total_visits'].mean()
        avg_traffic_outside_campaign = non_campaign_period['total_visits'].mean()
        
        # 计算增长率
        sales_growth = ((avg_sales_during_campaign / avg_sales_outside_campaign) - 1) * 100 if avg_sales_outside_campaign > 0 else 0
        traffic_growth = ((avg_traffic_during_campaign / avg_traffic_outside_campaign) - 1) * 100 if avg_traffic_outside_campaign > 0 else 0
        
        # 显示活动效果比较
        st.write("#### 活动效果比较")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("活动期间平均日销售额", f"¥{avg_sales_during_campaign:,.2f}", f"{sales_growth:+.1f}%")
        
        with col2:
            st.metric("活动期间平均日访问量", f"{avg_traffic_during_campaign:,.0f}", f"{traffic_growth:+.1f}%")
        
        # 活动投资回报评估
        st.write("#### 活动投资回报评估")
        
        # 计算活动带来的额外销售额
        campaign_days = (campaign_data['end_date'] - campaign_data['start_date']).days + 1
        baseline_sales = avg_sales_outside_campaign * campaign_days
        actual_sales = campaign_period['total_amount'].sum()
        incremental_sales = actual_sales - baseline_sales
        
        # 计算投资回报
        campaign_roi = incremental_sales / campaign_data['spend'] if campaign_data['spend'] > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("基线销售额", f"¥{baseline_sales:,.2f}")
        
        with col2:
            st.metric("实际销售额", f"¥{actual_sales:,.2f}")
        
        with col3:
            st.metric("增量销售额", f"¥{incremental_sales:,.2f}")
        
        st.metric("活动投资回报率", f"{campaign_roi:.2f}x", f"每投入¥1产生¥{campaign_roi:.2f}的额外销售额")
        
        # 如果增量销售额为负，添加警告
        if incremental_sales < 0:
            st.warning("⚠️ 活动期间的销售额低于预期基线。应分析活动执行和定位是否存在问题。")
    else:
        st.error("无法进行活动期间趋势分析，因为流量数据中缺少日期列。") 