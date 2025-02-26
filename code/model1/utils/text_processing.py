import re
import pandas as pd
import numpy as np
import jieba
import streamlit as st
from collections import Counter

def sentiment_analysis(text):
    """简单的情感分析，返回积极/消极分数"""
    # 这是一个非常简化的情感分析，实际情况应使用NLP模型
    positive_words = ['好', '棒', '喜欢', '满意', '推荐', '优秀', '惊艳', '不错', '强', '出色', 
                     '清晰', '流畅', '稳定', '值得', '爱上', '优质', '高级', '超出预期']
    negative_words = ['差', '失望', '不满', '问题', '糟', '坏', '后悔', '慢', '贵', '不值', 
                     '不推荐', '不好', '一般', '中规中矩', '卡顿', '发热']
    
    positive_score = sum(1 for word in positive_words if word in text)
    negative_score = sum(1 for word in negative_words if word in text)
    
    # 计算总分，范围从-1到1
    total_words = len(text)
    if total_words > 0:
        score = (positive_score - negative_score) / (positive_score + negative_score) if (positive_score + negative_score) > 0 else 0
    else:
        score = 0
    
    # 返回情感标签和分数
    if score > 0.2:
        return "积极", score
    elif score < -0.2:
        return "消极", score
    else:
        return "中性", score

def segment_text(text, use_jieba=True):
    """
    对文本进行分词
    
    参数:
    text: str, 待分词的文本
    use_jieba: bool, 是否使用结巴分词 (中文文本)
    
    返回:
    list: 分词结果列表
    """
    if not text or not isinstance(text, str):
        return []
    
    # 使用结巴分词处理中文
    if use_jieba:
        return list(jieba.cut(text))
    
    # 简单的英文分词 (按空格和标点)
    return re.findall(r'\w+', text.lower())

def extract_keywords(text, top_n=5, use_jieba=True, remove_stopwords=True):
    """
    提取文本关键词
    
    参数:
    text: str, 待处理的文本
    top_n: int, 返回前N个关键词
    use_jieba: bool, 是否使用结巴分词提取关键词
    remove_stopwords: bool, 是否移除停用词
    
    返回:
    list: 关键词列表 [(词, 权重), ...]
    """
    if not text or not isinstance(text, str):
        return []
    
    if use_jieba:
        try:
            import jieba.analyse
            # 使用TF-IDF算法提取关键词
            keywords = jieba.analyse.extract_tags(text, topK=top_n, withWeight=True)
            return keywords
        except:
            # 如果jieba分析模块导入失败，回退到简单词频统计
            pass
    
    # 简单的词频统计
    words = segment_text(text, use_jieba=use_jieba)
    
    # 移除停用词
    if remove_stopwords:
        stopwords = get_stopwords()
        words = [word for word in words if word not in stopwords and len(word) > 1]
    
    # 统计词频
    word_counts = Counter(words)
    
    # 返回前N个高频词
    return word_counts.most_common(top_n)

def get_stopwords():
    """
    获取中文停用词列表
    
    返回:
    set: 停用词集合
    """
    # 基本的中文停用词
    basic_stopwords = {
        '的', '了', '和', '是', '就', '都', '而', '及', '或', '一', '与', '这', '那', '你',
        '我', '他', '她', '它', '们', '个', '上', '下', '在', '有', '人', '来', '去', '说',
        '被', '到', '为', '却', '对', '能', '可', '也', '很', '但', '将', '已', '于', '后',
        '前', '从', '想', '大', '小', '多', '少', '之', '么', '什', '怎', '啊', '呢', '吧'
    }
    
    return basic_stopwords

def extract_patterns(text, pattern):
    """
    从文本中提取匹配指定正则表达式的内容
    
    参数:
    text: str, 待处理的文本
    pattern: str, 正则表达式模式
    
    返回:
    list: 匹配的内容列表
    """
    if not text or not isinstance(text, str):
        return []
    
    try:
        matches = re.findall(pattern, text)
        return matches
    except:
        return []

