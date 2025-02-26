import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# 添加项目根目录到Python路径，以便导入utils模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import generate_example_data

def show():
    """显示数据可视化页面内容"""
    st.header("数据可视化")
    
    st.markdown("""
    ## 数据可视化概述
    
    数据可视化是将数据转化为图形表示的过程，旨在帮助人们更好地理解数据中的模式、趋势和关系。
    在商业智能中，良好的数据可视化可以帮助决策者快速把握关键信息，发现潜在的业务机会或问题。
    """)
    
    # 生成示例数据
    df = generate_example_data(100)
    
    # 缺失值和异常值处理
    # 确保数据质量以便可视化
    df['价格'] = pd.to_numeric(df['价格'], errors='coerce')
    df['评分'] = pd.to_numeric(df['评分'], errors='coerce')
    
    # 移除极端的异常值以便更好地可视化
    Q1 = df['价格'].quantile(0.01)
    Q3 = df['价格'].quantile(0.99)
    df_clean = df[(df['价格'] >= Q1) & (df['价格'] <= Q3)]
    
    # 可视化类型概述
    st.subheader("常用可视化类型")
    
    tab1, tab2, tab3, tab4 = st.tabs(["基础图表", "多变量分析", "交互式图表", "地理数据"])
    
    # 基础图表选项卡
    with tab1:
        st.markdown("""
        ### 基础图表类型
        
        基础图表适用于展示简单的数据关系和分布：
        
        - **柱状图**：显示不同类别之间的比较
        - **饼图**：显示整体中各部分的比例
        - **折线图**：显示连续数据的变化趋势
        - **散点图**：显示两个变量之间的关系
        - **直方图**：显示数值数据的分布
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("柱状图示例：各类别产品数量")
            category_counts = df['类别'].value_counts()
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(category_counts.index, category_counts.values)
            ax.set_xlabel('产品类别')
            ax.set_ylabel('数量')
            ax.set_title('各类别产品数量')
            st.pyplot(fig)
            
            st.subheader("折线图示例：不同类别的平均价格")
            category_price = df.groupby('类别')['价格'].mean().sort_values()
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(category_price.index, category_price.values, marker='o', linewidth=2)
            ax.set_xlabel('产品类别')
            ax.set_ylabel('平均价格')
            ax.set_title('各类别平均价格')
            plt.xticks(rotation=45)
            st.pyplot(fig)
        
        with col2:
            st.subheader("饼图示例：商店产品占比")
            shop_counts = df['商店'].value_counts()
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.pie(shop_counts.values, labels=shop_counts.index, autopct='%1.1f%%', startangle=90)
            ax.set_title('各商店产品数量占比')
            st.pyplot(fig)
            
            st.subheader("直方图示例：价格分布")
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(df_clean['价格'], bins=20, alpha=0.7)
            ax.set_xlabel('价格')
            ax.set_ylabel('频次')
            ax.set_title('产品价格分布')
            st.pyplot(fig)
    
    # 多变量分析选项卡
    with tab2:
        st.markdown("""
        ### 多变量分析图表
        
        多变量分析图表用于探索两个或多个变量之间的关系：
        
        - **箱线图**：显示数据分布和离群值
        - **热图**：显示变量之间的相关性
        - **分组柱状图**：比较不同类别间的多个指标
        - **气泡图**：在散点图基础上增加第三个维度
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("箱线图示例：各类别价格分布")
            fig = px.box(df_clean, x='类别', y='价格', title='各类别价格分布')
            st.plotly_chart(fig)
            
            # 创建分组数据
            category_shop_price = df.groupby(['类别', '商店'])['价格'].mean().reset_index()
            pivot_data = category_shop_price.pivot(index='类别', columns='商店', values='价格')
            
            st.subheader("热图示例：类别与商店的平均价格关系")
            fig = px.imshow(pivot_data, 
                            labels=dict(x="商店", y="类别", color="平均价格"),
                            title="类别与商店的平均价格热图")
            st.plotly_chart(fig)
        
        with col2:
            st.subheader("分组柱状图示例：各商店不同促销状态的产品数量")
            grouped_counts = df.groupby(['商店', '是否促销']).size().reset_index(name='数量')
            fig = px.bar(grouped_counts, x='商店', y='数量', color='是否促销',
                         barmode='group', title='各商店促销/非促销产品数量')
            st.plotly_chart(fig)
            
            st.subheader("气泡图示例：价格、评分与评论数的关系")
            fig = px.scatter(df_clean, x='价格', y='评分', size='评论数', color='类别',
                             hover_name='产品名称', size_max=50,
                             title='价格、评分与评论数的关系')
            st.plotly_chart(fig)
    
    # 交互式图表选项卡
    with tab3:
        st.markdown("""
        ### 交互式可视化
        
        交互式图表允许用户直接与数据交互，更深入地探索数据：
        
        - **可筛选图表**：允许用户按条件筛选数据
        - **可缩放图表**：允许用户放大特定区域
        - **多层次交互**：提供多维度数据探索
        """)
        
        st.subheader("交互式散点图：价格与评分")
        
        # 添加交互式控件
        category_filter = st.multiselect(
            "选择产品类别",
            options=df['类别'].unique(),
            default=df['类别'].unique()
        )
        
        min_price, max_price = st.slider(
            "价格范围",
            int(df['价格'].min()),
            int(df['价格'].max()),
            (int(df['价格'].min()), int(df['价格'].max()))
        )
        
        # 应用筛选
        filtered_df = df[
            (df['类别'].isin(category_filter)) &
            (df['价格'] >= min_price) &
            (df['价格'] <= max_price)
        ]
        
        # 创建交互式散点图
        fig = px.scatter(
            filtered_df, 
            x='价格', 
            y='评分',
            color='类别',
            size='评论数',
            hover_name='产品名称',
            hover_data=['商店', '是否促销'],
            title='产品价格与评分关系（交互式）'
        )
        
        st.plotly_chart(fig)
        
        st.subheader("交互式柱状图：各商店产品数量与平均评分")
        
        # 聚合数据
        shop_stats = df.groupby('商店').agg({
            '产品ID': 'count',
            '评分': 'mean',
            '价格': 'mean'
        }).reset_index()
        
        shop_stats.columns = ['商店', '产品数量', '平均评分', '平均价格']
        
        # 添加单选按钮以切换显示指标
        metric = st.radio(
            "选择显示指标",
            ['产品数量', '平均评分', '平均价格'],
            horizontal=True
        )
        
        # 创建动态柱状图
        fig = px.bar(
            shop_stats,
            x='商店',
            y=metric,
            color='商店',
            title=f'各商店的{metric}'
        )
        
        st.plotly_chart(fig)
    
    # 地理数据选项卡
    with tab4:
        st.markdown("""
        ### 地理数据可视化
        
        地理数据可视化用于展示与地理位置相关的数据：
        
        - **地图标记**：在地图上标记特定位置
        - **热力图**：显示地理区域上的数据密度
        - **轮廓图**：显示区域数据的分布
        """)
        
        st.info("这里我们使用模拟的中国城市销售数据来演示地理数据可视化")
        
        # 创建模拟的城市销售数据
        chinese_cities = {
            '北京': (39.9042, 116.4074, '华北'),
            '上海': (31.2304, 121.4737, '华东'),
            '广州': (23.1291, 113.2644, '华南'),
            '深圳': (22.5431, 114.0579, '华南'),
            '成都': (30.5723, 104.0665, '西南'),
            '重庆': (29.4316, 106.9123, '西南'),
            '武汉': (30.5928, 114.3055, '华中'),
            '西安': (34.3416, 108.9398, '西北'),
            '南京': (32.0603, 118.7969, '华东'),
            '杭州': (30.2741, 120.1551, '华东'),
            '天津': (39.0842, 117.2009, '华北'),
            '苏州': (31.2990, 120.5853, '华东'),
            '郑州': (34.7466, 113.6253, '华中'),
            '长沙': (28.2282, 112.9388, '华中'),
            '青岛': (36.0671, 120.3826, '华东')
        }
        
        # 生成销售数据
        np.random.seed(42)
        cities = list(chinese_cities.keys())
        sales_data = []
        
        for city in cities:
            lat, lon, region = chinese_cities[city]
            sales = np.random.randint(5000, 50000)
            growth = np.random.uniform(-0.2, 0.5)
            stores = np.random.randint(3, 30)
            
            sales_data.append({
                '城市': city,
                '纬度': lat,
                '经度': lon,
                '地区': region,
                '销售额': sales,
                '增长率': growth,
                '门店数': stores
            })
        
        df_cities = pd.DataFrame(sales_data)
        
        st.subheader("城市销售数据表")
        st.dataframe(df_cities[['城市', '地区', '销售额', '增长率', '门店数']])
        
        st.subheader("地图标记：各城市销售额")
        
        fig = px.scatter_mapbox(
            df_cities, 
            lat='纬度', 
            lon='经度', 
            color='地区',
            size='销售额',
            hover_name='城市',
            hover_data=['销售额', '增长率', '门店数'],
            zoom=3,
            title='各城市销售额地理分布'
        )
        
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})
        
        st.plotly_chart(fig)
        
        st.subheader("地区销售额分布")
        region_sales = df_cities.groupby('地区')['销售额'].sum().reset_index()
        
        fig = px.pie(
            region_sales,
            values='销售额',
            names='地区',
            title='各地区销售额分布'
        )
        
        st.plotly_chart(fig)
    
    # 数据可视化最佳实践
    st.header("数据可视化最佳实践")
    
    st.markdown("""
    ### 选择合适的图表类型
    
    不同的数据关系适合不同的可视化方式：
    
    1. **比较不同类别**：柱状图、条形图、雷达图
    2. **显示组成部分**：饼图、堆叠柱状图、树状图
    3. **显示分布情况**：直方图、密度图、箱线图
    4. **分析趋势变化**：折线图、面积图
    5. **研究相关性**：散点图、气泡图、热图
    6. **分析地理数据**：各类地图可视化
    
    ### 视觉设计原则
    
    * **简洁明了**：去除无关视觉元素，突出重要信息
    * **色彩合理**：使用对比色突出重点，考虑色盲友好
    * **标签清晰**：添加适当的标题、轴标签和图例
    * **比例一致**：保持数据比例的一致性，避免视觉误导
    * **交互增强**：适当添加交互元素，提升用户体验
    
    ### 常见错误
    
    * 使用不恰当的图表类型（如对时间序列数据使用饼图）
    * 图表过于复杂，信息过载
    * 色彩使用过度鲜艳或不协调
    * 缺少必要的上下文和标签
    * 不考虑受众需求和理解能力
    """)
    
    # 案例分析
    st.header("商业案例分析")
    
    st.markdown("""
    ### 销售数据分析案例
    
    以下是一个综合销售数据分析的示例，结合多种可视化方法来分析产品销售情况。
    """)
    
    # 销售数据分析
    # 为每个产品生成模拟的月度销售数据
    months = ['1月', '2月', '3月', '4月', '5月', '6月', 
              '7月', '8月', '9月', '10月', '11月', '12月']
    
    # 选择几个主要类别进行分析
    main_categories = df['类别'].value_counts().nlargest(3).index.tolist()
    
    # 生成月度销售数据
    np.random.seed(42)
    monthly_sales = []
    
    for category in main_categories:
        category_products = df[df['类别'] == category]
        
        for _, product in category_products.iterrows():
            # 生成基础销量
            base_sales = np.random.randint(50, 500)
            
            # 季节性模式：第一和第四季度销量较高
            seasonal_pattern = [1.2, 0.9, 0.8, 0.9, 1.0, 1.1, 1.2, 1.1, 1.0, 1.1, 1.2, 1.5]
            
            # 生成月度销量
            for i, month in enumerate(months):
                # 添加一些随机波动
                fluctuation = np.random.uniform(0.8, 1.2)
                sales = int(base_sales * seasonal_pattern[i] * fluctuation)
                
                monthly_sales.append({
                    '产品ID': product['产品ID'],
                    '产品名称': product['产品名称'],
                    '类别': category,
                    '月份': month,
                    '销量': sales,
                    '收入': sales * product['价格']
                })
    
    df_monthly = pd.DataFrame(monthly_sales)
    
    # 按类别和月份聚合数据
    category_monthly = df_monthly.groupby(['类别', '月份']).agg({
        '销量': 'sum',
        '收入': 'sum'
    }).reset_index()
    
    # 确保月份顺序正确
    month_order = {month: i for i, month in enumerate(months)}
    category_monthly['月份序号'] = category_monthly['月份'].map(month_order)
    category_monthly = category_monthly.sort_values(['类别', '月份序号'])
    
    # 可视化月度销售趋势
    st.subheader("各类别月度销售趋势")
    
    fig = px.line(
        category_monthly, 
        x='月份', 
        y='销量', 
        color='类别',
        markers=True,
        title='各类别月度销量趋势',
        category_orders={'月份': months}
    )
    
    st.plotly_chart(fig)
    
    # 各类别销售占比
    st.subheader("各类别销售收入占比")
    
    category_total = df_monthly.groupby('类别').agg({
        '收入': 'sum'
    }).reset_index()
    
    fig = px.pie(
        category_total,
        values='收入',
        names='类别',
        title='各类别销售收入占比'
    )
    
    st.plotly_chart(fig)
    
    # 热销产品分析
    st.subheader("热销产品TOP 10")
    
    product_sales = df_monthly.groupby(['产品ID', '产品名称', '类别']).agg({
        '销量': 'sum',
        '收入': 'sum'
    }).reset_index()
    
    top_products = product_sales.sort_values('收入', ascending=False).head(10)
    
    fig = px.bar(
        top_products,
        x='产品名称',
        y='收入',
        color='类别',
        title='销售收入最高的10个产品',
        text='收入'
    )
    
    fig.update_traces(texttemplate='%{text:.0f}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    
    st.plotly_chart(fig)
    
    # 总结见解
    st.header("数据可视化见解")
    
    st.markdown("""
    通过对数据的可视化分析，我们可以得出以下商业见解：
    
    1. **季节性趋势**：各类别产品销量在1月和12月都有明显的增长，表明节假日效应对销售有显著影响。
    
    2. **类别表现**：从收入占比来看，不同产品类别之间存在显著差异，管理层可以考虑优化产品结构。
    
    3. **热销产品**：TOP 10产品贡献了大量收入，应重点关注这些产品的库存和促销策略。
    
    4. **区域分布**：销售额在不同地区分布不均，可以考虑针对低销售区域制定专门的营销策略。
    
    5. **价格与评分关系**：从散点图分析可见，价格与评分之间并无明显线性关系，表明消费者更关注产品价值而非单纯的价格。
    
    这些见解可以帮助企业优化产品组合、调整定价策略、改进营销方案，从而提升整体业绩。
    """)
    
    # 参考资源
    st.subheader("扩展资源")
    
    st.markdown("""
    - [Matplotlib 文档](https://matplotlib.org/)
    - [Plotly 文档](https://plotly.com/python/)
    - [Seaborn 文档](https://seaborn.pydata.org/)
    - [Streamlit 可视化指南](https://docs.streamlit.io/library/api-reference/charts)
    - [数据可视化实践指南](https://www.tableau.com/learn/articles/data-visualization-tips)
    """) 