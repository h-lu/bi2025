import streamlit as st
import os
import sys
import pandas as pd
import time

# 导入模块
from modules.data_loader import load_data
from modules.data_cleaner import clean_data
from modules.data_visualizer import create_dashboard
from modules.customer_segmentation import perform_customer_segmentation
from modules.marketing_analysis import analyze_marketing
from modules.sales_forecasting import forecast_sales
from modules.utils import display_dataset_info, check_data_generated

# 页面配置已经在run_app.py中设置，此处不再重复设置

# 主函数
def main():
    # 侧边栏
    st.sidebar.title("GlobalMart商务智能分析平台")
    st.sidebar.image("https://img.icons8.com/color/96/000000/store-front.png", width=100)
    
    # 检查数据是否已生成
    if not check_data_generated():
        st.warning("数据文件不存在。请先运行 generate_ecommerce_data.py 生成数据。")
        if st.button("生成示例数据"):
            with st.spinner("正在生成数据，请稍候..."):
                import subprocess
                subprocess.run([sys.executable, "generate_ecommerce_data.py"])
                st.success("数据生成完成！")
                st.rerun()
        return
    
    # 导航菜单
    menu = st.sidebar.selectbox(
        "分析模块",
        ["项目介绍", "数据探索", "数据清理", "数据可视化仪表盘", "客户细分分析", "营销效果分析", "销售预测"]
    )
    
    # 数据加载（仅在需要时加载）
    if menu != "项目介绍":
        data = load_data()
        if not data:
            st.error("无法加载数据。请确保数据文件存在。")
            return
    
    # 根据选择显示不同页面
    if menu == "项目介绍":
        display_intro()
    elif menu == "数据探索":
        display_data_exploration(data)
    elif menu == "数据清理":
        display_data_cleaning(data)
    elif menu == "数据可视化仪表盘":
        display_dashboard(data)
    elif menu == "客户细分分析":
        display_customer_segmentation(data)
    elif menu == "营销效果分析":
        display_marketing_analysis(data)
    elif menu == "销售预测":
        display_sales_forecasting(data)

# 项目介绍页面
def display_intro():
    st.title("GlobalMart电子商务平台数据分析项目")
    
    st.markdown("""
    ## 项目背景
    
    GlobalMart是一家综合性电子商务平台，销售各类产品，包括电子产品、服装、家居用品等。
    公司面临日益激烈的市场竞争，希望通过数据分析提升业务表现，特别是：
    
    - 更好地理解客户行为和需求
    - 优化营销策略和预算分配
    - 改进库存管理和销售预测
    
    本项目使用GlobalMart的模拟数据集，展示如何应用商务智能技术解决这些业务问题。
    """)
    
    st.markdown("""
    ## 模块介绍
    
    本平台包含以下分析模块：
    
    1. **数据探索**：查看原始数据，了解数据结构和特征
    2. **数据清理**：处理缺失值、异常值和格式问题
    3. **数据可视化仪表盘**：通过图表直观展示数据洞察
    4. **客户细分分析**：基于RFM模型和聚类分析识别客户群体
    5. **营销效果分析**：评估不同营销渠道和活动的ROI
    6. **销售预测**：基于历史数据预测未来销售趋势
    """)
    
    # 添加AI辅助学习指南
    st.markdown("""
    ## AI辅助学习指南
    """)
    
    st.info("""
    ### 🤖 如何在商务智能分析中使用AI
    
    本平台旨在帮助您学习如何结合AI工具进行商务智能分析，培养数据驱动决策能力。每个分析模块都配备了专门的AI辅助学习指南，以下是整体使用建议：
    
    **1. 建立有效的AI协作工作流**
    
    有效的AI辅助分析遵循以下工作流：
    - **问题定义** → **数据分析** → **结果解释** → **战略建议** → **实施方案**
    
    **2. AI辅助分析的最佳实践**
    
    - **先思考后询问**：先形成自己的分析和假设，再与AI讨论
    - **具体而精准**：提供具体上下文和数据，提出精确问题
    - **批判性思考**：评估AI建议的合理性和适用性
    - **迭代改进**：基于AI反馈完善分析，形成对话循环
    
    **3. 课程应用建议**
    
    - 将平台视为学习实验室，尝试不同分析方法
    - 记录您与AI的对话和分析过程，作为学习日志
    - 比较不同AI工具(如ChatGPT、Claude、Bard等)的分析结果差异
    - 将您的分析结果与同学分享，讨论不同的分析角度
    
    **4. 模拟实际业务场景**
    
    尝试扮演不同角色进行分析：
    - 作为**数据分析师**：与AI讨论技术实现和方法选择
    - 作为**业务经理**：与AI讨论分析结果的商业意义
    - 作为**执行官**：与AI讨论战略决策和资源分配
    
    在每个模块中，您会看到具体的AI协作指南，帮助您充分利用人工智能辅助商务分析。
    """)
    
    st.markdown("""
    ## 数据集说明
    
    本项目包含以下模拟数据集：
    
    1. **客户数据**：客户人口统计信息和偏好
    2. **产品数据**：产品目录和属性
    3. **交易数据**：客户购买记录
    4. **营销活动数据**：营销活动记录和效果
    5. **网站流量数据**：客户浏览行为和渠道来源
    
    这些数据经过设计，反映真实电子商务平台的业务特点和挑战。
    """)
    
    st.info("开始使用: 请使用左侧菜单导航到不同的分析模块。")

