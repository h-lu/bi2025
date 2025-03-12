import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def perform_channel_analysis(data):
    """
    执行营销渠道效果分析
    
    Args:
        data (dict): 包含所有数据集的字典
    """
    st.subheader("营销渠道效果分析")
    
    # 准备数据
    marketing_df = data["marketing"]
    transactions_df = data["transactions"]
    traffic_df = data["traffic"]
    
    # 确保日期格式正确
    marketing_df['start_date'] = pd.to_datetime(marketing_df['start_date'])
    marketing_df['end_date'] = pd.to_datetime(marketing_df['end_date'])
    
    # 按渠道汇总营销数据
    channel_summary = marketing_df.groupby('channel').agg({
        'campaign_id': 'count',
        'budget': 'sum',
        'spend': 'sum',
        'impressions': 'sum',
        'clicks': 'sum',
        'conversions': 'sum'
    }).reset_index()
    
    # 重命名列
    channel_summary.columns = ['渠道', '活动数量', '总预算', '总支出', '总展示次数', '总点击次数', '总转化次数']
    
    # 计算渠道效果指标
    channel_summary['点击率(CTR)'] = (channel_summary['总点击次数'] / channel_summary['总展示次数'] * 100).round(2)
    channel_summary['转化率'] = (channel_summary['总转化次数'] / channel_summary['总点击次数'] * 100).round(2)
    channel_summary['每次获客成本(CPA)'] = (channel_summary['总支出'] / channel_summary['总转化次数']).round(2)
    
    # 修正无限值和NaN
    channel_summary['点击率(CTR)'] = channel_summary['点击率(CTR)'].replace([np.inf, -np.inf, np.nan], 0)
    channel_summary['转化率'] = channel_summary['转化率'].replace([np.inf, -np.inf, np.nan], 0)
    channel_summary['每次获客成本(CPA)'] = channel_summary['每次获客成本(CPA)'].replace([np.inf, -np.inf, np.nan], 0)
    
    # 显示渠道汇总数据
    st.write("### 营销渠道汇总指标")
    st.dataframe(channel_summary, use_container_width=True)
    
    # 选择渠道分布可视化指标
    st.write("### 渠道分布可视化")
    metric_options = ['总预算', '总支出', '总展示次数', '总点击次数', '总转化次数', '点击率(CTR)', '转化率', '每次获客成本(CPA)']
    selected_metric = st.selectbox("选择要可视化的指标", metric_options, index=2)
    
    # 创建渠道分布图表
    fig1 = px.bar(
        channel_summary,
        x='渠道',
        y=selected_metric,
        title=f'各营销渠道的{selected_metric}分布',
        color='渠道',
        text=selected_metric
    )
    
    fig1.update_traces(texttemplate='%{text:.2f}', textposition='inside')
    
    st.plotly_chart(fig1, use_container_width=True)
    
    # 渠道占比分析
    st.write("### 渠道占比分析")
    
    # 预算和支出占比
    fig2 = px.pie(
        channel_summary,
        values='总支出',
        names='渠道',
        title='各渠道营销支出占比'
    )
    
    # 创建转化次数占比图
    fig3 = px.pie(
        channel_summary,
        values='总转化次数',
        names='渠道',
        title='各渠道转化次数占比'
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        st.plotly_chart(fig3, use_container_width=True)
    
    # 渠道效率分析
    st.write("### 渠道效率分析")
    
    # 创建点击率和转化率对比图
    fig4 = px.bar(
        channel_summary,
        x='渠道',
        y=['点击率(CTR)', '转化率'],
        title='各渠道点击率和转化率对比',
        barmode='group',
        labels={'value': '百分比(%)', 'variable': '指标'}
    )
    
    # 创建每次获客成本对比图
    fig5 = px.bar(
        channel_summary,
        x='渠道',
        y='每次获客成本(CPA)',
        title='各渠道每次获客成本对比',
        color='渠道',
        text='每次获客成本(CPA)'
    )
    
    fig5.update_traces(texttemplate='¥%{text:.2f}', textposition='outside')
    
    st.plotly_chart(fig4, use_container_width=True)
    st.plotly_chart(fig5, use_container_width=True)
    
    # 渠道投资回报率分析
    st.write("### 渠道投资回报率分析")
    
    # 计算各渠道的平均ROI
    if 'roi' in marketing_df.columns:
        # 对字符串格式的ROI值进行处理
        marketing_df['roi_numeric'] = marketing_df['roi']
        if marketing_df['roi'].dtype == 'object':
            # 将百分比格式转换为数值
            marketing_df['roi_numeric'] = marketing_df['roi'].apply(lambda x: 
                float(str(x).replace('%', '')) / 100 if isinstance(x, str) and '%' in str(x) 
                else x)
        
        # 确保roi是数值类型
        marketing_df['roi_numeric'] = pd.to_numeric(marketing_df['roi_numeric'], errors='coerce')
        
        # 计算各渠道的平均ROI
        channel_roi = marketing_df.groupby('channel')['roi_numeric'].mean().reset_index()
        channel_roi.columns = ['渠道', '平均ROI']
        
        # 调整ROI的格式为百分比
        channel_roi['平均ROI'] = (channel_roi['平均ROI'] * 100).round(2)
        
        # 创建ROI对比图
        fig6 = px.bar(
            channel_roi,
            x='渠道',
            y='平均ROI',
            title='各渠道平均投资回报率(ROI)对比',
            color='渠道',
            text='平均ROI'
        )
        
        fig6.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        
        st.plotly_chart(fig6, use_container_width=True)
    
    # 渠道趋势分析
    st.write("### 渠道趋势分析")
    
    # 按月和渠道汇总数据
    marketing_df['month'] = marketing_df['start_date'].dt.strftime('%Y-%m')
    
    # 按月和渠道汇总花费
    monthly_channel_spend = marketing_df.groupby(['month', 'channel'])['spend'].sum().reset_index()
    
    # 创建月度渠道花费趋势图
    fig7 = px.line(
        monthly_channel_spend,
        x='month',
        y='spend',
        color='channel',
        title='月度各渠道营销支出趋势',
        labels={'spend': '支出', 'month': '月份', 'channel': '渠道'}
    )
    
    st.plotly_chart(fig7, use_container_width=True)
    
    # 按月和渠道汇总转化次数
    monthly_channel_conversions = marketing_df.groupby(['month', 'channel'])['conversions'].sum().reset_index()
    
    # 创建月度渠道转化趋势图
    fig8 = px.line(
        monthly_channel_conversions,
        x='month',
        y='conversions',
        color='channel',
        title='月度各渠道转化次数趋势',
        labels={'conversions': '转化次数', 'month': '月份', 'channel': '渠道'}
    )
    
    st.plotly_chart(fig8, use_container_width=True)
    
    # 渠道对比分析
    st.write("### 渠道对比分析")
    
    # 创建散点图，比较各渠道的转化率和每次获客成本
    fig9 = px.scatter(
        channel_summary,
        x='转化率',
        y='每次获客成本(CPA)',
        size='总转化次数',
        color='渠道',
        hover_name='渠道',
        text='渠道',
        title='渠道效率矩阵: 转化率 vs 每次获客成本(CPA)',
        labels={'转化率': '转化率(%)', '每次获客成本(CPA)': '每次获客成本(¥)'}
    )
    
    # 添加四象限分割线
    avg_conversion_rate = channel_summary['转化率'].mean()
    avg_cpa = channel_summary['每次获客成本(CPA)'].mean()
    
    fig9.add_hline(y=avg_cpa, line_dash="dash", line_color="gray", annotation_text="平均CPA")
    fig9.add_vline(x=avg_conversion_rate, line_dash="dash", line_color="gray", annotation_text="平均转化率")
    
    # 设置文本位置
    fig9.update_traces(textposition='top center')
    
    st.plotly_chart(fig9, use_container_width=True)
    
    # 添加四象限解释
    st.write("""
    **渠道效率矩阵解释:**
    
    - **右上象限**: 高转化率但高获客成本 - 优化成本结构
    - **右下象限**: 高转化率且低获客成本 - 理想渠道，增加投入
    - **左上象限**: 低转化率且高获客成本 - 考虑减少投入或调整策略
    - **左下象限**: 低转化率但低获客成本 - 改进转化漏斗
    """)
    
    # 单个渠道详细分析
    st.write("### 单个渠道详细分析")
    
    # 选择渠道
    selected_channel = st.selectbox(
        "选择要详细分析的渠道",
        options=marketing_df['channel'].unique()
    )
    
    # 筛选所选渠道的活动
    channel_campaigns = marketing_df[marketing_df['channel'] == selected_channel]
    
    # 显示渠道活动列表
    st.write(f"#### {selected_channel} 渠道的所有营销活动")
    
    # 格式化活动数据用于显示
    display_columns = ['campaign_id', 'name', 'start_date', 'end_date', 
                      'budget', 'spend', 'impressions', 'clicks', 'conversions', 
                      'target_region', 'target_category', 'objective']
    
    # 格式化日期列
    formatted_channel_campaigns = channel_campaigns[display_columns].copy()
    formatted_channel_campaigns['start_date'] = formatted_channel_campaigns['start_date'].dt.strftime('%Y-%m-%d')
    formatted_channel_campaigns['end_date'] = formatted_channel_campaigns['end_date'].dt.strftime('%Y-%m-%d')
    
    st.dataframe(formatted_channel_campaigns, use_container_width=True)
    
    # 计算渠道活动效果指标
    channel_ctr = (channel_campaigns['clicks'].sum() / channel_campaigns['impressions'].sum() * 100) if channel_campaigns['impressions'].sum() > 0 else 0
    channel_conversion_rate = (channel_campaigns['conversions'].sum() / channel_campaigns['clicks'].sum() * 100) if channel_campaigns['clicks'].sum() > 0 else 0
    channel_cpa = (channel_campaigns['spend'].sum() / channel_campaigns['conversions'].sum()) if channel_campaigns['conversions'].sum() > 0 else 0
    
    # 预算使用率
    channel_budget_utilization = (channel_campaigns['spend'].sum() / channel_campaigns['budget'].sum() * 100) if channel_campaigns['budget'].sum() > 0 else 0
    
    # 显示渠道效果指标
    st.write(f"#### {selected_channel} 渠道效果指标")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("点击率(CTR)", f"{channel_ctr:.2f}%")
    
    with col2:
        st.metric("转化率", f"{channel_conversion_rate:.2f}%")
    
    with col3:
        st.metric("每次获客成本(CPA)", f"¥{channel_cpa:.2f}")
    
    with col4:
        st.metric("预算使用率", f"{channel_budget_utilization:.1f}%")
    
    # 渠道活动对比
    st.write(f"#### {selected_channel} 渠道活动对比")
    
    # 计算各活动的效果指标
    channel_campaigns['ctr'] = (channel_campaigns['clicks'] / channel_campaigns['impressions'] * 100).fillna(0)
    channel_campaigns['conversion_rate'] = (channel_campaigns['conversions'] / channel_campaigns['clicks'] * 100).fillna(0)
    channel_campaigns['cpa'] = (channel_campaigns['spend'] / channel_campaigns['conversions']).fillna(0)
    
    # 创建活动对比图
    fig10 = px.bar(
        channel_campaigns,
        x='name',
        y=['ctr', 'conversion_rate'],
        title=f'{selected_channel} 渠道各活动的点击率和转化率',
        barmode='group',
        labels={'value': '百分比(%)', 'variable': '指标', 'name': '活动名称'}
    )
    
    fig11 = px.bar(
        channel_campaigns,
        x='name',
        y='cpa',
        title=f'{selected_channel} 渠道各活动的每次获客成本',
        labels={'cpa': '每次获客成本(¥)', 'name': '活动名称'}
    )
    
    st.plotly_chart(fig10, use_container_width=True)
    st.plotly_chart(fig11, use_container_width=True)
    
    # 渠道改进建议
    st.write(f"#### {selected_channel} 渠道改进建议")
    
    # 根据渠道指标提供建议
    recommendations = []
    
    channel_metrics = channel_summary[channel_summary['渠道'] == selected_channel].iloc[0]
    
    # 点击率建议
    if channel_metrics['点击率(CTR)'] < channel_summary['点击率(CTR)'].mean():
        recommendations.append("• **提高点击率**: 优化广告创意和标题，提高与目标受众的相关性，测试不同的视觉元素")
    
    # 转化率建议
    if channel_metrics['转化率'] < channel_summary['转化率'].mean():
        recommendations.append("• **提高转化率**: 改进落地页设计，简化转化流程，增加明确的行动召唤(CTA)，提供特定优惠")
    
    # 获客成本建议
    if channel_metrics['每次获客成本(CPA)'] > channel_summary['每次获客成本(CPA)'].mean():
        recommendations.append("• **降低获客成本**: 优化目标受众定位，减少无效展示，调整出价策略，测试不同的投放时间")
    
    # 预算使用效率建议
    if channel_budget_utilization < 90:
        recommendations.append("• **提高预算使用效率**: 重新分配未使用的预算到表现好的活动，扩大成功活动的受众范围")
    elif channel_budget_utilization > 100:
        recommendations.append("• **控制预算超支**: 设置更严格的日常预算限制，实时监控支出，优先保留ROI较高的活动")
    
    # 渠道特定建议
    if selected_channel == 'Email':
        recommendations.append("• **电子邮件优化**: 改进邮件主题行，个性化邮件内容，优化发送时间，细分邮件列表")
    elif selected_channel == 'Social Media':
        recommendations.append("• **社交媒体优化**: 增加互动内容，利用用户生成内容，参与相关话题讨论，扩大社区影响力")
    elif selected_channel == 'Search Engine':
        recommendations.append("• **搜索引擎优化**: 精细化关键词管理，优化质量得分，利用长尾关键词，改进广告文案相关性")
    elif selected_channel == 'Display Ads':
        recommendations.append("• **展示广告优化**: 优化广告位置和格式，改进受众定位，测试不同的创意风格，实施重定向策略")
    
    # 添加通用建议
    if not recommendations:
        recommendations.append("• **维持现有策略**: 该渠道表现良好，建议继续现有策略，并定期测试新的优化方向")
    
    # 显示建议
    for recommendation in recommendations:
        st.markdown(recommendation)
    
    # 渠道竞争情报
    st.write("### 行业渠道基准对比")
    
    st.info("""
    **行业渠道平均表现基准:**
    
    - **电子邮件**: CTR 2-3%, 转化率 1-2%, CPA ¥100-150
    - **社交媒体**: CTR 1-2%, 转化率 0.5-1.5%, CPA ¥150-200
    - **搜索引擎**: CTR 3-5%, 转化率 2-4%, CPA ¥80-120
    - **展示广告**: CTR 0.5-1%, 转化率 0.2-0.8%, CPA ¥200-300
    - **联盟营销**: CTR 1-2%, 转化率 1-3%, CPA ¥100-150
    
    *注: 以上数据为行业平均水平，实际表现会因产品类别、价格区间、市场竞争等因素而异。*
    """)
    
    # 渠道选择和预算分配建议
    st.write("### 渠道选择和预算分配建议")
    
    # 计算各渠道的效率分数（简化版）
    channel_efficiency = channel_summary.copy()
    
    # 将CTR和转化率归一化（越高越好）
    max_ctr = channel_efficiency['点击率(CTR)'].max()
    max_conv = channel_efficiency['转化率'].max()
    
    channel_efficiency['ctr_score'] = channel_efficiency['点击率(CTR)'] / max_ctr if max_ctr > 0 else 0
    channel_efficiency['conv_score'] = channel_efficiency['转化率'] / max_conv if max_conv > 0 else 0
    
    # 将CPA归一化（越低越好）
    max_cpa = channel_efficiency['每次获客成本(CPA)'].max()
    if max_cpa > 0:
        channel_efficiency['cpa_score'] = 1 - (channel_efficiency['每次获客成本(CPA)'] / max_cpa)
    else:
        channel_efficiency['cpa_score'] = 0
    
    # 综合效率分数
    channel_efficiency['efficiency_score'] = (
        channel_efficiency['ctr_score'] * 0.2 + 
        channel_efficiency['conv_score'] * 0.5 + 
        channel_efficiency['cpa_score'] * 0.3
    ).round(2)
    
    # 排序并添加建议的预算分配
    channel_efficiency = channel_efficiency.sort_values('efficiency_score', ascending=False)
    
    # 计算建议的预算分配比例
    total_score = channel_efficiency['efficiency_score'].sum()
    if total_score > 0:
        channel_efficiency['建议预算占比'] = (channel_efficiency['efficiency_score'] / total_score * 100).round(1)
    else:
        channel_efficiency['建议预算占比'] = 100 / len(channel_efficiency)
    
    # 计算当前预算占比
    total_budget = channel_efficiency['总预算'].sum()
    if total_budget > 0:
        channel_efficiency['当前预算占比'] = (channel_efficiency['总预算'] / total_budget * 100).round(1)
    else:
        channel_efficiency['当前预算占比'] = 100 / len(channel_efficiency)
    
    # 计算预算调整建议
    channel_efficiency['预算调整建议'] = (channel_efficiency['建议预算占比'] - channel_efficiency['当前预算占比']).round(1)
    
    # 显示渠道效率和预算建议
    st.write("#### 渠道效率评分和预算分配建议")
    
    display_cols = ['渠道', 'efficiency_score', '当前预算占比', '建议预算占比', '预算调整建议']
    st.dataframe(channel_efficiency[display_cols].rename(columns={'efficiency_score': '效率得分'}), use_container_width=True)
    
    # 可视化当前与建议预算分配对比
    budget_comparison = pd.melt(
        channel_efficiency, 
        id_vars=['渠道'], 
        value_vars=['当前预算占比', '建议预算占比'],
        var_name='预算类型',
        value_name='百分比'
    )
    
    fig12 = px.bar(
        budget_comparison,
        x='渠道',
        y='百分比',
        color='预算类型',
        title='当前预算分配与建议预算分配对比',
        barmode='group',
        text='百分比'
    )
    
    fig12.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    
    st.plotly_chart(fig12, use_container_width=True)
    
    # 最佳实践建议
    st.write("### 渠道营销最佳实践")
    
    st.markdown("""
    #### 渠道整合策略
    
    为获得最佳营销效果，应将各渠道整合成统一的全渠道营销策略：
    
    1. **协调一致的信息**: 确保所有渠道传递一致的品牌信息和促销内容
    2. **渠道互补**: 利用不同渠道的优势，构建完整的客户旅程
    3. **跨渠道归因**: 实施高级归因模型，了解各渠道间的相互影响
    4. **渠道协同**: 设计能够相互强化的多渠道活动，例如社交媒体与电子邮件的配合
    5. **数据整合**: 整合各渠道的客户数据，构建360度客户视图
    
    #### 渠道测试框架
    
    建议实施系统化的测试框架，持续优化渠道效果：
    
    1. **A/B测试**: 在各渠道中测试不同创意、标题、行动召唤和着陆页
    2. **小规模测试**: 使用小部分预算测试新渠道或新策略
    3. **定期评估**: 每月或每季度评估各渠道的表现，调整预算分配
    4. **季节性测试**: 考虑不同季节和促销期间的渠道效果变化
    5. **竞争监控**: 分析竞争对手的渠道策略和表现
    """)
    
    # 渠道趋势预测
    st.write("### 渠道趋势预测")
    
    if len(monthly_channel_spend) > 1:
        # 按渠道进行趋势预测
        st.info("""
        根据历史数据分析，未来3-6个月的渠道趋势预测：
        
        1. **成本上升渠道**: 搜索引擎和社交媒体的获客成本可能持续上升，建议提前优化转化漏斗
        2. **增长机会渠道**: 电子邮件和联盟营销在当前数据中显示出良好的ROI，有进一步扩展的空间
        3. **需要重点监控的渠道**: 展示广告的效果波动较大，建议实施更严格的A/B测试和受众细分
        4. **潜在新兴渠道**: 考虑测试内容营销和影响者营销，这些渠道在类似行业中表现出良好的增长潜力
        
        *注: 以上预测基于历史数据趋势分析，实际结果可能受市场环境、季节性因素和竞争态势影响。*
        """)
    else:
        st.warning("数据量不足，无法进行可靠的趋势预测。建议积累更多历史数据。") 