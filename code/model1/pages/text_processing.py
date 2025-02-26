import streamlit as st
import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import os
import sys
from collections import Counter
import jieba
import plotly.express as px
import plotly.graph_objects as go

# 添加项目根目录到Python路径，以便导入utils模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helpers import load_html_file, extract_review_data, sentiment_analysis

def show():
    """显示文本处理页面内容"""
    st.header("文本处理")
    
    st.markdown("""
    ## 文本处理概述
    
    文本数据是一种常见的非结构化数据形式，需要通过特定的处理技术来提取有价值的信息。在商业智能中，文本处理通常用于分析用户评论、社交媒体内容、新闻报道等。
    """)
    
    st.subheader("常见文本处理任务")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 文本清洗
        
        * 去除HTML标签
        * 去除特殊字符
        * 删除多余空格
        * 大小写转换
        * 错别字纠正
        
        ### 文本分词
        
        * 中文分词
        * 停用词过滤
        * 词干提取/词形还原
        * 词性标注
        """)
        
    with col2:
        st.markdown("""
        ### 文本特征提取
        
        * 词袋模型(Bag of Words)
        * TF-IDF
        * Word2Vec
        * BERT等预训练模型
        
        ### 文本分析
        
        * 情感分析
        * 主题建模
        * 实体识别
        * 关键词提取
        """)
    
    # 文本清洗示例
    st.subheader("文本清洗示例")
    
    st.markdown("""
    文本清洗是文本处理的第一步，旨在移除不必要的元素并将文本转换为标准格式。以下是一些常见的文本清洗操作：
    """)
    
    with st.expander("查看文本清洗代码"):
        st.code("""
import re
from bs4 import BeautifulSoup

def clean_text(text):
    \"\"\"基本文本清洗函数\"\"\"
    # 去除HTML标签
    text = BeautifulSoup(text, "html.parser").get_text()
    
    # 去除URL
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # 去除邮箱
    text = re.sub(r'\S+@\S+', '', text)
    
    # 去除特殊字符和数字
    text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)
    
    # 去除多余空格
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

# 示例文本
html_text = \"\"\"
<div>这是一个<b>产品评论</b>。我非常喜欢这款产品！价格是¥399.00，性价比很高。
用户可以访问 https://example.com 了解更多，或发邮件到 support@example.com 咨询。
#好评 #推荐购买
</div>
\"\"\"

# 应用清洗
cleaned_text = clean_text(html_text)
print(f"原始文本: {html_text}")
print(f"清洗后文本: {cleaned_text}")
        """, language="python")
        
        # 示例文本
        html_text = """
        <div>这是一个<b>产品评论</b>。我非常喜欢这款产品！价格是¥399.00，性价比很高。
        用户可以访问 https://example.com 了解更多，或发邮件到 support@example.com 咨询。
        #好评 #推荐购买
        </div>
        """
        
        # 清洗函数
        def clean_text(text):
            # 去除HTML标签
            text = BeautifulSoup(text, "html.parser").get_text()
            
            # 去除URL
            text = re.sub(r'https?://\S+|www\.\S+', '', text)
            
            # 去除邮箱
            text = re.sub(r'\S+@\S+', '', text)
            
            # 去除特殊字符和数字
            text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)
            
            # 去除多余空格
            text = re.sub(r'\s+', ' ', text).strip()
            
            return text
        
        # 应用清洗
        cleaned_text = clean_text(html_text)
        
        # 显示对比
        st.subheader("文本清洗效果:")
        col1, col2 = st.columns(2)
        with col1:
            st.text_area("原始文本:", html_text, height=150)
        with col2:
            st.text_area("清洗后文本:", cleaned_text, height=150)
    
    # 中文分词示例
    st.subheader("中文分词示例")
    
    st.markdown("""
    中文文本没有明确的词语分隔符，需要使用专门的分词工具进行处理。jieba是一个常用的中文分词库。
    """)
    
    with st.expander("查看中文分词代码"):
        st.code("""
import jieba
import pandas as pd
from collections import Counter

def segment_text(text):
    \"\"\"中文分词\"\"\"
    words = jieba.cut(text)
    return [word for word in words if len(word.strip()) > 0]

# 示例文本
text = "这款手机的屏幕显示效果非常好，电池续航也很强，拍照功能一般，总体来说很满意这次购买"

# 分词
words = segment_text(text)
print(f"分词结果: {' / '.join(words)}")

# 词频统计
word_counts = Counter(words)
df_words = pd.DataFrame({
    '词语': list(word_counts.keys()),
    '频次': list(word_counts.values())
}).sort_values('频次', ascending=False)

