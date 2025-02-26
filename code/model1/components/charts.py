import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# 引入工具函数
from utils.visualization import (
    plot_bar_chart, plot_line_chart, plot_scatter, plot_histogram,
    plot_pie_chart, plot_box, plot_heatmap, plot_wordcloud, plot_time_series
)

def show_categorical_analysis(df, column, title=None):
    """展示分类列的分析图表"""
    if title is None:
        title = f"{column}分布"
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("条形图")
        fig = plot_bar_chart(df, column, title=title)
        st.pyplot(fig)
    
    with col2:
        st.subheader("饼图")
        fig = plot_pie_chart(df, column, title=title)
        st.pyplot(fig)
    
    # 显示数据表格
    st.subheader("数据统计")
    value_counts = df[column].value_counts().reset_index()
    value_counts.columns = [column, '数量']
    value_counts['百分比'] = value_counts['数量'] / value_counts['数量'].sum() * 100
    value_counts['百分比'] = value_counts['百分比'].map('{:.2f}%'.format)
    st.dataframe(value_counts)

def show_numeric_analysis(df, column, title=None, bins=10):
    """展示数值列的分析图表"""
    if title is None:
        title = f"{column}分布"
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("直方图")
        fig = plot_histogram(df, column, bins=bins, title=title, kde=True)
        st.pyplot(fig)
    
    with col2:
        st.subheader("箱线图")
        fig = plot_box(df, y_col=column, title=title)
        st.pyplot(fig)
    
    # 显示数据统计
    st.subheader("数据统计")
    stats = df[column].describe().reset_index()
    stats.columns = ['统计量', '值']
    st.dataframe(stats)

def show_correlation_analysis(df, columns=None, title="相关性分析"):
    """展示相关性分析"""
    st.subheader(title)
    
    if columns is None:
        # 默认使用所有数值列
        columns = df.select_dtypes(include=['number']).columns.tolist()
    
    # 用户可选择感兴趣的列
    selected_columns = st.multiselect(
        "选择要分析的列",
        options=columns,
        default=columns[:min(5, len(columns))]
    )
    
    if not selected_columns:
        st.warning("请至少选择一个列进行分析")
        return
    
    if len(selected_columns) < 2:
        st.warning("请至少选择两个列以分析相关性")
        return
    
    # 绘制热力图
    fig = plot_heatmap(
        df, 
        columns=selected_columns,
        title="相关性热力图",
        figsize=(10, 8)
    )
    st.pyplot(fig)
    
    # 显示相关系数表格
    st.subheader("相关系数表")
    corr = df[selected_columns].corr().round(2)
    st.dataframe(corr)

def show_scatter_plot_matrix(df, columns=None, title="散点图矩阵"):
    """展示散点图矩阵"""
    st.subheader(title)
    
    if columns is None:
        # 默认使用所有数值列
        columns = df.select_dtypes(include=['number']).columns.tolist()
    
    # 用户可选择感兴趣的列
    selected_columns = st.multiselect(
        "选择要分析的列",
        options=columns,
        default=columns[:min(4, len(columns))]
    )
    
    if not selected_columns:
        st.warning("请至少选择一个列进行分析")
        return
    
    # 绘制散点图矩阵
    fig, axs = plt.subplots(len(selected_columns), len(selected_columns), 
                           figsize=(len(selected_columns)*3, len(selected_columns)*3))
    
    for i, col1 in enumerate(selected_columns):
        for j, col2 in enumerate(selected_columns):
            if i == j:  # 对角线上绘制直方图
                sns.histplot(df[col1], ax=axs[i, j], kde=True)
            else:  # 非对角线上绘制散点图
                sns.scatterplot(data=df, x=col1, y=col2, ax=axs[i, j], alpha=0.5)
            
            # 设置标签
            if i == len(selected_columns) - 1:
                axs[i, j].set_xlabel(col1)
            else:
                axs[i, j].set_xlabel('')
            
            if j == 0:
                axs[i, j].set_ylabel(col2)
            else:
                axs[i, j].set_ylabel('')
    
    plt.tight_layout()
    st.pyplot(fig)

def show_time_series_analysis(df, date_col, value_col, title=None, resample='D'):
    """展示时间序列分析"""
    if title is None:
        title = f"{value_col}随时间的变化"
    
    st.subheader(title)
    
    # 确保日期列是日期类型
    df_plot = df.copy()
    df_plot[date_col] = pd.to_datetime(df_plot[date_col])
    
    # 按日期排序
    df_plot = df_plot.sort_values(by=date_col)
    
    # 绘制原始时间序列
    fig = plot_time_series(
        df_plot,
        date_col=date_col,
        value_col=value_col,
        title="原始时间序列"
    )
    st.pyplot(fig)
    
    # 提供重采样选项
    st.subheader("时间聚合分析")
    
    resample_options = {
        'D': '按天',
        'W': '按周',
        'M': '按月',
        'Q': '按季度',
        'Y': '按年'
    }
    
    selected_resample = st.selectbox(
        "选择时间聚合粒度",
        options=list(resample_options.keys()),
        format_func=lambda x: resample_options[x],
        index=list(resample_options.keys()).index(resample)
    )
    
    # 重采样数据
    df_resampled = df_plot.set_index(date_col).resample(selected_resample)
    
    # 计算聚合
    df_agg = pd.DataFrame({
        'mean': df_resampled[value_col].mean(),
        'min': df_resampled[value_col].min(),
        'max': df_resampled[value_col].max(),
        'sum': df_resampled[value_col].sum()
    }).reset_index()
    
    # 绘制聚合时间序列
    fig = plot_time_series(
        df_agg,
        date_col=date_col,
        value_col=['mean', 'min', 'max'],
        title=f"按{resample_options[selected_resample]}聚合的{value_col}"
    )
    st.pyplot(fig)
    
    # 显示统计数据
    st.subheader("聚合统计数据")
    st.dataframe(df_agg)

def show_wordcloud_component(word_freq, title="词云图"):
    """展示词云组件"""
    st.subheader(title)
    
    # 生成词云图
    fig = plot_wordcloud(word_freq, title="")
    st.pyplot(fig)
    
    # 显示频率最高的词
    st.subheader("高频词统计")
    if isinstance(word_freq, dict):
        word_data = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    else:
        word_data = sorted(word_freq, key=lambda x: x[1], reverse=True)
    
    # 转换为DataFrame并显示
    word_df = pd.DataFrame(word_data, columns=['词', '频率'])
    word_df = word_df.head(20)  # 仅显示前20个
    st.dataframe(word_df)

def show_grouped_analysis(df, group_col, value_col, title=None):
    """展示分组分析组件"""
    if title is None:
        title = f"按{group_col}分组的{value_col}分析"
    
    st.subheader(title)
    
    # 计算分组统计
    grouped = df.groupby(group_col)[value_col].agg(['mean', 'min', 'max', 'count']).reset_index()
    grouped.columns = [group_col, '平均值', '最小值', '最大值', '数量']
    
    # 绘制分组条形图
    fig = plot_bar_chart(
        grouped,
        x_col=group_col,
        y_col='平均值',
        title=f"按{group_col}分组的{value_col}平均值"
    )
    st.pyplot(fig)
    
    # 绘制箱线图
    fig = plot_box(
        df,
        x_col=group_col,
        y_col=value_col,
        title=f"按{group_col}分组的{value_col}分布"
    )
    st.pyplot(fig)
    
    # 显示分组统计数据
    st.subheader("分组统计数据")
    st.dataframe(grouped) 