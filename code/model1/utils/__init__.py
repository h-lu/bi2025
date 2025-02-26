"""工具函数包，提供数据处理、解析、可视化等功能"""

from .data_generators import generate_example_data, generate_text_data, generate_time_series_data
from .parsers import (load_html_file, extract_product_data, extract_review_data, 
                     extract_news_data, parse_api_json)
from .preprocessing import (clean_numeric_column, remove_duplicates, clean_text_column,
                          normalize_column, encode_categorical, detect_outliers,
                          bin_numeric_column)
from .text_processing import (sentiment_analysis, segment_text, extract_keywords,
                            get_stopwords, extract_patterns, calculate_text_stats,
                            batch_sentiment_analysis, classify_by_keywords,
                            word_cloud_data)
from .visualization import (plot_bar_chart, plot_line_chart, plot_scatter, plot_histogram,
                          plot_pie_chart, plot_box, plot_heatmap, plot_wordcloud,
                          plot_time_series)

__all__ = [
    'generate_example_data', 'generate_text_data', 'generate_time_series_data',
    'load_html_file', 'extract_product_data', 'extract_review_data', 'extract_news_data', 'parse_api_json',
    'clean_numeric_column', 'remove_duplicates', 'clean_text_column', 'normalize_column',
    'encode_categorical', 'detect_outliers', 'bin_numeric_column',
    'sentiment_analysis', 'segment_text', 'extract_keywords', 'get_stopwords',
    'extract_patterns', 'calculate_text_stats', 'batch_sentiment_analysis',
    'classify_by_keywords', 'word_cloud_data',
    'plot_bar_chart', 'plot_line_chart', 'plot_scatter', 'plot_histogram',
    'plot_pie_chart', 'plot_box', 'plot_heatmap', 'plot_wordcloud', 'plot_time_series'
] 