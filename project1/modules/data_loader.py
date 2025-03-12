import pandas as pd
import streamlit as st
import os

@st.cache_data(ttl=3600, show_spinner=True)
def load_data():
    """
    加载所有数据集并缓存，避免重复加载
    
    Returns:
        dict: 包含所有数据集的字典
    """
    try:
        # 数据文件路径
        customers_path = "data/customers.csv"
        products_path = "data/products.csv"
        transactions_path = "data/transactions.csv"
        marketing_path = "data/marketing_campaigns.csv"
        traffic_path = "data/website_traffic.csv"
        
        # 检查文件是否存在
        if not all(os.path.exists(path) for path in [customers_path, products_path, transactions_path, marketing_path, traffic_path]):
            st.error("数据文件不存在，请先运行 generate_ecommerce_data.py 生成数据")
            return None
        
        # 加载数据
        with st.spinner("正在加载数据..."):
            # 客户数据
            customers_df = pd.read_csv(customers_path)
            
            # 产品数据
            products_df = pd.read_csv(products_path)
            
            # 交易数据
            transactions_df = pd.read_csv(transactions_path)
            
            # 营销活动数据
            marketing_df = pd.read_csv(marketing_path)
            
            # 网站流量数据
            traffic_df = pd.read_csv(traffic_path)
            
            # 初始数据转换
            # 转换日期列
            for df, date_cols in [
                (customers_df, ['registration_date']),
                (products_df, ['launch_date']),
                (transactions_df, ['date']),
                (marketing_df, ['start_date', 'end_date']),
                (traffic_df, ['date'])
            ]:
                for col in date_cols:
                    if col in df.columns:
                        try:
                            # 尝试多种日期格式
                            df[col] = pd.to_datetime(df[col], errors='coerce')
                        except:
                            pass
            
            # 返回数据集字典
            return {
                "customers": customers_df,
                "products": products_df,
                "transactions": transactions_df,
                "marketing": marketing_df,
                "traffic": traffic_df
            }
    
    except Exception as e:
        st.error(f"加载数据时出错: {str(e)}")
        return None

# 加载单个数据集
def load_single_dataset(dataset_name):
    """
    加载单个数据集
    
    Args:
        dataset_name (str): 数据集名称 ('customers', 'products', 'transactions', 'marketing', 'traffic')
    
    Returns:
        pandas.DataFrame: 加载的数据集
    """
    try:
        file_path = f"data/{dataset_name}.csv"
        if dataset_name == "marketing":
            file_path = "data/marketing_campaigns.csv"
            
        if os.path.exists(file_path):
            return pd.read_csv(file_path)
        else:
            st.error(f"文件 {file_path} 不存在")
            return None
    except Exception as e:
        st.error(f"加载 {dataset_name} 数据时出错: {str(e)}")
        return None 