print(df_words.head(10))
        """, language="python")
        
        # 示例文本
        text = "这款手机的屏幕显示效果非常好，电池续航也很强，拍照功能一般，总体来说很满意这次购买"
        
        # 分词函数
        def segment_text(text):
            words = jieba.cut(text)
            return [word for word in words if len(word.strip()) > 0]
        
        # 应用分词
        words = segment_text(text)
        word_counts = Counter(words)
        df_words = pd.DataFrame({
            '词语': list(word_counts.keys()),
            '频次': list(word_counts.values())
        }).sort_values('频次', ascending=False)
        
        # 显示结果
        st.text(f"原始文本: {text}")
        st.text(f"分词结果: {' / '.join(words)}")
        st.dataframe(df_words)
    
    # 情感分析示例
    st.subheader("简单情感分析")
    
    st.markdown("""
    情感分析是判断文本表达的情感倾向的过程，可以用于分析用户评论、产品反馈等。
    """)
    
    with st.expander("查看简单情感分析代码"):
        st.code("""
def simple_sentiment_analysis(text):
    \"\"\"简单的情感分析，返回积极/消极分数\"\"\"
    # 这是一个非常简化的情感分析，实际情况应使用更复杂的模型
    positive_words = ['好', '棒', '喜欢', '满意', '推荐', '优秀', '惊艳', '不错', '强', '出色']
    negative_words = ['差', '失望', '不满', '问题', '糟', '坏', '后悔', '慢', '贵', '不值']
    
    positive_score = sum(1 for word in positive_words if word in text)
    negative_score = sum(1 for word in negative_words if word in text)
    
    # 计算总分，范围从-1到1
    score = (positive_score - negative_score) / (positive_score + negative_score) if (positive_score + negative_score) > 0 else 0
    
    # 返回情感标签和分数
    if score > 0.2:
        return "积极", score
    elif score < -0.2:
        return "消极", score
    else:
        return "中性", score

# 示例评论
reviews = [
    "这款手机非常好用，屏幕清晰，电池续航强，推荐购买！",
    "产品质量一般，有些小问题，但总体还可以接受。",
    "太失望了，收到的产品有划痕，客服态度也不好，后悔购买。"
]

