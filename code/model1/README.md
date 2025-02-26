# 商业智能数据采集与预处理应用

这是一个基于Streamlit开发的交互式应用，用于展示数据采集与预处理模块的主要内容，包括数据源、网络爬虫、数据清洗、文本处理和数据可视化等内容。

## 功能特点

- **模块化架构**：采用模块化设计，每个功能分离为独立模块，便于维护和扩展
- **多页面导航**：通过侧边栏轻松切换不同主题
- **交互式演示**：展示爬虫、数据处理和分析的实际效果
- **代码示例**：提供各种技术的代码示例
- **数据可视化**：使用Plotly和Matplotlib进行各类数据可视化
- **模拟数据**：使用模拟数据展示完整的数据分析流程

## 目录结构

```
code/model1/
├── app.py                 # 主应用入口
├── README.md              # 项目说明文档
├── requirements.txt       # 依赖包列表
├── pages/                 # 页面模块目录
│   ├── __init__.py
│   ├── home.py            # 首页模块
│   ├── data_sources.py    # 数据源模块
│   ├── web_scraping_basics.py  # 爬虫基础模块
│   ├── advanced_scraping.py    # 高级爬虫模块
│   ├── dynamic_scraping.py     # 动态网页抓取模块
│   ├── data_cleaning.py        # 数据清洗模块
│   ├── text_processing.py      # 文本处理模块
│   ├── data_visualization.py   # 数据可视化模块
│   └── project_demo.py         # 项目演示模块
├── utils/                 # 工具类目录
│   ├── __init__.py
│   └── helpers.py         # 辅助函数
├── data/                  # 数据目录
└── mock_html/             # 模拟HTML文件目录
    ├── mock_shop.html          # 电商网站模拟
    ├── product_reviews.html    # 产品评论页面模拟
    ├── news_site.html          # 新闻网站模拟
    └── api_response.json       # API响应模拟
```

## 安装方法

1. 确保已安装Python 3.8或更高版本
2. 克隆或下载此仓库
3. 安装必要的依赖：

```bash
pip install -r requirements.txt
```

## 运行应用

```bash
streamlit run app.py
```

## 应用内容

应用包含以下几个主要部分：

1. **首页**：模块概述和学习目标
2. **数据源**：介绍不同类型的数据源
3. **网络爬虫基础**：展示使用Requests和BeautifulSoup进行基础爬虫
4. **高级爬虫技术**：介绍Scrapy框架的使用
5. **动态网页抓取**：展示使用Playwright抓取动态网页
6. **数据清洗与转换**：演示数据清洗流程
7. **文本处理**：展示文本处理和简单情感分析
8. **数据可视化**：展示多种数据可视化技术和最佳实践
9. **项目演示**：综合展示电商产品数据采集与分析

## 技术栈

- **Streamlit**: 应用框架
- **Pandas & NumPy**: 数据处理
- **Matplotlib & Plotly**: 数据可视化
- **Requests & BeautifulSoup**: 网页抓取
- **Jieba**: 中文分词

## 注意事项

- 本应用使用模拟数据，实际项目中需要从真实数据源采集数据
- 在进行网络爬虫时，请尊重网站的robots.txt规则，遵守合法、合理的访问方式
- 对于生产环境，请考虑更完善的错误处理和性能优化

## 扩展建议

- 添加实际网站抓取示例（注意合规性）
- 集成更高级的NLP模型
- 加入数据库访问示例
- 增加机器学习模型用于预测分析

## 许可

本项目仅用于教学目的，请勿用于商业用途。 