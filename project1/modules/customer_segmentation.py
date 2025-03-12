import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def perform_customer_segmentation(data):
    """
    执行客户细分分析
    
    Args:
        data (dict): 包含所有数据集的字典
    """
    # 添加分析选项
    analysis_type = st.radio(
        "选择细分分析方法",
        ["RFM分析", "K-means聚类", "消费行为分析"],
        horizontal=True
    )
    
    # 根据选择执行不同的分析
    if analysis_type == "RFM分析":
        perform_rfm_analysis(data)
    elif analysis_type == "K-means聚类":
        perform_kmeans_clustering(data)
    elif analysis_type == "消费行为分析":
        perform_behavioral_analysis(data)

def perform_rfm_analysis(data):
    """
    执行RFM客户细分分析
    
    Args:
        data (dict): 包含所有数据集的字典
    """
    st.subheader("RFM客户细分分析")
    
    st.write("""
    RFM分析是一种根据客户行为对客户进行细分的方法，基于三个关键指标：
    - **最近消费(Recency)**: 客户最近一次购买的时间
    - **消费频率(Frequency)**: 客户购买的频率
    - **消费金额(Monetary)**: 客户消费的金额
    """)
    
    # 准备数据
    customers_df = data["customers"]
    transactions_df = data["transactions"]
    
    # 确保日期格式正确
    transactions_df['date'] = pd.to_datetime(transactions_df['date'])
    
    # 计算RFM指标
    # 最近消费(R): 计算最后一次购买距今的天数
    latest_purchase = transactions_df.groupby('customer_id')['date'].max().reset_index()
    latest_purchase.columns = ['customer_id', 'latest_purchase']
    latest_purchase['recency'] = (pd.to_datetime('today') - latest_purchase['latest_purchase']).dt.days
    
    # 消费频率(F): 计算购买次数
    purchase_frequency = transactions_df.groupby('customer_id')['transaction_id'].nunique().reset_index()
    purchase_frequency.columns = ['customer_id', 'frequency']
    
    # 消费金额(M): 计算总消费金额
    purchase_monetary = transactions_df.groupby('customer_id')['total_amount'].sum().reset_index()
    
    # 合并RFM数据
    rfm_df = latest_purchase.merge(purchase_frequency, on='customer_id')
    rfm_df = rfm_df.merge(purchase_monetary, on='customer_id')
    
    # 添加客户信息
    rfm_df = rfm_df.merge(customers_df[['customer_id', 'name', 'segment', 'region', 'gender']], on='customer_id', how='left')
    
    # 显示RFM数据样本
    st.write("RFM数据样本：")
    st.dataframe(rfm_df.head())
    
    # 创建RFM得分
    # 逆序转换最近消费(R)，使较小的值(更近的购买)获得更高的分数
    rfm_df['r_score'] = pd.qcut(rfm_df['recency'], 5, labels=[5, 4, 3, 2, 1])
    # 频率(F)和金额(M)转换
    rfm_df['f_score'] = pd.qcut(rfm_df['frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
    rfm_df['m_score'] = pd.qcut(rfm_df['total_amount'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
    
    # 计算RFM总分
    rfm_df['rfm_score'] = rfm_df['r_score'].astype(int) + rfm_df['f_score'].astype(int) + rfm_df['m_score'].astype(int)
    
    # 进行客户分群
    rfm_df['customer_segment'] = pd.qcut(rfm_df['rfm_score'], 4, 
                                         labels=['低价值客户', '一般价值客户', '高价值客户', '顶级价值客户'])
    
    # 显示分群结果
    st.subheader("RFM客户分群结果")
    
    # 各分群的客户数量
    segment_counts = rfm_df['customer_segment'].value_counts().reset_index()
    segment_counts.columns = ['客户分群', '客户数量']
    
    # 分群分布
    fig1 = px.pie(segment_counts, values='客户数量', names='客户分群', 
                  title='客户分群分布',
                  color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig1, use_container_width=True)
    
    # 显示各分群的RFM特征
    segment_characteristics = rfm_df.groupby('customer_segment').agg({
        'recency': 'mean',
        'frequency': 'mean',
        'total_amount': 'mean',
        'rfm_score': 'mean'
    }).reset_index()
    
    st.write("各客户分群的平均特征：")
    st.dataframe(segment_characteristics)
    
    # 创建雷达图展示各分群的RFM特征
    st.subheader("各客户群RFM特征对比")
    
    # 准备雷达图数据 - 确保数值类型
    try:
        # 确保r_score, f_score, m_score为数值类型
        for col in ['r_score', 'f_score', 'm_score']:
            if rfm_df[col].dtype.name == 'category':
                rfm_df[col] = rfm_df[col].astype(float)
        
        radar_df = rfm_df.groupby('customer_segment').agg({
            'r_score': 'mean',
            'f_score': 'mean',
            'm_score': 'mean'
        }).reset_index()
        
        # 创建雷达图
        fig2 = go.Figure()
        
        for segment in radar_df['customer_segment'].unique():
            segment_data = radar_df[radar_df['customer_segment'] == segment]
            fig2.add_trace(go.Scatterpolar(
                r=[segment_data['r_score'].values[0], 
                   segment_data['f_score'].values[0], 
                   segment_data['m_score'].values[0]],
                theta=['最近消费(R)', '消费频率(F)', '消费金额(M)'],
                fill='toself',
                name=segment
            ))
        
        fig2.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 5]
                )),
            showlegend=True,
            title="客户分群RFM特征雷达图"
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    except Exception as e:
        st.error(f"创建雷达图时发生错误: {e}")
    
    # 分析各群体的消费行为和特征
    st.subheader("客户群体特征分析")
    
    # 合并更多客户特征
    segment_analysis = rfm_df.merge(
        customers_df[['customer_id', 'age', 'gender', 'region', 'income', 'preferred_payment', 'preferred_device']], 
        on='customer_id', 
        how='left'
    )
    
    # 按分群和区域分析
    try:
        if 'region' in segment_analysis.columns:
            region_segment = segment_analysis.groupby(['customer_segment', 'region']).size().reset_index()
            region_segment.columns = ['客户分群', '区域', '客户数量']
            
            fig3 = px.bar(region_segment, x='区域', y='客户数量', color='客户分群', 
                         barmode='group', 
                         title='各区域客户分群分布')
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.warning("数据中缺少'region'列，无法进行区域分析")
    except Exception as e:
        st.error(f"区域分析出错: {e}")
    
    # 按分群和性别分析
    try:
        if 'gender' in segment_analysis.columns:
            gender_segment = segment_analysis.groupby(['customer_segment', 'gender']).size().reset_index()
            gender_segment.columns = ['客户分群', '性别', '客户数量']
            
            fig4 = px.bar(gender_segment, x='性别', y='客户数量', color='客户分群',
                         barmode='group',
                         title='各性别的客户分群分布')
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.warning("数据中缺少'gender'列，无法进行性别分析")
    except Exception as e:
        st.error(f"性别分析出错: {e}")
    
    # 分析顶级价值客户
    st.subheader("顶级价值客户特征")
    
    top_customers = segment_analysis[segment_analysis['customer_segment'] == '顶级价值客户']
    
    # 顶级客户年龄分布
    fig5 = px.histogram(top_customers, x='age', 
                       title='顶级价值客户年龄分布',
                       labels={'age': '年龄', 'count': '客户数量'},
                       nbins=20)
    st.plotly_chart(fig5, use_container_width=True)
    
    # 按收入分析顶级客户
    if 'income' in top_customers.columns:
        fig6 = px.box(segment_analysis, x='customer_segment', y='income', 
                     title='各客户群收入分布',
                     labels={'customer_segment': '客户分群', 'income': '收入'})
        st.plotly_chart(fig6, use_container_width=True)
    
    # 营销建议
    st.subheader("客户分群营销建议")
    
    st.markdown("""
    ### 针对各客户群的营销策略建议：
    
    #### 顶级价值客户
    - **保持关系**: 提供VIP服务和专属优惠
    - **交叉销售**: 推荐高价值相关产品
    - **客户忠诚度计划**: 提供特别奖励和早期访问新产品的机会
    
    #### 高价值客户
    - **增加消费**: 提供数量折扣和捆绑优惠
    - **提高忠诚度**: 升级会员等级的激励措施
    - **个性化推荐**: 基于其购买历史的推荐
    
    #### 一般价值客户
    - **提高购买频率**: 限时优惠和季节性促销
    - **增加客单价**: 推荐中高价位产品
    - **电子邮件营销**: 定期推送新品和促销信息
    
    #### 低价值客户
    - **重新激活**: 为长期未活动的客户提供特别折扣
    - **提高参与度**: 通过社交媒体和内容营销增加互动
    - **了解需求**: 发送调查了解其需求和偏好
    """)

def perform_kmeans_clustering(data):
    """
    使用K-means聚类进行客户细分
    
    Args:
        data (dict): 包含所有数据集的字典
    """
    st.subheader("K-means客户聚类分析")
    
    st.write("""
    K-means聚类是一种无监督学习算法，可以根据客户的多维特征将客户分成不同的群体。
    与RFM分析不同，K-means可以考虑更多的客户特征。
    """)
    
    # 准备数据
    customers_df = data["customers"]
    transactions_df = data["transactions"]
    
    # 合并交易数据，计算每个客户的购买行为
    customer_purchase = transactions_df.groupby('customer_id').agg({
        'transaction_id': 'nunique',  # 购买次数
        'total_amount': 'sum',  # 总消费金额
        'quantity': 'sum',  # 总购买数量
        'date': 'max'  # 最近购买日期
    }).reset_index()
    
    customer_purchase.columns = ['customer_id', 'purchase_count', 'total_spend', 'total_items', 'last_purchase']
    
    # 计算最近购买天数
    customer_purchase['last_purchase'] = pd.to_datetime(customer_purchase['last_purchase'])
    customer_purchase['recency'] = (pd.to_datetime('today') - customer_purchase['last_purchase']).dt.days
    
    # 计算平均订单金额
    customer_purchase['avg_order_value'] = customer_purchase['total_spend'] / customer_purchase['purchase_count']
    
    # 合并客户信息
    clustering_data = customer_purchase.merge(
        customers_df[['customer_id', 'age', 'gender', 'region', 'income', 'registration_date']], 
        on='customer_id', 
        how='left'
    )
    
    # 处理收入字段 - 清理货币符号和K/M等后缀
    try:
        # 如果income是字符串类型，进行清理
        if clustering_data['income'].dtype == 'object':
            # 移除货币符号($)
            clustering_data['income'] = clustering_data['income'].astype(str).str.replace('$', '')
            # 处理K/M后缀
            clustering_data['income'] = clustering_data['income'].apply(lambda x: 
                float(x.replace('K', '')) * 1000 if 'K' in str(x) 
                else (float(x.replace('M', '')) * 1000000 if 'M' in str(x) 
                     else float(x) if str(x).replace('.', '', 1).isdigit() else 0))
    except Exception as e:
        st.warning(f"处理收入数据时出错: {e}")
        # 遇到错误时，将income设为0
        clustering_data['income'] = 0
    
    # 处理缺失值
    clustering_data = clustering_data.fillna({
        'age': clustering_data['age'].median(),
        'income': clustering_data['income'].median()
    })
    
    # 计算客户的忠诚度（注册时间）
    clustering_data['registration_date'] = pd.to_datetime(clustering_data['registration_date'])
    clustering_data['loyalty_days'] = (pd.to_datetime('today') - clustering_data['registration_date']).dt.days
    
    # 准备聚类特征
    # 允许用户选择要包含的特征
    st.subheader("选择用于聚类的特征")
    
    clustering_features = st.multiselect(
        "选择要包含在聚类分析中的特征",
        ['recency', 'purchase_count', 'total_spend', 'avg_order_value', 'age', 'income', 'loyalty_days', 'total_items'],
        default=['recency', 'purchase_count', 'total_spend', 'age']
    )
    
    if not clustering_features:
        st.error("请至少选择一个特征进行聚类分析。")
        return
    
    # 选择聚类数量
    n_clusters = st.slider("选择客户群体数量", min_value=2, max_value=10, value=4)
    
    # 准备特征数据
    X = clustering_data[clustering_features].copy()
    
    # 标准化特征
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 执行K-means聚类
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    clustering_data['cluster'] = kmeans.fit_predict(X_scaled)
    
    # 显示聚类结果
    st.subheader("K-means聚类结果")
    
    # 聚类分布
    cluster_counts = clustering_data['cluster'].value_counts().reset_index()
    cluster_counts.columns = ['聚类', '客户数量']
    
    fig1 = px.pie(cluster_counts, values='客户数量', names='聚类', 
                 title='聚类分布',
                 color_discrete_sequence=px.colors.qualitative.Set1)
    st.plotly_chart(fig1, use_container_width=True)
    
    # 显示各聚类的特征
    cluster_characteristics = clustering_data.groupby('cluster')[clustering_features].mean().reset_index()
    
    st.write("各聚类的平均特征：")
    st.dataframe(cluster_characteristics)
    
    # 使用雷达图显示聚类特征
    st.subheader("聚类特征对比")
    
    # 准备雷达图数据
    radar_data = cluster_characteristics.copy()
    
    # 标准化雷达图数据，使其范围在0-1之间
    for feature in clustering_features:
        radar_data[feature] = (radar_data[feature] - radar_data[feature].min()) / (radar_data[feature].max() - radar_data[feature].min())
    
    # 创建雷达图
    fig2 = go.Figure()
    
    for cluster in radar_data['cluster'].unique():
        cluster_data = radar_data[radar_data['cluster'] == cluster]
        fig2.add_trace(go.Scatterpolar(
            r=cluster_data[clustering_features].values[0],
            theta=clustering_features,
            fill='toself',
            name=f'聚类 {cluster}'
        ))
    
    fig2.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True,
        title="聚类特征雷达图"
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # 使用PCA降维并可视化聚类
    st.subheader("聚类可视化 (PCA降维)")
    
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    
    pca_df = pd.DataFrame(X_pca, columns=['PCA1', 'PCA2'])
    pca_df['cluster'] = clustering_data['cluster']
    
    fig3 = px.scatter(pca_df, x='PCA1', y='PCA2', color='cluster',
                     title='客户聚类PCA可视化',
                     labels={'PCA1': '主成分1', 'PCA2': '主成分2', 'cluster': '聚类'},
                     color_discrete_sequence=px.colors.qualitative.Set1)
    
    st.plotly_chart(fig3, use_container_width=True)
    
    # 分析各聚类的其他特征
    st.subheader("聚类的额外特征分析")
    
    # 合并更多客户特征
    extended_cluster_data = clustering_data.merge(
        customers_df[['customer_id', 'gender', 'region', 'preferred_payment', 'preferred_device', 'segment']], 
        on='customer_id', 
        how='left'
    )
    
    # 按聚类和原始客户细分分析
    segment_cluster = extended_cluster_data.groupby(['cluster', 'segment']).size().reset_index()
    segment_cluster.columns = ['聚类', '客户细分', '客户数量']
    
    fig4 = px.bar(segment_cluster, x='聚类', y='客户数量', color='客户细分', 
                 barmode='stack', 
                 title='聚类与原始客户细分的关系')
    st.plotly_chart(fig4, use_container_width=True)
    
    # 按集群和区域分析
    try:
        if 'region' in extended_cluster_data.columns:
            region_cluster = extended_cluster_data.groupby(['cluster', 'region']).size().reset_index()
            region_cluster.columns = ['集群', '区域', '客户数量']
            
            fig3 = px.bar(region_cluster, x='区域', y='客户数量', color='集群',
                        barmode='group',
                        title='各区域客户集群分布')
            
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.warning("数据中缺少'region'列，无法进行区域分析")
    except Exception as e:
        st.error(f"区域分析出错: {e}")
        
    # 按集群和性别分析
    try:
        if 'gender' in extended_cluster_data.columns:
            gender_cluster = extended_cluster_data.groupby(['cluster', 'gender']).size().reset_index()
            gender_cluster.columns = ['集群', '性别', '客户数量']
            
            fig4 = px.bar(gender_cluster, x='性别', y='客户数量', color='集群',
                        barmode='group',
                        title='各性别客户集群分布')
            
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.warning("数据中缺少'gender'列，无法进行性别分析")
    except Exception as e:
        st.error(f"性别分析出错: {e}")
    
    # 聚类解释和营销建议
    st.subheader("聚类解释和营销建议")
    
    # 根据特征自动生成聚类描述
    cluster_descriptions = []
    
    for cluster in range(n_clusters):
        cluster_data = cluster_characteristics[cluster_characteristics['cluster'] == cluster]
        
        description = f"### 聚类 {cluster} 特征:\n\n"
        
        # 分析消费金额
        spend_rank = cluster_characteristics['total_spend'].rank(ascending=False)
        spend_position = spend_rank[cluster_characteristics['cluster'] == cluster].values[0]
        if spend_position == 1:
            description += "- **高消费客户**: 总消费金额在所有群体中最高\n"
        elif spend_position <= n_clusters / 2:
            description += "- **中高消费客户**: 总消费金额较高\n"
        else:
            description += "- **低消费客户**: 总消费金额较低\n"
        
        # 分析购买频率
        freq_rank = cluster_characteristics['purchase_count'].rank(ascending=False)
        freq_position = freq_rank[cluster_characteristics['cluster'] == cluster].values[0]
        if freq_position == 1:
            description += "- **高频率购买者**: 购买次数在所有群体中最多\n"
        elif freq_position <= n_clusters / 2:
            description += "- **中频率购买者**: 购买次数较多\n"
        else:
            description += "- **低频率购买者**: 购买次数较少\n"
        
        # 分析最近购买
        recency_rank = cluster_characteristics['recency'].rank(ascending=True)  # 较小值表示更近的购买
        recency_position = recency_rank[cluster_characteristics['cluster'] == cluster].values[0]
        if recency_position == 1:
            description += "- **活跃客户**: 最近购买时间最近\n"
        elif recency_position <= n_clusters / 2:
            description += "- **中度活跃客户**: 最近购买时间较近\n"
        else:
            description += "- **不活跃客户**: 长时间未购买\n"
        
        # 添加营销建议
        description += "\n### 营销建议:\n\n"
        
        # 根据客户特征提供建议
        if spend_position <= n_clusters / 2 and freq_position <= n_clusters / 2:
            description += "- **维护关系**: 这是高价值客户群体，应提供VIP服务和专属优惠\n"
            description += "- **交叉销售**: 推荐高价值相关产品\n"
            description += "- **忠诚度计划**: 提供特别奖励和早期访问新产品的机会\n"
        elif spend_position <= n_clusters / 2 and freq_position > n_clusters / 2:
            description += "- **提高购买频率**: 推出定期购买激励计划\n"
            description += "- **个性化推荐**: 基于其购买历史的推荐\n"
            description += "- **便捷购买**: 简化购买流程，提供一键复购选项\n"
        elif spend_position > n_clusters / 2 and freq_position <= n_clusters / 2:
            description += "- **提高客单价**: 推荐中高价位产品\n"
            description += "- **捆绑销售**: 提供相关产品的捆绑优惠\n"
            description += "- **质量升级**: 引导客户尝试更高品质的产品\n"
        else:
            description += "- **重新激活**: 为长期未活动的客户提供特别折扣\n"
            description += "- **教育客户**: 提供产品价值和使用教程\n"
            description += "- **简化体验**: 降低购买门槛，提供试用机会\n"
        
        cluster_descriptions.append(description)
    
    # 显示聚类描述和建议
    for description in cluster_descriptions:
        st.markdown(description)

def perform_behavioral_analysis(data):
    """
    基于消费行为的客户细分分析
    
    Args:
        data (dict): 包含所有数据集的字典
    """
    st.subheader("消费行为客户细分分析")
    
    st.write("""
    消费行为分析从多个角度考察客户的购买模式，包括：
    - 消费品类偏好
    - 购买时段分布
    - 支付方式选择
    - 设备使用偏好
    - 优惠券使用情况
    
    通过这些维度，我们可以更全面地了解客户行为模式。
    """)
    
    # 准备数据
    customers_df = data["customers"]
    transactions_df = data["transactions"]
    products_df = data["products"]
    
    # 合并数据
    merged_data = transactions_df.merge(
        customers_df[['customer_id', 'segment', 'region', 'gender', 'age']], 
        on='customer_id', 
        how='left'
    )
    
    # 添加产品类别信息
    if 'category' in products_df.columns:
        product_categories = products_df[['product_id', 'category', 'subcategory']]
        merged_data = merged_data.merge(product_categories, on='product_id', how='left')
    
    # 分析品类偏好
    st.subheader("客户品类偏好分析")
    
    # 按客户细分和产品类别分析
    if 'product_category' in merged_data.columns:
        segment_category = merged_data.groupby(['segment', 'product_category'])['total_amount'].sum().reset_index()
        
        fig1 = px.bar(segment_category, x='segment', y='total_amount', color='product_category',
                     title='各客户细分的品类偏好',
                     labels={'segment': '客户细分', 'total_amount': '消费金额', 'product_category': '产品类别'})
        
        st.plotly_chart(fig1, use_container_width=True)
    
    # 分析购买时段分布
    st.subheader("购买时段分析")
    
    # 提取小时信息
    if 'time' in merged_data.columns:
        merged_data['hour'] = pd.to_datetime(merged_data['time']).dt.hour
        
        # 定义时段
        def get_time_period(hour):
            if 5 <= hour < 12:
                return '上午 (5-12点)'
            elif 12 <= hour < 18:
                return '下午 (12-18点)'
            elif 18 <= hour < 22:
                return '晚上 (18-22点)'
            else:
                return '夜间 (22-5点)'
        
        merged_data['time_period'] = merged_data['hour'].apply(get_time_period)
        
        # 按客户细分和时段分析
        segment_time = merged_data.groupby(['segment', 'time_period']).size().reset_index()
        segment_time.columns = ['客户细分', '时段', '订单数量']
        
        fig2 = px.bar(segment_time, x='客户细分', y='订单数量', color='时段',
                     title='各客户细分的购买时段分布',
                     barmode='group')
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # 分析支付方式
    st.subheader("支付方式偏好分析")
    
    if 'payment_method' in merged_data.columns:
        # 按客户细分和支付方式分析
        segment_payment = merged_data.groupby(['segment', 'payment_method']).size().reset_index()
        segment_payment.columns = ['客户细分', '支付方式', '订单数量']
        
        fig3 = px.bar(segment_payment, x='客户细分', y='订单数量', color='支付方式',
                     title='各客户细分的支付方式偏好',
                     barmode='stack')
        
        st.plotly_chart(fig3, use_container_width=True)
    
    # 分析设备使用
    st.subheader("设备使用偏好分析")
    
    if 'device' in merged_data.columns:
        # 按客户细分和设备分析
        segment_device = merged_data.groupby(['segment', 'device']).size().reset_index()
        segment_device.columns = ['客户细分', '设备', '订单数量']
        
        fig4 = px.bar(segment_device, x='客户细分', y='订单数量', color='设备',
                     title='各客户细分的设备使用偏好',
                     barmode='stack')
        
        st.plotly_chart(fig4, use_container_width=True)
    
    # 分析优惠券使用
    st.subheader("优惠券使用分析")
    
    if 'coupon_used' in merged_data.columns:
        # 计算各细分的优惠券使用率
        coupon_usage = merged_data.groupby('segment')['coupon_used'].mean().reset_index()
        coupon_usage.columns = ['客户细分', '优惠券使用率']
        
        fig5 = px.bar(coupon_usage, x='客户细分', y='优惠券使用率',
                     title='各客户细分的优惠券使用率',
                     labels={'优惠券使用率': '使用率 (0-1)'})
        
        st.plotly_chart(fig5, use_container_width=True)
        
        # 分析使用优惠券的订单金额变化
        coupon_amount = merged_data.groupby(['segment', 'coupon_used'])['total_amount'].mean().reset_index()
        coupon_amount.columns = ['客户细分', '是否使用优惠券', '平均订单金额']
        
        fig6 = px.bar(coupon_amount, x='客户细分', y='平均订单金额', color='是否使用优惠券',
                     title='优惠券对订单金额的影响',
                     labels={'平均订单金额': '金额', '是否使用优惠券': '优惠券使用'},
                     barmode='group')
        
        st.plotly_chart(fig6, use_container_width=True)
    
    # 行为画像总结
    st.subheader("客户行为画像总结")
    
    # 处理customers_df数据，确保类型正确
    try:
        # 确保segment是分类变量
        if 'segment' not in customers_df.columns:
            st.error("数据中缺少'segment'列，无法生成客户行为画像")
            return
            
        # 确保数值列是数值类型
        if 'age' in customers_df.columns and customers_df['age'].dtype == 'object':
            try:
                customers_df['age'] = pd.to_numeric(customers_df['age'], errors='coerce')
            except:
                customers_df['age'] = 0
                
        # 处理收入字段
        if 'income' in customers_df.columns and customers_df['income'].dtype == 'object':
            try:
                # 移除货币符号($)
                customers_df['income'] = customers_df['income'].astype(str).str.replace('$', '')
                # 处理K/M后缀
                customers_df['income'] = customers_df['income'].apply(lambda x: 
                    float(x.replace('K', '')) * 1000 if 'K' in str(x) 
                    else (float(x.replace('M', '')) * 1000000 if 'M' in str(x) 
                         else float(x) if str(x).replace('.', '', 1).isdigit() else 0))
            except:
                customers_df['income'] = 0
        
        # 获取各细分的基本信息
        segment_summary = customers_df.groupby('segment').agg({
            'customer_id': 'count',
            'age': 'mean',
            'income': 'mean'
        }).reset_index()
        
        segment_summary.columns = ['客户细分', '客户数量', '平均年龄', '平均收入']
        
        st.write("各客户细分的基本信息：")
        st.dataframe(segment_summary)
    except Exception as e:
        st.error(f"生成客户行为画像时出错: {e}")
    
    # 自动生成客户画像和营销建议
    st.subheader("客户画像和营销建议")
    
    # 获取客户细分列表
    segments = customers_df['segment'].unique()
    
    for segment in segments:
        st.markdown(f"### {segment}类客户")
        
        # 提取该细分的数据
        segment_data = merged_data[merged_data['segment'] == segment]
        
        # 获取该细分的主要特征
        segment_info = customers_df[customers_df['segment'] == segment]
        
        # 计算该细分的特征
        avg_age = segment_info['age'].mean()
        top_regions = segment_info['region'].value_counts().head(2).index.tolist()
        top_devices = segment_data['device'].value_counts().head(1).index.tolist() if 'device' in segment_data.columns else []
        top_payments = segment_data['payment_method'].value_counts().head(2).index.tolist() if 'payment_method' in segment_data.columns else []
        top_categories = segment_data['product_category'].value_counts().head(3).index.tolist() if 'product_category' in segment_data.columns else []
        
        # 构建客户画像
        portrait = f"""
        #### 客户画像:
        - **平均年龄**: {avg_age:.1f}岁
        - **主要区域**: {', '.join(top_regions)}
        - **设备偏好**: {', '.join(top_devices) if top_devices else '无明显偏好'}
        - **支付偏好**: {', '.join(top_payments) if top_payments else '无明显偏好'}
        - **品类偏好**: {', '.join(top_categories) if top_categories else '无明显偏好'}
        """
        
        st.markdown(portrait)
        
        # 根据客户画像生成营销建议
        marketing_suggestions = """
        #### 营销建议:
        """
        
        if segment == 'VIP':
            marketing_suggestions += """
            - **专属服务**: 提供个人购物顾问和专属客服
            - **早期访问**: 提供新品抢先体验机会
            - **高端活动**: 邀请参与高端品牌活动和VIP晚宴
            - **定制化推荐**: 基于其购买历史提供高度个性化的推荐
            """
        elif segment == 'Loyal':
            marketing_suggestions += """
            - **忠诚度奖励**: 提供累积积分和阶梯式奖励
            - **会员专享**: 提供会员专享折扣和福利
            - **生日特惠**: 在生日月提供特别优惠
            - **推荐计划**: 鼓励推荐新客户并提供奖励
            """
        elif segment == 'New':
            marketing_suggestions += """
            - **欢迎礼包**: 提供首次购物礼包和教程
            - **引导计划**: 帮助了解产品线和服务
            - **试用优惠**: 提供小额试用装和体验装
            - **简化流程**: 确保购物和支付流程简单直观
            """
        elif segment == 'At Risk':
            marketing_suggestions += """
            - **挽回计划**: 提供特别折扣吸引回流
            - **调查反馈**: 了解客户流失原因
            - **产品更新**: 通知产品改进和新功能
            - **个性化邮件**: 发送"我们想念您"类型的沟通
            """
        else:
            marketing_suggestions += """
            - **定期促销**: 提供季节性促销和折扣
            - **交叉销售**: 推荐相关产品和配件
            - **个性化推荐**: 基于浏览和购买历史的推荐
            - **社区参与**: 鼓励参与品牌社区和活动
            """
        
        st.markdown(marketing_suggestions) 