# 分析每条评论
for i, review in enumerate(reviews):
    sentiment, score = simple_sentiment_analysis(review)
    print(f"评论 {i+1}: {sentiment} (分数: {score:.2f})")
    print(f"文本: {review}")
    print()
        """, language="python")
        
        # 示例评论
        reviews = [
            "这款手机非常好用，屏幕清晰，电池续航强，推荐购买！",
            "产品质量一般，有些小问题，但总体还可以接受。",
            "太失望了，收到的产品有划痕，客服态度也不好，后悔购买。"
        ]
        
        # 分析每条评论
        results = []
        for review in reviews:
            sent, score = sentiment_analysis(review)
            results.append({
                "评论": review,
                "情感": sent,
                "分数": score
            })
        
        # 显示结果
        df_sentiment = pd.DataFrame(results)
        st.dataframe(df_sentiment)
        
        # 可视化情感分布
        fig, ax = plt.subplots()
        bars = ax.bar(df_sentiment.index, df_sentiment['分数'], color=['green' if s > 0 else 'red' if s < 0 else 'gray' for s in df_sentiment['分数']])
        ax.set_xticks(df_sentiment.index)
        ax.set_xticklabels([f"评论 {i+1}" for i in df_sentiment.index])
        ax.set_ylabel('情感分数')
        ax.set_title('评论情感分析')
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')
        
        st.pyplot(fig)
    
    # 使用模拟数据的真实案例
    st.header("案例：电商产品评论分析")
    
    st.markdown("""
    接下来，我们将使用模拟的电商产品评论数据，演示如何应用文本处理技术进行分析。
    """)
    
    # 加载模拟评论数据
    html_content, soup = load_html_file('mock_html/product_reviews.html')
    
    if html_content and soup:
        # 提取评论数据
        reviews_data = extract_review_data(soup)
        
        if reviews_data:
            df_reviews = pd.DataFrame(reviews_data)
            
            # 显示评论数据
            st.subheader("评论数据预览:")
            st.dataframe(df_reviews[['user_name', 'date', 'rating', 'content']].head())
            
            # 评分分布
            st.subheader("评分分布")
            fig = px.histogram(df_reviews, x='rating', nbins=5, 
                               title="评分分布", 
                               labels={'rating': '评分', 'count': '数量'})
            fig.update_layout(bargap=0.1)
            st.plotly_chart(fig)
            
            # 文本长度分析
            df_reviews['content_length'] = df_reviews['content'].apply(len)
            
            fig = px.scatter(df_reviews, x='rating', y='content_length', 
                             title="评分与评论长度关系",
                             labels={'rating': '评分', 'content_length': '评论长度(字符数)'})
            st.plotly_chart(fig)
            
            # 情感分析
            sentiment_results = []
            for review in df_reviews['content']:
                sent, score = sentiment_analysis(review)
                sentiment_results.append({
                    'sentiment': sent,
                    'score': score
                })
            
            df_sentiment = pd.DataFrame(sentiment_results)
            df_reviews = pd.concat([df_reviews, df_sentiment], axis=1)
            
            # 情感分布
            st.subheader("情感分布")
            fig = px.pie(df_reviews, names='sentiment', title="评论情感分布")
            st.plotly_chart(fig)
            
            # 评分与情感的关系
            st.subheader("评分与情感得分的关系")
            fig = px.scatter(df_reviews, x='rating', y='score', color='sentiment',
                             title="评分与情感得分的关系",
                             labels={'rating': '评分', 'score': '情感得分'},
                             color_discrete_map={'积极': 'green', '消极': 'red', '中性': 'gray'})
            st.plotly_chart(fig)
            
            # 词频分析
            st.subheader("词频分析")
            all_words = []
            for content in df_reviews['content']:
                words = segment_text(content)
                all_words.extend(words)
            
            # 过滤常见停用词
            stopwords = ['的', '了', '和', '是', '在', '我', '也', '不', '都', '这', '有', '就', '很', '也是', '但是', '但']
            filtered_words = [word for word in all_words if word not in stopwords and len(word) > 1]
            
            word_counts = Counter(filtered_words).most_common(20)
            df_word_freq = pd.DataFrame(word_counts, columns=['词语', '频次'])
            
            # 词频柱状图
            fig = px.bar(df_word_freq, x='词语', y='频次', title="评论中最常见的词语")
            st.plotly_chart(fig)
            
            # 基于评分的词汇对比
            st.subheader("不同评分下的特征词汇")
            
            # 提取高评分(4-5)和低评分(1-2)的评论
            high_rating_reviews = df_reviews[df_reviews['rating'] >= 4]['content'].tolist()
            low_rating_reviews = df_reviews[df_reviews['rating'] <= 2]['content'].tolist()
            
            high_words = []
            for review in high_rating_reviews:
                words = segment_text(review)
                high_words.extend([w for w in words if w not in stopwords and len(w) > 1])
            
            low_words = []
            for review in low_rating_reviews:
                words = segment_text(review)
                low_words.extend([w for w in words if w not in stopwords and len(w) > 1])
            
            high_word_counts = Counter(high_words).most_common(10)
            low_word_counts = Counter(low_words).most_common(10)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("高评分(4-5星)特征词:")
                df_high = pd.DataFrame(high_word_counts, columns=['词语', '频次'])
                st.dataframe(df_high)
            
            with col2:
                st.write("低评分(1-2星)特征词:")
                df_low = pd.DataFrame(low_word_counts, columns=['词语', '频次'])
                st.dataframe(df_low)
            
            # 评论示例展示
            st.subheader("典型评论示例")
            
            # 最积极的评论
            most_positive = df_reviews.loc[df_reviews['score'].idxmax()]
            # 最消极的评论
            most_negative = df_reviews.loc[df_reviews['score'].idxmin()]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("最积极的评论:")
                st.info(most_positive['content'])
                st.write(f"评分: {most_positive['rating']}星")
                st.write(f"情感得分: {most_positive['score']:.2f}")
            
            with col2:
                st.write("最消极的评论:")
                st.error(most_negative['content'])
                st.write(f"评分: {most_negative['rating']}星")
                st.write(f"情感得分: {most_negative['score']:.2f}")
        else:
            st.error("无法提取评论数据。")
    else:
        st.error("无法加载模拟评论数据。")
    
    # 结论和建议
    st.header("总结与建议")
    
    st.markdown("""
    通过对模拟电商评论的分析，我们可以得出以下结论：
    
    1. **情感与评分的一致性**：评论的情感分析结果与用户给出的星级评分有较高的一致性，表明文本情感分析可以作为评估用户满意度的一种有效方法。
    
    2. **关键词洞察**：通过词频分析，我们可以识别出用户最关注的产品特性和问题点，如"电池"、"拍照"、"价格"等。
    
    3. **正负面因素对比**：高评分与低评分评论中的关键词对比，揭示了产品的优势和不足。
    
    **业务建议**：
    
    1. 针对负面评论中频繁出现的问题点进行产品改进
    2. 在营销中强调正面评论中提到的产品优势
    3. 建立评论监控系统，及时发现和解决用户投诉
    4. 利用情感分析结果筛选出需要客服介入的评论
    
    **技术提升方向**：
    
    实际应用中，我们可以使用更高级的NLP技术进行更深入的分析，如：
    
    1. 使用更先进的预训练语言模型进行情感分析
    2. 应用主题建模技术挖掘评论中的隐含主题
    3. 引入命名实体识别识别产品具体特性
    4. 构建情感词典，提高分析精度
    """)
    
    # 参考资源
    st.subheader("扩展资源")
    
    st.markdown("""
    - [jieba中文分词](https://github.com/fxsjy/jieba)
    - [NLTK自然语言处理工具包](https://www.nltk.org/)
    - [spaCy现代NLP库](https://spacy.io/)
    - [HanLP多语言自然语言处理工具包](https://github.com/hankcs/HanLP)
    - [中文NLP资源汇总](https://github.com/crownpku/Awesome-Chinese-NLP)
    """) 