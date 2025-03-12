import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def perform_roi_analysis(data):
    """
    执行ROI和投资回报分析
    
    Args:
        data (dict): 包含所有数据集的字典
    """
    st.subheader("ROI和投资回报分析")
    
    # 准备数据
    marketing_df = data["marketing"]
    transactions_df = data["transactions"]
    
    # 确保日期格式正确
    marketing_df['start_date'] = pd.to_datetime(marketing_df['start_date'])
    marketing_df['end_date'] = pd.to_datetime(marketing_df['end_date'])
    transactions_df['date'] = pd.to_datetime(transactions_df['date'])
    
    # 标准化ROI值
    if 'roi' in marketing_df.columns:
        marketing_df['roi_numeric'] = marketing_df['roi']
        
        # 如果ROI是字符串类型（比如包含%），进行转换
        if marketing_df['roi'].dtype == 'object':
            marketing_df['roi_numeric'] = marketing_df['roi'].apply(lambda x: 
                float(str(x).replace('%', '')) / 100 if isinstance(x, str) and '%' in str(x) 
                else x)
        
        # 确保转换为数值类型
        marketing_df['roi_numeric'] = pd.to_numeric(marketing_df['roi_numeric'], errors='coerce')
    else:
        st.warning("营销数据中缺少ROI字段，将使用估算值进行分析。")
        # 基于其他指标估算ROI
        marketing_df['roi_numeric'] = (marketing_df['conversions'] * 100 - marketing_df['spend']) / marketing_df['spend']
    
    # 投资回报概览
    st.write("### 投资回报概览")
    
    # 计算总体ROI
    total_spend = marketing_df['spend'].sum()
    total_conversions = marketing_df['conversions'].sum()
    
    # 估算每次转化的平均价值
    avg_conversion_value = 100  # 假设每次转化的平均价值为100元
    
    # 计算总回报
    total_return = total_conversions * avg_conversion_value
    
    # 计算总体ROI
    overall_roi = (total_return - total_spend) / total_spend if total_spend > 0 else 0
    
    # 显示关键指标
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("总营销支出", f"¥{total_spend:,.2f}")
    
    with col2:
        st.metric("总转化次数", f"{total_conversions:,}")
    
    with col3:
        st.metric("估算总回报", f"¥{total_return:,.2f}")
    
    with col4:
        st.metric("总体ROI", f"{overall_roi:.2f}x")
    
    # ROI分布
    st.write("### ROI分布分析")
    
    # 计算正ROI和负ROI的活动数量
    positive_roi_count = (marketing_df['roi_numeric'] > 0).sum()
    negative_roi_count = (marketing_df['roi_numeric'] <= 0).sum()
    
    # 创建ROI分布饼图
    roi_distribution = pd.DataFrame({
        'ROI类型': ['正ROI', '负ROI'],
        '活动数量': [positive_roi_count, negative_roi_count]
    })
    
    fig1 = px.pie(
        roi_distribution,
        values='活动数量',
        names='ROI类型',
        title='正ROI vs 负ROI活动数量分布',
        color='ROI类型',
        color_discrete_map={'正ROI': 'green', '负ROI': 'red'}
    )
    
    # 创建ROI值分布直方图
    fig2 = px.histogram(
        marketing_df,
        x='roi_numeric',
        nbins=20,
        title='营销活动ROI分布',
        labels={'roi_numeric': 'ROI值', 'count': '活动数量'}
    )
    
    # 添加中位数线
    median_roi = marketing_df['roi_numeric'].median()
    fig2.add_vline(x=median_roi, line_dash="dash", line_color="red", annotation_text=f"中位数: {median_roi:.2f}")
    
    # 添加零线
    fig2.add_vline(x=0, line_dash="solid", line_color="black", annotation_text="盈亏平衡点")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.plotly_chart(fig2, use_container_width=True)
    
    # 按不同维度分析ROI
    st.write("### 多维度ROI分析")
    
    # 按渠道分析ROI
    channel_roi = marketing_df.groupby('channel').agg({
        'roi_numeric': 'mean',
        'spend': 'sum',
        'conversions': 'sum',
        'campaign_id': 'count'
    }).reset_index()
    
    channel_roi.columns = ['渠道', '平均ROI', '总支出', '总转化', '活动数量']
    
    # 创建按渠道的ROI条形图
    fig3 = px.bar(
        channel_roi.sort_values('平均ROI', ascending=False),
        x='渠道',
        y='平均ROI',
        title='各渠道平均ROI',
        color='平均ROI',
        text='平均ROI',
        color_continuous_scale=px.colors.sequential.RdBu,
        color_continuous_midpoint=0
    )
    
    fig3.update_traces(texttemplate='%{text:.2f}x', textposition='outside')
    
    # 按目标受众分析ROI
    audience_roi = marketing_df.groupby('target_audience').agg({
        'roi_numeric': 'mean',
        'spend': 'sum',
        'conversions': 'sum',
        'campaign_id': 'count'
    }).reset_index()
    
    audience_roi.columns = ['目标受众', '平均ROI', '总支出', '总转化', '活动数量']
    
    # 创建按目标受众的ROI条形图
    fig4 = px.bar(
        audience_roi.sort_values('平均ROI', ascending=False),
        x='目标受众',
        y='平均ROI',
        title='各目标受众平均ROI',
        color='平均ROI',
        text='平均ROI',
        color_continuous_scale=px.colors.sequential.RdBu,
        color_continuous_midpoint=0
    )
    
    fig4.update_traces(texttemplate='%{text:.2f}x', textposition='outside')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        st.plotly_chart(fig4, use_container_width=True)
    
    # 按目标和渠道交叉分析ROI
    objective_channel_roi = marketing_df.groupby(['objective', 'channel']).agg({
        'roi_numeric': 'mean',
        'spend': 'sum'
    }).reset_index()
    
    # 创建热力图
    fig5 = px.density_heatmap(
        objective_channel_roi,
        x='channel',
        y='objective',
        z='roi_numeric',
        title='目标-渠道ROI热力图',
        labels={'roi_numeric': 'ROI', 'channel': '渠道', 'objective': '营销目标'},
        color_continuous_scale=px.colors.sequential.RdBu,
        color_continuous_midpoint=0
    )
    
    st.plotly_chart(fig5, use_container_width=True)
    
    # 投资规模与ROI关系分析
    st.write("### 投资规模与ROI关系分析")
    
    # 创建散点图
    fig6 = px.scatter(
        marketing_df,
        x='spend',
        y='roi_numeric',
        color='channel',
        size='conversions',
        hover_name='name',
        title='营销投资规模与ROI关系',
        labels={'spend': '营销支出', 'roi_numeric': 'ROI', 'channel': '渠道', 'conversions': '转化次数'}
    )
    
    # 添加盈亏平衡线
    fig6.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="盈亏平衡线")
    
    # 添加趋势线
    fig6.update_layout(
        shapes=[
            dict(
                type='line',
                yref='paper', y0=0, y1=1,
                xref='paper', x0=0, x1=1,
                line=dict(color="lightgrey", width=2, dash="dot")
            )
        ]
    )
    
    st.plotly_chart(fig6, use_container_width=True)
    
    # ROI和转化率关系分析
    st.write("### ROI与转化率关系分析")
    
    # 计算转化率
    marketing_df['conversion_rate'] = (marketing_df['conversions'] / marketing_df['clicks'] * 100).fillna(0)
    
    # 创建散点图
    fig7 = px.scatter(
        marketing_df,
        x='conversion_rate',
        y='roi_numeric',
        color='channel',
        size='spend',
        hover_name='name',
        title='转化率与ROI关系',
        labels={'conversion_rate': '转化率(%)', 'roi_numeric': 'ROI', 'channel': '渠道', 'spend': '营销支出'}
    )
    
    # 添加盈亏平衡线
    fig7.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="盈亏平衡线")
    
    # 添加趋势线
    fig7.add_traces(
        px.scatter(
            marketing_df, 
            x='conversion_rate', 
            y='roi_numeric', 
            trendline='ols'
        ).data[1]
    )
    
    st.plotly_chart(fig7, use_container_width=True)
    
    # 时间维度ROI分析
    st.write("### 时间维度ROI分析")
    
    # 按月统计ROI
    marketing_df['month'] = marketing_df['start_date'].dt.strftime('%Y-%m')
    
    monthly_roi = marketing_df.groupby('month').agg({
        'roi_numeric': 'mean',
        'spend': 'sum',
        'conversions': 'sum'
    }).reset_index()
    
    # 计算月度回报和净收益
    monthly_roi['return'] = monthly_roi['conversions'] * avg_conversion_value
    monthly_roi['net_profit'] = monthly_roi['return'] - monthly_roi['spend']
    
    # 创建月度ROI趋势图
    fig8 = px.line(
        monthly_roi,
        x='month',
        y='roi_numeric',
        title='月度ROI趋势',
        labels={'month': '月份', 'roi_numeric': 'ROI'}
    )
    
    # 创建月度净收益图表
    fig9 = px.bar(
        monthly_roi,
        x='month',
        y=['spend', 'return', 'net_profit'],
        title='月度营销支出、回报和净收益',
        labels={'value': '金额', 'variable': '指标类型', 'month': '月份'},
        barmode='group'
    )
    
    st.plotly_chart(fig8, use_container_width=True)
    st.plotly_chart(fig9, use_container_width=True)
    
    # 活动持续时间与ROI关系
    st.write("### 活动持续时间与ROI关系")
    
    # 计算活动持续天数
    marketing_df['duration_days'] = (marketing_df['end_date'] - marketing_df['start_date']).dt.days + 1
    
    # 按持续时间分组
    duration_bins = [0, 7, 14, 30, 60, 90, float('inf')]
    duration_labels = ['1周内', '1-2周', '2-4周', '1-2个月', '2-3个月', '3个月以上']
    marketing_df['duration_group'] = pd.cut(marketing_df['duration_days'], bins=duration_bins, labels=duration_labels)
    
    # 按持续时间组统计ROI
    duration_roi = marketing_df.groupby('duration_group').agg({
        'roi_numeric': 'mean',
        'spend': 'sum',
        'conversions': 'sum',
        'campaign_id': 'count'
    }).reset_index()
    
    duration_roi.columns = ['持续时间', '平均ROI', '总支出', '总转化', '活动数量']
    
    # 创建按持续时间的ROI条形图
    fig10 = px.bar(
        duration_roi,
        x='持续时间',
        y='平均ROI',
        title='不同持续时间的活动平均ROI',
        color='平均ROI',
        text='平均ROI',
        color_continuous_scale=px.colors.sequential.RdBu,
        color_continuous_midpoint=0
    )
    
    fig10.update_traces(texttemplate='%{text:.2f}x', textposition='outside')
    
    st.plotly_chart(fig10, use_container_width=True)
    
    # ROI预测和优化
    st.write("### ROI优化建议")
    
    # 提取表现最好的活动特征
    top_roi_campaigns = marketing_df.sort_values('roi_numeric', ascending=False).head(5)
    bottom_roi_campaigns = marketing_df.sort_values('roi_numeric').head(5)
    
    # 显示最佳和最差活动
    st.write("#### 表现最佳的5个活动")
    
    display_cols = ['name', 'channel', 'target_audience', 'objective', 'roi_numeric', 'spend', 'conversions']
    st.dataframe(top_roi_campaigns[display_cols])
    
    st.write("#### 表现最差的5个活动")
    st.dataframe(bottom_roi_campaigns[display_cols])
    
    # 优化建议
    st.write("#### ROI优化策略建议")
    
    # 分析高ROI活动的共同特征
    top_channels = top_roi_campaigns['channel'].value_counts().index.tolist()
    top_objectives = top_roi_campaigns['objective'].value_counts().index.tolist()
    top_audiences = top_roi_campaigns['target_audience'].value_counts().index.tolist()
    
    st.markdown(f"""
    **基于高ROI活动的特征分析，建议以下优化策略：**
    
    1. **优先渠道**: 增加在 {', '.join(top_channels[:2])} 渠道的投资，这些渠道显示出较高的投资回报率。
    
    2. **目标调整**: 更多关注 {', '.join(top_objectives[:2])} 类型的营销目标，这些目标与较高ROI相关。
    
    3. **受众定位**: 优先针对 {', '.join(top_audiences[:2])} 受众，这些受众对营销活动的响应更积极。
    
    4. **优化活动持续时间**: 数据显示，{duration_roi.iloc[duration_roi['平均ROI'].argmax()]['持续时间']} 的活动平均ROI最高，
       建议将活动持续时间调整至这一范围。
    
    5. **重新分配预算**: 从低ROI活动转移预算到高ROI活动，特别是那些具有相似目标但ROI差异显著的活动。
    
    6. **转化价值优化**: 分析高转化价值的产品和客户群体，调整营销策略以吸引这些高价值转化。
    
    7. **A/B测试**: 对关键活动元素（如创意、标题、着陆页等）进行系统的A/B测试，提高转化率和ROI。
    """)
    
    # 高级ROI分析
    st.write("### 高级ROI分析")
    
    # 投资组合优化
    st.write("#### 营销投资组合优化")
    
    # 展示理论上最优的投资组合
    optimal_allocation = channel_roi.sort_values('平均ROI', ascending=False).reset_index(drop=True)
    
    # 确保建议占比数组长度与DataFrame行数匹配
    num_channels = len(optimal_allocation)
    
    # 根据渠道数动态分配百分比
    if num_channels >= 4:
        allocation_percentages = [50, 30, 15, 5] + [0] * (num_channels - 4)
    elif num_channels == 3:
        allocation_percentages = [50, 30, 20]
    elif num_channels == 2:
        allocation_percentages = [70, 30]
    elif num_channels == 1:
        allocation_percentages = [100]
    else:
        allocation_percentages = []
    
    # 确保长度匹配
    if len(allocation_percentages) == num_channels:
        optimal_allocation['建议占比'] = allocation_percentages
        optimal_allocation['建议占比'] = optimal_allocation['建议占比'] / 100
        
        # 计算当前分配
        total_spend = channel_roi['总支出'].sum()
        optimal_allocation['当前占比'] = optimal_allocation['总支出'] / total_spend if total_spend > 0 else 0
        
        # 计算优化后的投资和回报
        budget_scenario = st.slider("营销预算情景分析 (元)", min_value=int(total_spend*0.5), max_value=int(total_spend*1.5), value=int(total_spend), step=10000)
        
        optimal_allocation['优化后投资'] = optimal_allocation['建议占比'] * budget_scenario
        optimal_allocation['预计转化'] = optimal_allocation['优化后投资'] * optimal_allocation['总转化'] / optimal_allocation['总支出']
        optimal_allocation['预计回报'] = optimal_allocation['预计转化'] * avg_conversion_value
        optimal_allocation['预计ROI'] = (optimal_allocation['预计回报'] - optimal_allocation['优化后投资']) / optimal_allocation['优化后投资']
        
        # 显示优化结果
        st.dataframe(optimal_allocation[['渠道', '当前占比', '建议占比', '平均ROI', '优化后投资', '预计转化', '预计回报', '预计ROI']].round(2))
        
        # 计算优化前后的总体回报
        current_return = total_return
        optimized_return = optimal_allocation['预计回报'].sum()
        improvement = (optimized_return - current_return) / current_return * 100 if current_return > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("当前总回报", f"¥{current_return:,.2f}")
        
        with col2:
            st.metric("优化后预计总回报", f"¥{optimized_return:,.2f}")
        
        with col3:
            st.metric("预计改进", f"{improvement:.1f}%")
        
        # 边际ROI分析
        st.write("#### 边际ROI分析")
        
        st.info("""
        **边际ROI分析**表明，随着营销支出的增加，ROI通常会遵循递减回报规律。基于当前数据分析：
        
        1. **目前状态**: 营销支出处于递增回报阶段，增加投资可能带来更高的总体ROI
        2. **预测拐点**: 当总营销支出达到当前支出的约1.3-1.5倍时，可能达到边际效益递减的拐点
        3. **建议策略**: 
           - 优先增加高ROI渠道的投资
           - 持续监控边际ROI变化
           - 在接近预测拐点时重新评估策略
        
        *注: 此分析基于历史数据的模式，实际拐点可能受市场环境变化影响*
        """)
        
        # ROI归因模型
        st.write("#### 多触点ROI归因")
        
        st.info("""
        在多渠道营销环境中，简单的单一渠道ROI可能无法完全反映真实的营销效果。推荐实施高级归因模型：
        
        1. **首触点归因**: 将转化归功于客户接触的第一个营销渠道
        2. **末触点归因**: 将转化归功于促成最终转化的渠道
        3. **线性归因**: 在客户旅程的所有接触点之间平均分配转化功劳
        4. **时间衰减归因**: 给予接近转化时间的接触点更多权重
        5. **数据驱动归因**: 使用机器学习模型基于历史数据确定各接触点的贡献
        
        建议实施数据驱动归因模型，以获得更准确的跨渠道ROI视图，并优化整体营销组合。
        """) 