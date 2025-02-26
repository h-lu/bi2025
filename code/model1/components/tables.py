import streamlit as st
import pandas as pd
import numpy as np

def show_dataframe_info(df, title="数据预览"):
    """显示数据框的基本信息"""
    st.subheader(title)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**行数**: {df.shape[0]}")
        st.write(f"**列数**: {df.shape[1]}")
    
    with col2:
        # 计算内存使用
        memory_usage = df.memory_usage(deep=True).sum()
        if memory_usage < 1024:
            memory_str = f"{memory_usage} bytes"
        elif memory_usage < 1024 * 1024:
            memory_str = f"{memory_usage / 1024:.2f} KB"
        else:
            memory_str = f"{memory_usage / (1024 * 1024):.2f} MB"
        
        st.write(f"**内存使用**: {memory_str}")
        st.write(f"**重复行数**: {df.duplicated().sum()}")
    
    # 显示数据类型
    st.subheader("数据类型")
    dtypes = pd.DataFrame(df.dtypes, columns=["数据类型"])
    dtypes.index.name = "列名"
    dtypes = dtypes.reset_index()
    dtypes["非空值数"] = [df[col].count() for col in df.columns]
    dtypes["非空值百分比"] = [f"{df[col].count() / len(df) * 100:.2f}%" for col in df.columns]
    dtypes["唯一值数"] = [df[col].nunique() for col in df.columns]
    dtypes["示例值"] = [str(df[col].iloc[0]) if not df[col].empty and pd.notna(df[col].iloc[0]) else "N/A" for col in df.columns]
    
    st.dataframe(dtypes)

def show_data_with_filters(df, title="数据浏览", max_rows=1000):
    """显示带有筛选功能的数据表格"""
    st.subheader(title)
    
    # 创建筛选工具
    with st.expander("筛选选项"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # 列选择
            selected_columns = st.multiselect(
                "选择要显示的列",
                options=df.columns.tolist(),
                default=df.columns.tolist()
            )
        
        with col2:
            # 数值筛选
            numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
            if numeric_cols:
                filter_numeric = st.selectbox(
                    "按数值筛选 (可选)",
                    options=["无"] + numeric_cols
                )
                
                if filter_numeric != "无":
                    min_val = float(df[filter_numeric].min())
                    max_val = float(df[filter_numeric].max())
                    
                    filter_range = st.slider(
                        f"选择 {filter_numeric} 范围",
                        min_value=min_val,
                        max_value=max_val,
                        value=(min_val, max_val)
                    )
        
        with col3:
            # 类别筛选
            categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
            if categorical_cols:
                filter_categorical = st.selectbox(
                    "按类别筛选 (可选)",
                    options=["无"] + categorical_cols
                )
                
                if filter_categorical != "无":
                    categories = df[filter_categorical].dropna().unique().tolist()
                    selected_categories = st.multiselect(
                        f"选择 {filter_categorical} 类别",
                        options=categories,
                        default=categories
                    )
        
        # 搜索功能
        search_term = st.text_input("搜索 (在所有列中查找)", "")
    
    # 应用筛选
    filtered_df = df.copy()
    
    if 'selected_columns' in locals() and selected_columns:
        display_df = filtered_df[selected_columns]
    else:
        display_df = filtered_df
    
    if 'filter_numeric' in locals() and filter_numeric != "无":
        display_df = display_df[(display_df[filter_numeric] >= filter_range[0]) & 
                               (display_df[filter_numeric] <= filter_range[1])]
    
    if 'filter_categorical' in locals() and filter_categorical != "无" and selected_categories:
        display_df = display_df[display_df[filter_categorical].isin(selected_categories)]
    
    if search_term:
        # 在所有列中搜索
        mask = pd.Series(False, index=display_df.index)
        for col in display_df.columns:
            mask |= display_df[col].astype(str).str.contains(search_term, case=False, na=False)
        display_df = display_df[mask]
    
    # 显示结果数量
    st.write(f"显示 {len(display_df)} 行 (共 {len(df)} 行)")
    
    # 限制显示行数以提高性能
    if len(display_df) > max_rows:
        st.warning(f"为了提高性能，仅显示前 {max_rows} 行数据。")
        display_df = display_df.head(max_rows)
    
    # 显示数据
    st.dataframe(display_df)
    
    # 提供下载选项
    if not display_df.empty:
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="下载筛选后的数据为CSV",
            data=csv,
            file_name="filtered_data.csv",
            mime="text/csv",
        )

