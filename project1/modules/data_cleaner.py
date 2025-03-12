import pandas as pd
import numpy as np
import streamlit as st

def clean_data(df, dataset_type):
    """
    根据数据集类型进行数据清理
    
    Args:
        df (pd.DataFrame): 要清理的数据集
        dataset_type (str): 数据集类型 (customers, products, transactions, marketing, traffic)
    
    Returns:
        tuple: (清理后的数据集, 清理报告)
    """
    # 创建数据清理报告
    cleaning_report = {}
    
    # 复制数据集以避免修改原始数据
    cleaned_df = df.copy()
    
    # 根据数据集类型调用相应的清理函数
    if dataset_type == 'customers':
        cleaned_df, cleaning_report = clean_customer_data(cleaned_df)
    elif dataset_type == 'products':
        cleaned_df, cleaning_report = clean_product_data(cleaned_df)
    elif dataset_type == 'transactions':
        cleaned_df, cleaning_report = clean_transaction_data(cleaned_df)
    elif dataset_type == 'marketing':
        cleaned_df, cleaning_report = clean_marketing_data(cleaned_df)
    elif dataset_type == 'traffic':
        cleaned_df, cleaning_report = clean_traffic_data(cleaned_df)
    
    return cleaned_df, cleaning_report

def clean_customer_data(df):
    """清理客户数据"""
    report = {}
    df_copy = df.copy()
    
    # 步骤1: 处理客户ID重复问题
    step = 1
    report[step] = {
        'title': '处理重复的客户ID',
        'description': '识别并修复重复的客户ID，确保每个客户只有一个唯一标识符。'
    }
    
    # 记录清理前的数据
    report[step]['before'] = df_copy[df_copy.duplicated(subset=['customer_id'], keep=False)][['customer_id', 'name']].head(10)
    
    # 查找重复的客户ID
    duplicate_ids = df_copy[df_copy.duplicated(subset=['customer_id'], keep=False)]['customer_id'].unique()
    
    # 对重复的ID进行修复
    for dup_id in duplicate_ids:
        # 获取具有重复ID的所有行
        dup_rows = df_copy[df_copy['customer_id'] == dup_id]
        # 保留第一行，修改其他行的ID
        for i, (index, _) in enumerate(dup_rows.iloc[1:].iterrows()):
            df_copy.at[index, 'customer_id'] = f"{dup_id}__{i+1}"
    
    # 记录清理后的数据
    report[step]['after'] = df_copy[df_copy['customer_id'].isin([id for id in duplicate_ids])].head(10)
    
    # 步骤2: 处理年龄异常值
    step = 2
    report[step] = {
        'title': '处理年龄异常值',
        'description': '将异常年龄值(>100岁)替换为空值(NaN)，并用中位数填充缺失的年龄。'
    }
    
    # 记录清理前的数据
    report[step]['before'] = pd.DataFrame({
        '年龄统计': [
            f"最小年龄: {df_copy['age'].min()}",
            f"最大年龄: {df_copy['age'].max()}",
            f"缺失值数量: {df_copy['age'].isna().sum()}",
            f"异常值数量(>100): {len(df_copy[df_copy['age'] > 100])}"
        ]
    })
    
    # 处理异常年龄值(>100)
    df_copy.loc[df_copy['age'] > 100, 'age'] = np.nan
    
    # 使用中位数填充缺失的年龄
    median_age = df_copy['age'].median()
    df_copy['age'] = df_copy['age'].fillna(median_age)
    
    # 记录清理后的数据
    report[step]['after'] = pd.DataFrame({
        '年龄统计': [
            f"最小年龄: {df_copy['age'].min()}",
            f"最大年龄: {df_copy['age'].max()}",
            f"缺失值数量: {df_copy['age'].isna().sum()}",
            f"异常值数量(>100): {len(df_copy[df_copy['age'] > 100])}"
        ]
    })
    
    # 步骤3: 统一收入格式
    step = 3
    report[step] = {
        'title': '统一收入格式',
        'description': '将不同格式的收入值转换为统一的数字格式。'
    }
    
    # 记录清理前的数据
    sample_incomes = df_copy['income'].sample(10).to_dict()
    report[step]['before'] = pd.DataFrame({'收入样本': [f"{k}: {v}" for k, v in sample_incomes.items()]})
    
    # 处理收入格式
    def clean_income(income):
        if pd.isna(income):
            return np.nan
        if isinstance(income, (int, float)):
            return income
        # 处理字符串格式，如"$50K"
        try:
            income_str = str(income).strip()
            if income_str.startswith('$'):
                income_str = income_str[1:]
            if income_str.upper().endswith('K'):
                return float(income_str[:-1]) * 1000
            return float(income_str)
        except:
            return np.nan
    
    df_copy['income'] = df_copy['income'].apply(clean_income)
    
    # 处理异常高收入（根据分位数）
    q3 = df_copy['income'].quantile(0.75)
    iqr = df_copy['income'].quantile(0.75) - df_copy['income'].quantile(0.25)
    upper_bound = q3 + 1.5 * iqr
    df_copy.loc[df_copy['income'] > upper_bound, 'income'] = upper_bound
    
    # 记录清理后的数据
    cleaned_incomes = {k: df_copy.loc[k, 'income'] for k in sample_incomes.keys() if k in df_copy.index}
    report[step]['after'] = pd.DataFrame({'收入样本': [f"{k}: {v}" for k, v in cleaned_incomes.items()]})
    
    # 步骤4: 修复错误的电子邮件格式
    step = 4
    report[step] = {
        'title': '修复错误的电子邮件格式',
        'description': '修复格式不正确的电子邮件地址。'
    }
    
    # 找出不符合电子邮件格式的记录
    import re
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    invalid_emails = df_copy[~df_copy['email'].str.match(email_pattern)]
    
    # 记录清理前的数据
    report[step]['before'] = invalid_emails[['email']].head(10)
    
    # 修复邮箱格式
    def fix_email(email):
        if pd.isna(email):
            return np.nan
        email = str(email).strip()
        if 'at' in email and '@' not in email:
            return email.replace('at', '@')
        if '@' not in email:
            return np.nan
        return email
    
    df_copy['email'] = df_copy['email'].apply(fix_email)
    
    # 记录清理后的数据
    fixed_emails = df_copy.loc[invalid_emails.index][['email']].head(10)
    report[step]['after'] = fixed_emails
    
    return df_copy, report

