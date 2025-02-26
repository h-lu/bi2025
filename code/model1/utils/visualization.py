import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

def plot_bar_chart(df, x_col, y_col=None, title=None, xlabel=None, ylabel=None, 
                  color='blue', horizontal=False, figsize=(10, 6)):
    """
    绘制条形图
    
    参数:
    df: DataFrame, 数据源
    x_col: str, X轴列名
    y_col: str, Y轴列名 (如果为None，则统计x_col的频数)
    title: str, 图表标题
    xlabel: str, X轴标签
    ylabel: str, Y轴标签
    color: str, 条形颜色
    horizontal: bool, 是否为水平条形图
    figsize: tuple, 图表尺寸
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    if y_col is None:
        # 统计x_col的频数
        data = df[x_col].value_counts().sort_values(ascending=horizontal)
        if horizontal:
            ax.barh(data.index, data.values, color=color)
        else:
            ax.bar(data.index, data.values, color=color)
    else:
        # 使用指定的x_col和y_col
        if horizontal:
            ax.barh(df[x_col], df[y_col], color=color)
        else:
            ax.bar(df[x_col], df[y_col], color=color)
    
    # 设置标题和标签
    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    
    # 处理标签拥挤问题
    if not horizontal and len(df[x_col].unique()) > 10:
        plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    return fig

def plot_line_chart(df, x_col, y_col, title=None, xlabel=None, ylabel=None, 
                  color='blue', marker='o', figsize=(10, 6)):
    """
    绘制折线图
    
    参数:
    df: DataFrame, 数据源
    x_col: str, X轴列名
    y_col: str or list, Y轴列名或列名列表
    title: str, 图表标题
    xlabel: str, X轴标签
    ylabel: str, Y轴标签
    color: str or list, 线条颜色
    marker: str, 数据点标记
    figsize: tuple, 图表尺寸
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    if isinstance(y_col, str):
        y_cols = [y_col]
    else:
        y_cols = y_col
    
    if isinstance(color, str):
        colors = [color] * len(y_cols)
    else:
        colors = color
    
    for i, (y, c) in enumerate(zip(y_cols, colors)):
        ax.plot(df[x_col], df[y], marker=marker, color=c, label=y)
    
    # 设置标题和标签
    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    
    # 显示图例
    if len(y_cols) > 1:
        ax.legend()
    
    # 处理标签拥挤问题
    if len(df[x_col].unique()) > 10:
        plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    return fig

def plot_scatter(df, x_col, y_col, title=None, xlabel=None, ylabel=None, 
               color_col=None, size_col=None, figsize=(10, 6)):
    """
    绘制散点图
    
    参数:
    df: DataFrame, 数据源
    x_col: str, X轴列名
    y_col: str, Y轴列名
    title: str, 图表标题
    xlabel: str, X轴标签
    ylabel: str, Y轴标签
    color_col: str, 用于区分颜色的列名
    size_col: str, 用于区分点大小的列名
    figsize: tuple, 图表尺寸
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    if color_col is not None and size_col is not None:
        scatter = ax.scatter(df[x_col], df[y_col], c=df[color_col], s=df[size_col]*10, 
                            alpha=0.7, cmap='viridis')
        plt.colorbar(scatter, label=color_col)
    elif color_col is not None:
        scatter = ax.scatter(df[x_col], df[y_col], c=df[color_col], alpha=0.7, cmap='viridis')
        plt.colorbar(scatter, label=color_col)
    elif size_col is not None:
        ax.scatter(df[x_col], df[y_col], s=df[size_col]*10, alpha=0.7)
    else:
        ax.scatter(df[x_col], df[y_col], alpha=0.7)
    
    # 设置标题和标签
    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    
    plt.tight_layout()
    return fig

def plot_histogram(df, column, bins=10, title=None, xlabel=None, ylabel="频数", 
                 color='blue', kde=False, figsize=(10, 6)):
    """
    绘制直方图
    
    参数:
    df: DataFrame, 数据源
    column: str, 待分析的列名
    bins: int or list, 分箱数量或自定义边界
    title: str, 图表标题
    xlabel: str, X轴标签
    ylabel: str, Y轴标签
    color: str, 填充颜色
    kde: bool, 是否显示核密度估计曲线
    figsize: tuple, 图表尺寸
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    sns.histplot(df[column], bins=bins, color=color, kde=kde, ax=ax)
    
    # 设置标题和标签
    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    plt.tight_layout()
    return fig