def show_summary_stats(df, columns=None, title="统计摘要"):
    """显示数值列的统计摘要"""
    st.subheader(title)
    
    # 选择要分析的列
    if columns is None:
        columns = df.select_dtypes(include=["number"]).columns.tolist()
    
    if not columns:
        st.warning("没有数值列可供分析")
        return
    
    # 计算统计量
    stats = df[columns].describe().T
    
    # 添加其他统计量
    stats["缺失值"] = df[columns].isna().sum()
    stats["缺失值比例"] = df[columns].isna().mean().round(4)
    stats["变异系数"] = (stats["std"] / stats["mean"]).abs().round(4)
    
    # 计算偏度和峰度
    if pd.__version__ >= "0.25.0":
        try:
            stats["偏度"] = df[columns].skew().round(4)
            stats["峰度"] = df[columns].kurtosis().round(4)
        except:
            pass
    
    # 重置索引
    stats = stats.reset_index()
    stats.columns = ["列名" if col == "index" else col for col in stats.columns]
    
    # 显示统计量
    st.dataframe(stats)

def show_correlation_table(df, columns=None, title="相关系数矩阵"):
    """显示相关系数表格"""
    st.subheader(title)
    
    # 选择要分析的列
    if columns is None:
        columns = df.select_dtypes(include=["number"]).columns.tolist()
    
    if not columns or len(columns) < 2:
        st.warning("至少需要2个数值列进行相关性分析")
        return
    
    # 计算相关系数
    corr = df[columns].corr().round(3)
    
    # 显示相关系数矩阵
    st.dataframe(corr)
    
    # 找出高度相关的变量对
    st.subheader("高度相关变量对")
    
    # 创建相关性对列表
    corr_pairs = []
    for i in range(len(columns)):
        for j in range(i+1, len(columns)):
            if i != j:
                col1, col2 = columns[i], columns[j]
                correlation = corr.loc[col1, col2]
                corr_pairs.append({
                    "变量1": col1,
                    "变量2": col2,
                    "相关系数": correlation,
                    "相关程度": "高" if abs(correlation) >= 0.7 else "中" if abs(correlation) >= 0.4 else "低"
                })
    
    # 转换为DataFrame并排序
    if corr_pairs:
        pairs_df = pd.DataFrame(corr_pairs)
        pairs_df = pairs_df.sort_values("相关系数", ascending=False)
        st.dataframe(pairs_df)
    else:
        st.write("没有变量对进行分析")

def show_category_breakdown(df, column, title=None, max_categories=10):
    """显示类别变量的明细分析"""
    if title is None:
        title = f"{column}类别分析"
    
    st.subheader(title)
    
    # 计算类别频数
    value_counts = df[column].value_counts()
    
    # 处理类别过多的情况
    if len(value_counts) > max_categories:
        top_n = value_counts.nlargest(max_categories - 1)
        others = pd.Series({"其他": value_counts.iloc[max_categories-1:].sum()})
        value_counts = pd.concat([top_n, others])
    
    # 转换为DataFrame
    counts_df = value_counts.reset_index()
    counts_df.columns = [column, "数量"]
    counts_df["百分比"] = (counts_df["数量"] / counts_df["数量"].sum() * 100).round(2).astype(str) + "%"
    
    # 显示频数表
    st.dataframe(counts_df)
    
    # 计算基本统计
    st.subheader("统计信息")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("唯一值数量", df[column].nunique())
    
    with col2:
        st.metric("最常见值", counts_df.iloc[0][column] if not counts_df.empty else "N/A")
    
    with col3:
        st.metric("缺失值百分比", f"{(df[column].isna().mean() * 100).round(2)}%")

