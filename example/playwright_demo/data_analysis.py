import pandas as pd
import re
import numpy as np
from datetime import datetime

class LaptopDataAnalyzer:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
        
    def clean_price(self):
        """清理价格数据，将'??'替换为实际数字"""
        def extract_price(price_str):
            if pd.isna(price_str):
                return np.nan
            # 提取价格中的数字部分
            base = re.sub(r'[^0-9]', '', price_str)
            if not base:
                return np.nan
            return float(base)
        
        self.df['price'] = self.df['price'].apply(extract_price)
        
    def extract_laptop_info(self):
        """从标题中提取笔记本信息"""
        def extract_brand(title):
            # 主流品牌匹配
            brands = {
                'lenovo': '联想',
                'thinkpad': 'ThinkPad',
                'huawei': '华为',
                'hp': '惠普',
                'dell': '戴尔',
                'apple': '苹果',
                'asus': '华硕',
                'honor': '荣耀',
                'microsoft': '微软',
                'msi': '微星'
            }
            
            title_lower = title.lower()
            for eng, chn in brands.items():
                if eng in title_lower or chn in title:
                    return chn
            return '其他'
        
        def extract_memory(title):
            """提取内存大小，常见值为8G、16G、32G、64G"""
            # 定义常见的内存大小
            common_sizes = {'8', '16', '32', '64'}
            
            # 首先尝试匹配"16G内存"这样的完整模式
            memory_pattern = r'(\d+)\s*[Gg][Bb]?\s*(内存|运存)'
            memory_match = re.search(memory_pattern, title)
            if memory_match and memory_match.group(1) in common_sizes:
                return int(memory_match.group(1))
            
            # 然后尝试匹配单独的"16G"模式
            simple_pattern = r'(?<!\d)(\d+)\s*[Gg][Bb]?(?!\d)'
            matches = re.finditer(simple_pattern, title)
            for match in matches:
                size = match.group(1)
                if size in common_sizes:
                    # 确保这不是硬盘大小（通常硬盘前后会有512G、1T这样的关键词）
                    context = title[max(0, match.start()-10):min(len(title), match.end()+10)]
                    if not any(keyword in context.lower() for keyword in ['ssd', '固态', '硬盘', 'tb', '存储']):
                        return int(size)
            return None
        
        def extract_storage(title):
            """提取存储容量，常见值为256G、512G、1T、2T"""
            # 首先尝试匹配TB模式
            tb_pattern = r'(?<!\d)([1-9])\s*[Tt][Bb]?(?!\d)'
            tb_match = re.search(tb_pattern, title)
            if tb_match:
                return int(tb_match.group(1)) * 1024  # 转换为GB
            
            # 然后匹配GB模式
            gb_pattern = r'(?<!\d)(256|512|1024)\s*[Gg][Bb]?(?!\d)'
            gb_match = re.search(gb_pattern, title)
            if gb_match:
                return int(gb_match.group(1))
            
            return None
        
        def extract_screen_size(title):
            """提取屏幕尺寸，常见值为13.3、14、15.6、16、17.3英寸"""
            common_sizes = {'13.3', '13.6', '14', '14.0', '15.6', '16', '16.0', '17.3'}
            screen_pattern = r'(\d{2}\.?\d?)\s*英寸'
            screen_match = re.search(screen_pattern, title)
            if screen_match:
                size = screen_match.group(1)
                # 如果是常见尺寸，则返回
                if size in common_sizes or any(abs(float(size) - float(common)) < 0.1 for common in common_sizes):
                    return float(size)
            return None
        
        def extract_processor(title):
            """提取处理器信息，包括代数"""
            processor_patterns = {
                'i9': r'(i9-1[0-5]\d{3}[A-Z]*|酷睿i9-1[0-5]代)',
                'i7': r'(i7-1[0-5]\d{3}[A-Z]*|酷睿i7-1[0-5]代)',
                'i5': r'(i5-1[0-5]\d{3}[A-Z]*|酷睿i5-1[0-5]代)',
                'r9': r'(r9-[7-8]\d{3}[A-Z]*|锐龙R9-[7-8])',
                'r7': r'(r7-[7-8]\d{3}[A-Z]*|锐龙R7-[7-8])',
                'r5': r'(r5-[7-8]\d{3}[A-Z]*|锐龙R5-[7-8])',
                'ultra': r'(Ultra\s*[3579]|酷睿Ultra\s*[3579])',
                'm3': r'M3\s*(pro|max|ultra)?',
                'm2': r'M2\s*(pro|max|ultra)?'
            }
            
            for proc_type, pattern in processor_patterns.items():
                if re.search(pattern, title, re.IGNORECASE):
                    return proc_type
            return '其他'

        def extract_gpu(title):
            """提取显卡信息"""
            gpu_patterns = {
                'RTX4090': r'4090',
                'RTX4080': r'4080',
                'RTX4070': r'4070',
                'RTX4060': r'4060',
                'RTX4050': r'4050',
                'RTX3060': r'3060',
                'Intel': r'锐炬|iris|xe',
                'AMD': r'AMD\s*Radeon',
                'Apple': r'M[23]\s*(pro|max|ultra)?'
            }
            
            for gpu_type, pattern in gpu_patterns.items():
                if re.search(pattern, title, re.IGNORECASE):
                    return gpu_type
            return '集成显卡'
        
        # 提取各种信息
        self.df['brand'] = self.df['title'].apply(extract_brand)
        self.df['memory'] = self.df['title'].apply(extract_memory)
        self.df['storage'] = self.df['title'].apply(extract_storage)
        self.df['screen_size'] = self.df['title'].apply(extract_screen_size)
        self.df['processor'] = self.df['title'].apply(extract_processor)
        self.df['gpu'] = self.df['title'].apply(extract_gpu)
        
    def analyze_data(self):
        """分析处理后的数据"""
        # 基本统计信息
        stats = {
            '品牌分布': self.df['brand'].value_counts(),
            '处理器分布': self.df['processor'].value_counts(),
            '显卡分布': self.df['gpu'].value_counts(),
            '平均价格': self.df['price'].mean(),
            '价格中位数': self.df['price'].median(),
            '最高价格': self.df['price'].max(),
            '最低价格': self.df['price'].min(),
            '内存分布': self.df['memory'].value_counts().sort_index(),
            '存储容量分布': self.df['storage'].value_counts().sort_index(),
            '屏幕尺寸分布': self.df['screen_size'].value_counts().sort_index()
        }
        
        # 品牌平均价格
        brand_avg_price = self.df.groupby('brand')['price'].agg(['mean', 'count']).round(2)
        brand_avg_price.columns = ['平均价格', '数量']
        stats['品牌平均价格'] = brand_avg_price
        
        # 处理器与显卡组合分析
        proc_gpu_combo = self.df.groupby(['processor', 'gpu']).size().unstack(fill_value=0)
        stats['处理器与显卡组合'] = proc_gpu_combo
        
        return stats
    
    def save_processed_data(self, output_file):
        """保存处理后的数据"""
        self.df.to_csv(output_file, index=False, encoding='utf-8-sig')
        
