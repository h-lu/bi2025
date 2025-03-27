# 商务智能课程 - Quarto Book

这是一个基于Quarto的《商务智能》课程电子书项目，适用于研究生教学。

## 内容介绍

本书集合了商务智能课程的理论知识和Python实践案例，包括：

- 泰坦尼克生存预测分析
- 房价预测分析

## 如何使用

### 环境要求

- 安装 [Quarto](https://quarto.org/docs/get-started/)
- 安装 Python 及相关依赖包

### 构建书籍

在项目根目录运行以下命令：

```bash
quarto render
```

生成的书籍将位于 `docs/` 目录中。

### 实时预览

在开发过程中，可以使用以下命令实时预览：

```bash
quarto preview
```

## 项目结构

- `_quarto.yml`: Quarto配置文件
- `index.qmd`: 书籍首页
- `泰坦尼克生存预测.qmd`: 泰坦尼克号生存预测案例
- `房价预测分析.qmd`: 房价预测分析案例
- `docs/`: 生成的书籍输出目录 