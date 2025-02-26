import pandas as pd
import numpy as np
import re

def clean_numeric_column(df, column, min_value=None, max_value=None, handle_missing='mean'):
    """
    清洗数值列，处理异常值和缺失值
    
    参数:
    df: DataFrame, 待处理的数据框
    column: str, 待清洗的列名
    min_value: float, 最小允许值，小于此值将被视为异常
    max_value: float, 最大允许值，大于此值将被视为异常
    handle_missing: str, 处理缺失值的方法: 'mean'(均值),'median'(中位数),'mode'(众数),'drop'(删除),'zero'(填0)
    
    返回:
    DataFrame: 处理后的数据框
    """
    # 创建副本避免修改原始数据
    df_clean = df.copy()
    
    # 如果列不存在，返回原始数据框
    if column not in df_clean.columns:
        return df_clean
    
    # 将非数值转换为NaN
    df_clean[column] = pd.to_numeric(df_clean[column], errors='coerce')
    
    # 处理异常值
    if min_value is not None:
        df_clean.loc[df_clean[column] < min_value, column] = np.nan
    
    if max_value is not None:
        df_clean.loc[df_clean[column] > max_value, column] = np.nan
    
    # 处理缺失值
    if handle_missing == 'mean' and not df_clean[column].isna().all():
        df_clean[column] = df_clean[column].fillna(df_clean[column].mean())
    elif handle_missing == 'median' and not df_clean[column].isna().all():
        df_clean[column] = df_clean[column].fillna(df_clean[column].median())
    elif handle_missing == 'mode' and not df_clean[column].isna().all():
        df_clean[column] = df_clean[column].fillna(df_clean[column].mode()[0])
    elif handle_missing == 'zero':
        df_clean[column] = df_clean[column].fillna(0)
    elif handle_missing == 'drop':
        df_clean = df_clean.dropna(subset=[column])
    
    return df_clean

def remove_duplicates(df, subset=None, keep='first'):
    """
    移除数据框中的重复行
    
    参数:
    df: DataFrame, 待处理的数据框
    subset: list, 用于判断重复的列，None表示使用所有列
    keep: str, 保留重复项的哪一个: 'first'(第一个), 'last'(最后一个), False(全部删除)
    
    返回:
    DataFrame: 去除重复行后的数据框
    tuple: (DataFrame, int) 去重后的数据框和删除的行数
    """
    # 记录原始行数
    original_rows = len(df)
    
    # 去除重复行
    df_clean = df.drop_duplicates(subset=subset, keep=keep)
    
    # 计算删除的行数
    removed_rows = original_rows - len(df_clean)
    
    return df_clean, removed_rows

def clean_text_column(df, column, lower=True, remove_punctuation=True, 
                     remove_numbers=False, remove_html_tags=False, 
                     remove_extra_spaces=True):
    """
    清洗文本列
    
    参数:
    df: DataFrame, 待处理的数据框
    column: str, 待清洗的文本列名
    lower: bool, 是否转换为小写
    remove_punctuation: bool, 是否移除标点符号
    remove_numbers: bool, 是否移除数字
    remove_html_tags: bool, 是否移除HTML标签
    remove_extra_spaces: bool, 是否移除多余空格
    
    返回:
    DataFrame: 处理后的数据框
    """
    # 创建副本避免修改原始数据
    df_clean = df.copy()
    
    # 如果列不存在或非文本列，返回原始数据框
    if column not in df_clean.columns:
        return df_clean
    
    # 确保是字符串类型
    df_clean[column] = df_clean[column].astype(str)
    
    # 转换为小写
    if lower:
        df_clean[column] = df_clean[column].str.lower()
    
    # 移除HTML标签
    if remove_html_tags:
        df_clean[column] = df_clean[column].str.replace(r'<.*?>', '', regex=True)
    
    # 移除标点符号
    if remove_punctuation:
        df_clean[column] = df_clean[column].str.replace(r'[^\w\s]', '', regex=True)
    
    # 移除数字
    if remove_numbers:
        df_clean[column] = df_clean[column].str.replace(r'\d+', '', regex=True)
    
    # 移除多余空格
    if remove_extra_spaces:
        df_clean[column] = df_clean[column].str.replace(r'\s+', ' ', regex=True).str.strip()
    
    return df_clean

def normalize_column(df, column):
    """
    对数值列进行标准化 (z-score)
    
    参数:
    df: DataFrame, 待处理的数据框
    column: str, 待标准化的列名
    
    返回:
    DataFrame: 标准化后的数据框
    """
    # 创建副本避免修改原始数据
    df_norm = df.copy()
    
    # 如果列不存在，返回原始数据框
    if column not in df_norm.columns:
        return df_norm
    
    # 将列转换为数值类型
    df_norm[column] = pd.to_numeric(df_norm[column], errors='coerce')
    
    # 应用标准化
    mean = df_norm[column].mean()
    std = df_norm[column].std()
    
    if std > 0:  # 避免除以零
        df_norm[column + '_normalized'] = (df_norm[column] - mean) / std
    else:
        df_norm[column + '_normalized'] = 0
    
    return df_norm