def clean_product_data(df):
    """清理产品数据"""
    report = {}
    df_copy = df.copy()
    
    # 步骤1: 统一产品ID格式
    step = 1
    report[step] = {
        'title': '统一产品ID格式',
        'description': '将纯数字ID转换为标准格式(PRODxxxxx)。'
    }
    
    # 记录清理前的数据
    non_standard_ids = df_copy[~df_copy['product_id'].str.startswith('PROD')][['product_id']].head(10)
    report[step]['before'] = non_standard_ids
    
    # 统一产品ID格式
    def standardize_product_id(pid):
        if not str(pid).startswith('PROD'):
            return f"PROD{int(pid):05d}"
        return pid
    
    df_copy['product_id'] = df_copy['product_id'].apply(standardize_product_id)
    
    # 记录清理后的数据
    report[step]['after'] = df_copy.loc[non_standard_ids.index][['product_id']]
    
    # 步骤2: 处理缺失的评分
    step = 2
    report[step] = {
        'title': '处理缺失的产品评分',
        'description': '使用基于产品类别的评分均值填充缺失的评分。'
    }
    
    # 记录清理前的数据
    missing_ratings = df_copy[df_copy['rating'].isna()][['product_id', 'name', 'category', 'rating']].head(10)
    report[step]['before'] = missing_ratings
    
    # 计算每个类别的平均评分
    category_avg_rating = df_copy.groupby('category')['rating'].mean()
    
    # 填充缺失评分
    for idx, row in df_copy[df_copy['rating'].isna()].iterrows():
        category = row['category']
        # 如果该类别有平均评分，使用它填充
        if category in category_avg_rating:
            df_copy.at[idx, 'rating'] = category_avg_rating[category]
        else:
            # 否则使用全局平均评分
            df_copy.at[idx, 'rating'] = df_copy['rating'].mean()
    
    # 记录清理后的数据
    report[step]['after'] = df_copy.loc[missing_ratings.index][['product_id', 'name', 'category', 'rating']]
    
    # 步骤3: 填充缺失的重量数据
    step = 3
    report[step] = {
        'title': '填充缺失的产品重量',
        'description': '使用基于产品子类别的重量中位数填充缺失的重量数据。'
    }
    
    # 记录清理前的数据
    missing_weights = df_copy[df_copy['weight_kg'].isna()][['product_id', 'name', 'subcategory', 'weight_kg']].head(10)
    report[step]['before'] = missing_weights
    
    # 计算每个子类别的重量中位数
    subcategory_median_weight = df_copy.groupby('subcategory')['weight_kg'].median()
    
    # 填充缺失重量
    for idx, row in df_copy[df_copy['weight_kg'].isna()].iterrows():
        subcategory = row['subcategory']
        # 如果该子类别有中位数重量，使用它填充
        if subcategory in subcategory_median_weight and not np.isnan(subcategory_median_weight[subcategory]):
            df_copy.at[idx, 'weight_kg'] = subcategory_median_weight[subcategory]
        else:
            # 否则使用全局中位数
            df_copy.at[idx, 'weight_kg'] = df_copy['weight_kg'].median()
    
    # 记录清理后的数据
    report[step]['after'] = df_copy.loc[missing_weights.index][['product_id', 'name', 'subcategory', 'weight_kg']]
    
    return df_copy, report