def show_pivot_table(df, index_col, columns_col=None, values_col=None, aggfunc="mean", title="数据透视表"):
    """显示数据透视表"""
    st.subheader(title)
    
    # 设置默认值列为第一个数值列
    if values_col is None:
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        if numeric_cols:
            values_col = numeric_cols[0]
    
    # 生成透视表选项
    cols = st.columns(3)
    
    with cols[0]:
        selected_index = st.selectbox("行指标", options=df.columns, index=df.columns.get_loc(index_col) if index_col in df.columns else 0)
    
    with cols[1]:
        selected_columns = st.selectbox("列指标", options=["无"] + df.columns.tolist(), index=0 if columns_col is None else df.columns.get_loc(columns_col) + 1)
    
    with cols[2]:
        selected_values = st.selectbox("值", options=df.select_dtypes(include=["number"]).columns, index=df.select_dtypes(include=["number"]).columns.get_loc(values_col) if values_col in df.columns else 0)
    
    # 选择聚合函数
    agg_options = {
        "mean": "均值",
        "sum": "求和",
        "count": "计数",
        "min": "最小值",
        "max": "最大值"
    }
    
    selected_agg = st.selectbox(
        "聚合函数",
        options=list(agg_options.keys()),
        format_func=lambda x: agg_options[x],
        index=list(agg_options.keys()).index(aggfunc) if aggfunc in agg_options else 0
    )
    
    # 生成透视表
    try:
        if selected_columns == "无":
            # 只有行索引的透视表
            pivot = df.pivot_table(
                index=selected_index,
                values=selected_values,
                aggfunc=selected_agg
            )
        else:
            # 行列索引都有的透视表
            pivot = df.pivot_table(
                index=selected_index,
                columns=selected_columns,
                values=selected_values,
                aggfunc=selected_agg
            )
        
        # 显示透视表
        st.dataframe(pivot)
        
        # 提供下载选项
        csv = pivot.to_csv()
        st.download_button(
            label="下载透视表为CSV",
            data=csv,
            file_name="pivot_table.csv",
            mime="text/csv",
        )
    
    except Exception as e:
        st.error(f"生成透视表时出错: {e}")
        
def show_missing_data_analysis(df, title="缺失值分析"):
    """显示缺失值分析"""
    st.subheader(title)
    
    # 计算每列的缺失值
    missing = df.isna().sum().to_frame("缺失值数量")
    missing["缺失值百分比"] = (df.isna().mean() * 100).round(2)
    missing = missing.sort_values("缺失值数量", ascending=False)
    missing = missing.reset_index()
    missing.columns = ["列名", "缺失值数量", "缺失值百分比(%)"]
    
    # 仅保留有缺失值的列
    missing_cols = missing[missing["缺失值数量"] > 0]
    
    if missing_cols.empty:
        st.success("数据中没有缺失值！")
        return
    
    # 显示缺失值统计
    st.dataframe(missing_cols)
    
    # 缺失值可视化
    if len(missing_cols) > 0:
        st.subheader("缺失值模式")
        
        # 绘制缺失值热图
        fig, ax = plt.subplots(figsize=(10, 6))
        cols_with_missing = missing_cols["列名"].tolist()
        msno.matrix(df[cols_with_missing], figsize=(10, 6), ax=ax)
        st.pyplot(fig)
        
        # 缺失值相关性
        if len(cols_with_missing) >= 2:
            st.subheader("缺失值相关性")
            fig, ax = plt.subplots(figsize=(10, 8))
            msno.heatmap(df[cols_with_missing], ax=ax)
            st.pyplot(fig)

# 如果使用缺失值分析功能，需要导入
import matplotlib.pyplot as plt
import missingno as msno 