def main():
    # 创建分析器实例
    analyzer = LaptopDataAnalyzer('jd_products_20250217_194405.csv')
    
    # 数据清理和转换
    print("正在清理价格数据...")
    analyzer.clean_price()
    
    print("正在提取笔记本信息...")
    analyzer.extract_laptop_info()
    
    # 数据分析
    print("\n开始分析数据...")
    stats = analyzer.analyze_data()
    
    # 打印分析结果
    print("\n=== 数据分析结果 ===")
    for key, value in stats.items():
        print(f"\n{key}:")
        print(value)
    
    # 保存处理后的数据
    output_file = f'processed_laptops_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    analyzer.save_processed_data(output_file)
    print(f"\n处理后的数据已保存到: {output_file}")
    
    # 额外的数据分析
    df = analyzer.df
    
    # 计算各品牌的市场份额
    market_share = (df['brand'].value_counts() / len(df) * 100).round(2)
    print("\n品牌市场份额（%）:")
    print(market_share)
    
    # 计算各处理器类型的平均价格
    proc_price = df.groupby('processor')['price'].mean().round(2).sort_values(ascending=False)
    print("\n各处理器类型平均价格:")
    print(proc_price)
    
    # 内存与价格的关系
    mem_price = df.groupby('memory')['price'].mean().round(2).sort_index()
    print("\n内存容量与平均价格的关系:")
    print(mem_price)
    
    # 高端机型分析（价格前20%的产品）
    high_end = df.nlargest(int(len(df) * 0.2), 'price')
    high_end_brands = high_end['brand'].value_counts()
    print("\n高端机型品牌分布:")
    print(high_end_brands)
    
    # 显卡与价格的关系
    gpu_price = df.groupby('gpu')['price'].agg(['mean', 'count']).round(2).sort_values('mean', ascending=False)
    print("\n显卡与价格的关系:")
    print(gpu_price)

if __name__ == "__main__":
    main() 