def clean_transaction_data(df):
    """清理交易数据"""
    report = {}
    df_copy = df.copy()
    
    # 步骤1: 统一交易ID格式
    step = 1
    report[step] = {
        'title': '统一交易ID格式',
        'description': '将不标准的交易ID转换为标准格式(TRXxxxxxx)。'
    }
    
    # 记录清理前的数据
    non_standard_ids = df_copy[~df_copy['transaction_id'].str.startswith('TRX')][['transaction_id']].head(10)
    report[step]['before'] = non_standard_ids
    
    # 统一交易ID格式
    def standardize_transaction_id(tid):
        if not str(tid).startswith('TRX'):
            return f"TRX{int(tid):06d}"
        return tid
    
    df_copy['transaction_id'] = df_copy['transaction_id'].apply(standardize_transaction_id)
    
    # 记录清理后的数据
    report[step]['after'] = df_copy.loc[non_standard_ids.index][['transaction_id']]
    
    # 步骤2: 统一日期格式
    step = 2
    report[step] = {
        'title': '统一日期格式',
        'description': '将各种格式的日期转换为标准格式(YYYY-MM-DD)。'
    }
    
    # 查找非标准日期格式
    try:
        # 首先尝试转换为日期时间类型
        pd.to_datetime(df_copy['date'], format='%Y-%m-%d', errors='raise')
        # 如果没有错误，说明所有日期都是标准格式
        non_standard_dates = pd.DataFrame()
    except:
        # 如果有错误，查找非标准格式的日期
        non_standard_dates = df_copy[~df_copy['date'].str.match(r'^\d{4}-\d{2}-\d{2}$')][['transaction_id', 'date']].head(10)
    
    # 记录清理前的数据
    report[step]['before'] = non_standard_dates if not non_standard_dates.empty else pd.DataFrame({'信息': ['所有日期已是标准格式']})
    
    # 统一日期格式
    df_copy['date'] = pd.to_datetime(df_copy['date'], errors='coerce').dt.strftime('%Y-%m-%d')
    
    # 记录清理后的数据
    report[step]['after'] = df_copy.loc[non_standard_dates.index][['transaction_id', 'date']] if not non_standard_dates.empty else pd.DataFrame({'信息': ['所有日期已是标准格式']})
    
    # 步骤3: 处理负价格
    step = 3
    report[step] = {
        'title': '处理负价格',
        'description': '将负价格转换为正价格，并标记为退款。'
    }
    
    # 记录清理前的数据
    negative_prices = df_copy[df_copy['unit_price'] < 0][['transaction_id', 'product_id', 'unit_price', 'item_total', 'status']].head(10)
    report[step]['before'] = negative_prices
    
    # 添加"退款类型"列
    if 'refund_type' not in df_copy.columns:
        df_copy['refund_type'] = 'None'
    
    # 处理负价格
    negative_price_indices = df_copy[df_copy['unit_price'] < 0].index
    df_copy.loc[negative_price_indices, 'unit_price'] = df_copy.loc[negative_price_indices, 'unit_price'].abs()
    df_copy.loc[negative_price_indices, 'item_total'] = df_copy.loc[negative_price_indices, 'item_total'].abs()
    df_copy.loc[negative_price_indices, 'status'] = 'Refunded'
    df_copy.loc[negative_price_indices, 'refund_type'] = 'Price Adjustment'
    
    # 记录清理后的数据
    report[step]['after'] = df_copy.loc[negative_prices.index][['transaction_id', 'product_id', 'unit_price', 'item_total', 'status', 'refund_type']]
    
    return df_copy, report