# 数据探索页面
def display_data_exploration(data):
    st.title("数据探索")
    
    # 添加AI辅助学习指导
    st.info("""
    ### 🤖 AI辅助学习指南：数据探索
    
    **学习目标**：理解数据结构、识别数据特征、发现潜在模式和问题。
    
    **如何与AI合作进行数据探索**：
    1. **提问示例**：
       - "请分析这些客户数据的年龄分布特点及商业意义"
       - "根据这些交易数据，有哪些明显的消费模式？"
       - "这些数据中可能存在哪些数据质量问题？"
    
    2. **使用AI分析数据特征**：将数据统计和图表截图提供给AI，请求解释异常值、分布特点或关联性。
    
    3. **实践建议**：先自行分析数据并形成假设，再与AI讨论，比较您的观察与AI的见解有何不同。
    
    **下一步**：探索完数据后，使用"数据清理"模块处理发现的数据问题。
    """)
    
    # 选择数据集
    dataset = st.selectbox(
        "选择要探索的数据集:",
        ["客户数据", "产品数据", "交易数据", "营销活动数据", "网站流量数据"]
    )
    
    dataset_mapping = {
        "客户数据": data["customers"],
        "产品数据": data["products"],
        "交易数据": data["transactions"],
        "营销活动数据": data["marketing"],
        "网站流量数据": data["traffic"]
    }
    
    df = dataset_mapping[dataset]
    
    # 显示数据集信息
    display_dataset_info(df, dataset)
    
    # 显示原始数据样本
    with st.expander("查看原始数据样本"):
        st.dataframe(df.head(100))
    
    # 数据统计
    with st.expander("查看数据统计信息"):
        st.write("基本统计信息")
        st.dataframe(df.describe())
        
        st.write("缺失值统计")
        missing_data = pd.DataFrame({
            '缺失值数量': df.isnull().sum(),
            '缺失值比例 (%)': (df.isnull().sum() / len(df) * 100).round(2)
        })
        st.dataframe(missing_data)
    
    # 列详情
    with st.expander("查看列详细信息"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("数据类型")
            st.dataframe(pd.DataFrame({
                '数据类型': df.dtypes
            }))
        
        with col2:
            st.write("唯一值数量")
            st.dataframe(pd.DataFrame({
                '唯一值数量': df.nunique()
            }))

# 数据清理页面
def display_data_cleaning(data):
    st.title("数据清理与预处理")
    
    # 添加AI辅助学习指导
    st.info("""
    ### 🤖 AI辅助学习指南：数据清理与预处理
    
    **学习目标**：学习识别和处理数据问题，准备高质量的分析数据集。
    
    **如何与AI合作进行数据清理**：
    1. **提问示例**：
       - "如何处理这些数据中的异常值？它们是否应该被移除？"
       - "这个字段的缺失值应该如何填充才最合理？" 
       - "这些日期格式不一致，如何编写代码统一转换？"
    
    2. **代码生成**：请AI生成数据清理代码，例如：
       - "请编写Pandas代码处理这个数据集中的重复记录"
       - "这个字段有多种表示方式，请生成规范化处理的代码"
    
    3. **验证策略**：讨论如何验证清理结果的有效性，例如：
       - "清理后的数据应该满足哪些业务规则？"
       - "如何确保数据转换没有引入新的错误？"
    
    **实践要点**：数据清理是反复的过程，先处理严重问题，再解决次要问题，记录所有清理步骤。
    """)
    
    # 选择数据集
    dataset = st.selectbox(
        "选择要清理的数据集:",
        ["客户数据", "产品数据", "交易数据", "营销活动数据", "网站流量数据"]
    )
    
    dataset_mapping = {
        "客户数据": ("customers", data["customers"]),
        "产品数据": ("products", data["products"]),
        "交易数据": ("transactions", data["transactions"]),
        "营销活动数据": ("marketing", data["marketing"]),
        "网站流量数据": ("traffic", data["traffic"])
    }
    
    dataset_key, df = dataset_mapping[dataset]
    
    st.write(f"### 原始{dataset}")
    st.dataframe(df.head())
    
    # 数据清理步骤
    st.write("### 数据清理步骤")
    
    # 清理数据
    cleaned_df, cleaning_report = clean_data(df, dataset_key)
    
    # 显示清理报告
    for step, details in cleaning_report.items():
        with st.expander(f"步骤 {step}: {details['title']}"):
            st.write(details['description'])
            if 'before' in details and 'after' in details:
                col1, col2 = st.columns(2)
                with col1:
                    st.write("清理前:")
                    st.dataframe(details['before'])
                with col2:
                    st.write("清理后:")
                    st.dataframe(details['after'])
    
    # 显示清理后的数据
    st.write(f"### 清理后的{dataset}")
    st.dataframe(cleaned_df.head())
    
    # 下载清理后的数据
    csv = cleaned_df.to_csv(index=False)
    st.download_button(
        label=f"下载清理后的{dataset} CSV",
        data=csv,
        file_name=f"cleaned_{dataset_key}.csv",
        mime="text/csv",
    )

# 数据可视化仪表盘页面
def display_dashboard(data):
    st.title("数据可视化仪表盘")
    
    # 添加AI辅助学习指导
    st.info("""
    ### 🤖 AI辅助学习指南：数据可视化
    
    **学习目标**：学习如何通过可视化呈现数据故事，发现数据模式和洞察。
    
    **如何与AI合作进行数据可视化**：
    1. **图表解释与深度解读**：
       - 将可视化结果截图给AI："请分析这个折线图显示的销售趋势，特别关注异常波动原因"
       - "这个散点图显示了哪些客户细分群体，它们的主要特征是什么？"
    
    2. **视觉设计改进**：
       - "如何优化这个图表的配色和布局，使信息更清晰？"
       - "这些数据用什么类型的图表表达更合适？为什么？"
    
    3. **业务洞察提取**：
       - "基于这些可视化结果，我们应该向管理层提出哪些商业建议？"
       - "这些图表中的模式如何帮助我们优化营销策略？"
    
    **技巧**：先描述你从图表中观察到的模式，再请AI补充可能被忽略的见解，最后讨论商业含义。
    """)
    
    # 创建仪表盘
    create_dashboard(data)

# 客户细分分析页面
def display_customer_segmentation(data):
    st.title("客户细分分析")
    
    # 添加AI辅助学习指导
    st.info("""
    ### 🤖 AI辅助学习指南：客户细分分析
    
    **学习目标**：掌握客户细分方法，理解不同客户群体的特征和价值。
    
    **如何与AI合作进行客户细分分析**：
    1. **解释细分结果**：
       - "请解释这些RFM分析结果，各客户群体有什么特点？"
       - "这些K-means聚类发现了哪些不同类型的客户群体？"
       - "为什么这个客户群体的价值比其他群体高？"
    
    2. **细分策略制定**：
       - "对于这个高价值但流失风险高的客户群，应该采取什么挽留策略？"
       - "我们如何提高这个低消费频率客户群的复购率？"
       - "基于这些细分结果，如何设计个性化的营销方案？"
    
    3. **细分方法改进**：
       - "除了RFM和K-means，还有哪些客户细分方法适合这类数据？"
       - "这个聚类的最优K值应该如何确定？"
       - "如何评估这个客户细分模型的业务有效性？"
    
    **实践建议**：细分完成后，为每个群体制定具体的营销策略，并与AI讨论预期效果和可能的改进。
    """)
    
    # 执行客户细分分析
    perform_customer_segmentation(data)

# 营销效果分析页面
def display_marketing_analysis(data):
    st.title("营销效果分析")
    
    # 添加AI辅助学习指导
    st.info("""
    ### 🤖 AI辅助学习指南：营销效果分析
    
    **学习目标**：学习评估营销活动效果，优化营销策略和资源分配。
    
    **如何与AI合作进行营销分析**：
    1. **ROI计算与解释**：
       - "这些渠道的ROI结果说明了什么？为什么会有这样的差异？"
       - "如何解释这个营销活动的低转化率但高客户获取？"
       - "基于历史ROI数据，应该如何调整未来的营销预算？"
    
    2. **多渠道归因分析**：
       - "这些营销渠道间可能存在哪些交互效应？"
       - "如何判断一个渠道的真实贡献，超出最后点击模型的局限？"
       - "设计一个合理的多触点归因模型需要考虑哪些因素？"
    
    3. **营销策略优化**：
       - "基于这些分析，如何重新分配我们的营销预算以最大化ROI？"
       - "哪些客户群体对此类营销活动最敏感，为什么？"
       - "如何设计A/B测试验证这些优化策略的效果？"
    
    **技巧**：结合客户细分结果与营销效果分析，设计针对不同客户群体的差异化营销策略。
    """)
    
    # 执行营销效果分析
    analyze_marketing(data)

# 销售预测页面
def display_sales_forecasting(data):
    st.title("销售预测")
    
    # 添加AI辅助学习指导
    st.info("""
    ### 🤖 AI辅助学习指南：销售预测
    
    **学习目标**：学习时间序列预测方法，了解如何基于历史数据做出科学的业务预测。
    
    **如何与AI合作进行销售预测**：
    1. **预测结果分析**：
       - "这个预测趋势的主要驱动因素可能是什么？"
       - "这些季节性模式与企业的哪些内外部因素相关？"
       - "为什么模型在某些时间点的预测误差较大？"
    
    2. **预测方法优化**：
       - "这种数据模式适合使用哪种预测算法？ARIMA、Prophet还是其他？"
       - "如何优化时间窗口和参数设置以提高预测准确性？"
       - "考虑到这些外部因素，如何改进当前的预测模型？"
    
    3. **业务决策支持**：
       - "基于这些预测结果，应该如何调整库存管理策略？"
       - "销售高峰期前，营销和供应链应当做哪些准备？"
       - "如何利用预测的不确定性区间制定稳健的业务计划？"
    
    **实践要点**：将预测结果与业务目标结合，形成具体的行动建议，并讨论不同情景下的应对策略。
    """)
    
    # 执行销售预测
    forecast_sales(data)

if __name__ == "__main__":
    main() 