def plot_pie_chart(df, column, title=None, colors=None, autopct='%1.1f%%', 
                 figsize=(10, 8), max_categories=8):
    """
    绘制饼图
    
    参数:
    df: DataFrame, 数据源
    column: str, 用于生成饼图的列名
    title: str, 图表标题
    colors: list, 颜色列表
    autopct: str, 百分比格式
    figsize: tuple, 图表尺寸
    max_categories: int, 最大类别数量 (超过则合并为"其他")
    """
    # 统计频数
    value_counts = df[column].value_counts()
    
    # 处理类别过多的情况
    if len(value_counts) > max_categories:
        others = pd.Series({'其他': value_counts[max_categories:].sum()})
        value_counts = pd.concat([value_counts[:max_categories], others])
    
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.pie(value_counts.values, labels=value_counts.index, autopct=autopct,
          shadow=False, startangle=90, colors=colors)
    
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    
    # 设置标题
    if title:
        ax.set_title(title)
    
    plt.tight_layout()
    return fig

def plot_box(df, x_col=None, y_col=None, title=None, xlabel=None, ylabel=None, 
           figsize=(10, 6), horizontal=False):
    """
    绘制箱线图
    
    参数:
    df: DataFrame, 数据源
    x_col: str, X轴分组列名
    y_col: str, Y轴数值列名
    title: str, 图表标题
    xlabel: str, X轴标签
    ylabel: str, Y轴标签
    figsize: tuple, 图表尺寸
    horizontal: bool, 是否为水平箱线图
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    if horizontal:
        if x_col and y_col:
            sns.boxplot(x=y_col, y=x_col, data=df, ax=ax)
        elif y_col:
            sns.boxplot(x=df[y_col], ax=ax)
    else:
        if x_col and y_col:
            sns.boxplot(x=x_col, y=y_col, data=df, ax=ax)
        elif y_col:
            sns.boxplot(y=df[y_col], ax=ax)
    
    # 设置标题和标签
    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    
    # 处理标签拥挤问题
    if x_col and len(df[x_col].unique()) > 10:
        plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    return fig

def plot_heatmap(df, columns=None, title=None, figsize=(12, 10), cmap='viridis'):
    """
    绘制相关性热力图
    
    参数:
    df: DataFrame, 数据源
    columns: list, 用于计算相关性的列名列表
    title: str, 图表标题
    figsize: tuple, 图表尺寸
    cmap: str, 颜色映射
    """
    # 如果指定了列，则取子集
    if columns:
        data = df[columns]
    else:
        data = df.select_dtypes(include=['number'])
    
    # 计算相关系数
    corr = data.corr()
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # 绘制热力图
    sns.heatmap(corr, annot=True, cmap=cmap, center=0, ax=ax)
    
    # 设置标题
    if title:
        ax.set_title(title)
    
    plt.tight_layout()
    return fig

def plot_wordcloud(word_freq, title=None, figsize=(12, 8), background_color="white"):
    """
    绘制词云图
    
    参数:
    word_freq: dict or list, 词频字典或(词,频率)列表
    title: str, 图表标题
    figsize: tuple, 图表尺寸
    background_color: str, 背景颜色
    """
    # 转换列表为字典
    if isinstance(word_freq, list):
        word_freq = dict(word_freq)
    
    # 创建词云对象
    wc = WordCloud(width=800, height=400, background_color=background_color,
                  max_words=200, contour_width=3, max_font_size=100)
    
    # 生成词云
    wc.generate_from_frequencies(word_freq)
    
    # 绘制词云
    fig, ax = plt.subplots(figsize=figsize)
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off")
    
    # 设置标题
    if title:
        ax.set_title(title, fontsize=16)
    
    plt.tight_layout()
    return fig

def plot_time_series(df, date_col, value_col, title=None, xlabel=None, ylabel=None, 
                   color='blue', marker=None, figsize=(12, 6)):
    """
    绘制时间序列图
    
    参数:
    df: DataFrame, 数据源
    date_col: str, 日期列名
    value_col: str or list, 值列名或列名列表
    title: str, 图表标题
    xlabel: str, X轴标签
    ylabel: str, Y轴标签
    color: str or list, 线条颜色
    marker: str, 数据点标记
    figsize: tuple, 图表尺寸
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # 确保日期列是日期类型
    df_plot = df.copy()
    df_plot[date_col] = pd.to_datetime(df_plot[date_col])
    df_plot = df_plot.sort_values(by=date_col)
    
    if isinstance(value_col, str):
        value_cols = [value_col]
    else:
        value_cols = value_col
    
    if isinstance(color, str):
        colors = [color] * len(value_cols)
    else:
        colors = color
    
    for i, (val, col) in enumerate(zip(value_cols, colors)):
        ax.plot(df_plot[date_col], df_plot[val], color=col, marker=marker, label=val)
    
    # 设置标题和标签
    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    else:
        ax.set_xlabel('日期')
    if ylabel:
        ax.set_ylabel(ylabel)
    
    # 如果有多个值列，显示图例
    if len(value_cols) > 1:
        ax.legend()
    
    # 格式化日期轴
    plt.xticks(rotation=45)
    fig.autofmt_xdate()
    
    plt.tight_layout()
    return fig 