def clean_marketing_data(df):
    """清理营销活动数据"""
    report = {}
    df_copy = df.copy()
    
    # 步骤1: 处理ROI格式不一致问题
    step = 1
    report[step] = {
        'title': '统一ROI格式',
        'description': '将百分比格式的ROI转换为小数格式。'
    }
    
    # 查找字符串格式的ROI
    string_rois = df_copy[df_copy['roi'].apply(lambda x: isinstance(x, str))][['campaign_id', 'name', 'roi']].head(10)
    
    # 记录清理前的数据
    report[step]['before'] = string_rois
    
    # 统一ROI格式
    def standardize_roi(roi):
        if pd.isna(roi):
            return np.nan
        if isinstance(roi, str):
            # 移除百分号并转换为小数
            return float(roi.strip('%')) / 100
        return roi
    
    df_copy['roi'] = df_copy['roi'].apply(standardize_roi)
    
    # 记录清理后的数据
    report[step]['after'] = df_copy.loc[string_rois.index][['campaign_id', 'name', 'roi']]
    
    # 步骤2: 处理异常的营销支出
    step = 2
    report[step] = {
        'title': '处理异常营销支出',
        'description': '将超出预算的支出调整为不超过预算的110%。'
    }
    
    # 找出支出超过预算的活动
    over_budget = df_copy[df_copy['spend'] > df_copy['budget'] * 1.1][['campaign_id', 'name', 'budget', 'spend']].head(10)
    
    # 记录清理前的数据
    report[step]['before'] = over_budget
    
    # 处理异常支出
    over_budget_indices = df_copy[df_copy['spend'] > df_copy['budget'] * 1.1].index
    df_copy.loc[over_budget_indices, 'spend'] = df_copy.loc[over_budget_indices, 'budget'] * 1.1
    
    # 记录清理后的数据
    report[step]['after'] = df_copy.loc[over_budget.index][['campaign_id', 'name', 'budget', 'spend']]
    
    # 步骤3: 添加派生指标
    step = 3
    report[step] = {
        'title': '添加派生营销指标',
        'description': '添加ROI_category和效率指标等派生字段。'
    }
    
    # 记录清理前的列
    report[step]['before'] = pd.DataFrame({'列名': df_copy.columns.tolist()})
    
    # 添加ROI分类
    df_copy['roi_category'] = pd.cut(
        df_copy['roi'], 
        bins=[-float('inf'), 0, 0.5, 1, 2, float('inf')],
        labels=['负收益', '低收益', '中等收益', '高收益', '超高收益']
    )
    
    # 添加效率指标
    df_copy['efficiency_score'] = (df_copy['conversions'] / df_copy['clicks']).fillna(0) * (df_copy['clicks'] / df_copy['impressions']).fillna(0) * 100
    
    # 添加活动持续时间
    df_copy['campaign_duration'] = (pd.to_datetime(df_copy['end_date']) - pd.to_datetime(df_copy['start_date'])).dt.days
    
    # 记录清理后的新列
    report[step]['after'] = pd.DataFrame({'列名': df_copy.columns.tolist()})
    
    return df_copy, report