def calculate_text_stats(text):
    """
    计算文本的基本统计信息
    
    参数:
    text: str, 待分析的文本
    
    返回:
    dict: 包含字符数、词数、句子数等统计信息
    """
    if not text or not isinstance(text, str):
        return {'字符数': 0, '词数': 0, '句子数': 0, '段落数': 0, '平均词长': 0}
    
    # 字符数 (不计空格)
    char_count = len(text.replace(' ', ''))
    
    # 分词
    words = segment_text(text)
    word_count = len(words)
    
    # 句子数 (按句号、问号、感叹号分割)
    sentences = re.split(r'[。！？.!?]', text)
    sentence_count = len([s for s in sentences if s.strip()])
    
    # 段落数 (按换行符分割)
    paragraphs = text.split('\n')
    paragraph_count = len([p for p in paragraphs if p.strip()])
    
    # 平均词长
    avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0
    
    return {
        '字符数': char_count,
        '词数': word_count,
        '句子数': sentence_count,
        '段落数': paragraph_count,
        '平均词长': round(avg_word_length, 2)
    }

def batch_sentiment_analysis(df, text_column):
    """
    对数据框中的文本列进行批量情感分析
    
    参数:
    df: DataFrame, 包含文本列的数据框
    text_column: str, 文本列的名称
    
    返回:
    DataFrame: 添加了情感分析结果的数据框
    """
    # 创建副本避免修改原始数据
    df_result = df.copy()
    
    # 如果文本列不存在，返回原始数据框
    if text_column not in df_result.columns:
        return df_result
    
    # 存储情感标签和分数
    sentiment_labels = []
    sentiment_scores = []
    
    # 对每行文本进行情感分析
    for text in df_result[text_column]:
        if pd.isna(text) or not isinstance(text, str):
            # 处理空值或非字符串
            sentiment_labels.append('未知')
            sentiment_scores.append(0)
        else:
            label, score = sentiment_analysis(text)
            sentiment_labels.append(label)
            sentiment_scores.append(score)
    
    # 添加结果列
    df_result['情感标签'] = sentiment_labels
    df_result['情感分数'] = sentiment_scores
    
    return df_result

def classify_by_keywords(text, keyword_dict):
    """
    根据关键词字典对文本进行分类
    
    参数:
    text: str, 待分类的文本
    keyword_dict: dict, 类别和关键词列表的字典 {'类别1': ['关键词1', '关键词2'], ...}
    
    返回:
    str: 匹配的类别，如果没有匹配则返回'未分类'
    """
    if not text or not isinstance(text, str) or not keyword_dict:
        return '未分类'
    
    # 转为小写以进行不区分大小写的匹配
    text_lower = text.lower()
    
    # 遍历每个类别的关键词
    for category, keywords in keyword_dict.items():
        for keyword in keywords:
            if keyword.lower() in text_lower:
                return category
    
    return '未分类'

def word_cloud_data(texts, top_n=100, use_jieba=True, remove_stopwords=True):
    """
    生成词云数据
    
    参数:
    texts: list or str, 文本列表或单个文本
    top_n: int, 返回前N个词
    use_jieba: bool, 是否使用结巴分词
    remove_stopwords: bool, 是否移除停用词
    
    返回:
    list: [(词, 词频), ...] 用于词云生成
    """
    if isinstance(texts, str):
        texts = [texts]
    
    # 合并所有文本
    all_text = ' '.join([str(text) for text in texts if text and not pd.isna(text)])
    
    # 分词
    words = segment_text(all_text, use_jieba=use_jieba)
    
    # 移除停用词
    if remove_stopwords:
        stopwords = get_stopwords()
        words = [word for word in words if word not in stopwords and len(word) > 1]
    
    # 统计词频
    word_counts = Counter(words)
    
    # 返回前N个高频词
    return word_counts.most_common(top_n) 