def encode_categorical(df, column, method='one-hot', drop_first=False):
    """
    对分类变量进行编码
    
    参数:
    df: DataFrame, 待处理的数据框
    column: str, 待编码的分类列名
    method: str, 编码方法: 'one-hot', 'label'
    drop_first: bool, 是否删除第一个类别(one-hot编码时)
    
    返回:
    DataFrame: 编码后的数据框
    """
    # 创建副本避免修改原始数据
    df_encoded = df.copy()
    
    # 如果列不存在，返回原始数据框
    if column not in df_encoded.columns:
        return df_encoded
    
    # 应用编码
    if method == 'one-hot':
        # 创建独热编码
        dummies = pd.get_dummies(df_encoded[column], prefix=column, drop_first=drop_first)
        
        # 将编码结果与原始数据框连接
        df_encoded = pd.concat([df_encoded, dummies], axis=1)
        
    elif method == 'label':
        # 创建标签编码
        df_encoded[column + '_encoded'] = df_encoded[column].astype('category').cat.codes
    
    return df_encoded

def detect_outliers(df, column, method='iqr', threshold=1.5):
    """
    检测数值列中的异常值
    
    参数:
    df: DataFrame, 待处理的数据框
    column: str, 待检测的列名
    method: str, 检测方法: 'iqr'(四分位距法), 'zscore'(Z分数法)
    threshold: float, 阈值倍数(IQR方法)或Z分数阈值
    
    返回:
    Series: 布尔序列，True表示该行是异常值
    """
    # 如果列不存在，返回空序列
    if column not in df.columns:
        return pd.Series([False] * len(df))
    
    # 将列转换为数值类型
    series = pd.to_numeric(df[column], errors='coerce')
    
    if method == 'iqr':
        # 计算四分位数
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        
        # 计算上下界
        lower_bound = q1 - threshold * iqr
        upper_bound = q3 + threshold * iqr
        
        # 检测异常值
        outliers = (series < lower_bound) | (series > upper_bound)
        
    elif method == 'zscore':
        # 计算Z分数
        z_scores = (series - series.mean()) / series.std()
        
        # 检测异常值
        outliers = abs(z_scores) > threshold
    
    else:
        outliers = pd.Series([False] * len(df))
    
    return outliers

def bin_numeric_column(df, column, bins=5, labels=None, strategy='uniform'):
    """
    将数值列分箱
    
    参数:
    df: DataFrame, 待处理的数据框
    column: str, 待分箱的列名
    bins: int or list, 分箱数量或自定义分箱边界
    labels: list, 分箱标签
    strategy: str, 分箱策略: 'uniform'(等宽), 'quantile'(等频), 'kmeans'(K均值)
    
    返回:
    DataFrame: 分箱后的数据框
    """
    # 创建副本避免修改原始数据
    df_binned = df.copy()
    
    # 如果列不存在，返回原始数据框
    if column not in df_binned.columns:
        return df_binned
    
    # 将列转换为数值类型
    df_binned[column] = pd.to_numeric(df_binned[column], errors='coerce')
    
    if strategy == 'uniform':
        # 等宽分箱
        df_binned[column + '_binned'] = pd.cut(df_binned[column], bins=bins, labels=labels)
    
    elif strategy == 'quantile':
        # 等频分箱
        df_binned[column + '_binned'] = pd.qcut(df_binned[column], q=bins, labels=labels, duplicates='drop')
    
    elif strategy == 'kmeans':
        # K均值分箱 (需要安装scikit-learn)
        try:
            from sklearn.cluster import KMeans
            
            # 去除缺失值
            valid_data = df_binned[column].dropna().values.reshape(-1, 1)
            
            # 应用K-means
            kmeans = KMeans(n_clusters=bins, random_state=0).fit(valid_data)
            
            # 获取排序后的中心点
            centers = sorted(kmeans.cluster_centers_.reshape(-1))
            
            # 创建分箱边界
            bin_edges = [float('-inf')] + [(centers[i] + centers[i+1])/2 for i in range(len(centers)-1)] + [float('inf')]
            
            # 应用分箱
            df_binned[column + '_binned'] = pd.cut(df_binned[column], bins=bin_edges, labels=labels)
            
        except ImportError:
            # 如果没有安装scikit-learn，回退到等宽分箱
            df_binned[column + '_binned'] = pd.cut(df_binned[column], bins=bins, labels=labels)
    
    return df_binned 