def clean_traffic_data(df):
    """清理网站流量数据"""
    report = {}
    df_copy = df.copy()
    
    # 步骤1: 处理缺失的渠道数据
    step = 1
    report[step] = {
        'title': '处理缺失的渠道数据',
        'description': '使用同一天其他渠道的平均分布填充缺失的渠道流量数据。'
    }
    
    # 查找有缺失渠道数据的行
    channels = ['organic_search', 'paid_search', 'social_media', 'email', 'direct', 'referral']
    missing_channels = df_copy[df_copy[channels].isna().any(axis=1)][['date', 'total_visits'] + channels].head(10)
    
    # 记录清理前的数据
    report[step]['before'] = missing_channels
    
    # 填充缺失的渠道数据
    for idx, row in df_copy[df_copy[channels].isna().any(axis=1)].iterrows():
        # 计算已知渠道流量的总和
        known_channels_sum = row[channels].sum(skipna=True)
        # 计算缺失的流量总量
        missing_traffic = row['total_visits'] - known_channels_sum
        
        # 计算缺失的渠道数量
        missing_channels_mask = row[channels].isna()
        missing_channels_count = missing_channels_mask.sum()
        
        if missing_channels_count > 0:
            # 平均分配缺失流量到缺失的渠道
            for channel in channels:
                if pd.isna(row[channel]):
                    df_copy.at[idx, channel] = missing_traffic / missing_channels_count
    
    # 记录清理后的数据
    report[step]['after'] = df_copy.loc[missing_channels.index][['date', 'total_visits'] + channels]
    
    # 步骤2: 计算返回访客百分比
    step = 2
    report[step] = {
        'title': '计算返回访客百分比',
        'description': '使用新访客百分比计算返回访客百分比。'
    }
    
    # 记录清理前的数据
    before_sample = df_copy[['date', 'new_visitors_pct', 'returning_visitors_pct']].head(10)
    report[step]['before'] = before_sample
    
    # 计算返回访客百分比
    df_copy['returning_visitors_pct'] = 1 - df_copy['new_visitors_pct']
    
    # 记录清理后的数据
    report[step]['after'] = df_copy.loc[before_sample.index][['date', 'new_visitors_pct', 'returning_visitors_pct']]
    
    # 步骤3: 添加周和月的派生字段
    step = 3
    report[step] = {
        'title': '添加时间派生字段',
        'description': '添加年、月、周、工作日等派生字段以便进行时间相关分析。'
    }
    
    # 记录清理前的列
    report[step]['before'] = pd.DataFrame({'列名': df_copy.columns.tolist()})
    
    # 确保日期列是日期时间类型
    df_copy['date'] = pd.to_datetime(df_copy['date'])
    
    # 添加派生字段
    df_copy['year'] = df_copy['date'].dt.year
    df_copy['month'] = df_copy['date'].dt.month
    df_copy['week'] = df_copy['date'].dt.isocalendar().week
    df_copy['day_of_week'] = df_copy['date'].dt.dayofweek
    df_copy['is_weekend'] = df_copy['day_of_week'].isin([5, 6])
    
    # 记录清理后的新列
    report[step]['after'] = pd.DataFrame({'列名': df_copy.columns.tolist()})
    
    return df_copy, report 