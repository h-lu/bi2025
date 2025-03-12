import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

# 尝试导入统计和机器学习库，如果不可用则跳过
try:
    from statsmodels.tsa.seasonal import seasonal_decompose
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
    import pmdarima as pm
    from sklearn.metrics import mean_absolute_error, mean_squared_error
    from prophet import Prophet
    import matplotlib.pyplot as plt
    ADVANCED_MODELS_AVAILABLE = True
except ImportError:
    ADVANCED_MODELS_AVAILABLE = False

def forecast_sales(data):
    """
    执行销售预测分析
    
    Args:
        data (dict): 包含所有数据集的字典
    """
    st.subheader("销售预测分析")
    
    # 检查是否有必要的库
    if not ADVANCED_MODELS_AVAILABLE:
        st.warning("""
        高级预测模型所需的一些库未安装。为使用全部功能，请安装以下库:
        - statsmodels
        - pmdarima
        - sklearn
        - prophet
        - matplotlib
        
        你可以通过运行以下命令进行安装:
        ```
        pip install statsmodels pmdarima scikit-learn prophet matplotlib
        ```
        """)
    
    # 准备数据
    transactions_df = data["transactions"]
    
    # 确保日期格式正确
    transactions_df['date'] = pd.to_datetime(transactions_df['date'])
    
    # 聚合数据
    # 按日期汇总销售数据
    daily_sales = transactions_df.groupby('date')['total_amount'].sum().reset_index()
    daily_sales = daily_sales.sort_values('date')
    
    # 计算一些派生特征
    daily_sales['day_of_week'] = daily_sales['date'].dt.dayofweek
    daily_sales['month'] = daily_sales['date'].dt.month
    daily_sales['year'] = daily_sales['date'].dt.year
    daily_sales['is_weekend'] = daily_sales['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
    
    # 显示时间序列数据
    st.write("### 历史销售趋势")
    
    # 创建每日销售趋势图
    fig1 = px.line(
        daily_sales,
        x='date',
        y='total_amount',
        title='每日销售趋势',
        labels={'date': '日期', 'total_amount': '销售金额'}
    )
    
    st.plotly_chart(fig1, use_container_width=True)
    
    # 按月汇总
    monthly_sales = daily_sales.groupby([daily_sales['year'], daily_sales['month']])['total_amount'].sum().reset_index()
    monthly_sales['date'] = pd.to_datetime(monthly_sales[['year', 'month']].assign(day=1))
    monthly_sales['month_name'] = monthly_sales['date'].dt.strftime('%Y-%m')
    
    # 创建月度销售趋势图
    fig2 = px.bar(
        monthly_sales,
        x='month_name',
        y='total_amount',
        title='月度销售趋势',
        labels={'month_name': '月份', 'total_amount': '销售金额'}
    )
    
    # 添加趋势线
    fig2.add_trace(
        go.Scatter(
            x=monthly_sales['month_name'],
            y=monthly_sales['total_amount'].rolling(window=3).mean(),
            mode='lines',
            name='3个月移动平均',
            line=dict(color='red', width=2)
        )
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # 销售模式分析
    st.write("### 销售模式分析")
    
    # 按周几分析
    weekday_sales = daily_sales.groupby('day_of_week')['total_amount'].agg(['mean', 'sum']).reset_index()
    weekday_sales['day_name'] = weekday_sales['day_of_week'].apply(lambda x: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][x])
    
    # 创建周几销售分布图
    fig3 = px.bar(
        weekday_sales,
        x='day_name',
        y='mean',
        title='平均每日销售额（按周几）',
        labels={'day_name': '星期', 'mean': '平均销售额'}
    )
    
    # 按月份分析
    monthly_pattern = daily_sales.groupby('month')['total_amount'].mean().reset_index()
    month_names = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月']
    monthly_pattern['month_name'] = monthly_pattern['month'].apply(lambda x: month_names[x-1])
    
    # 创建月份销售分布图
    fig4 = px.bar(
        monthly_pattern,
        x='month_name',
        y='total_amount',
        title='平均每日销售额（按月份）',
        labels={'month_name': '月份', 'total_amount': '平均销售额'}
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        st.plotly_chart(fig4, use_container_width=True)
    
    # 季节性分解
    st.write("### 时间序列分解")
    
    if ADVANCED_MODELS_AVAILABLE and len(monthly_sales) >= 12:
        # 创建时间序列对象
        ts_data = monthly_sales.set_index('date')['total_amount']
        
        # 执行季节性分解
        try:
            decomposition = seasonal_decompose(ts_data, model='additive', period=12)
            
            # 创建分解图表
            fig5 = make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.05)
            
            # 原始数据
            fig5.add_trace(
                go.Scatter(x=decomposition.observed.index, y=decomposition.observed, mode='lines', name='观测值'),
                row=1, col=1
            )
            
            # 趋势
            fig5.add_trace(
                go.Scatter(x=decomposition.trend.index, y=decomposition.trend, mode='lines', name='趋势'),
                row=2, col=1
            )
            
            # 季节性
            fig5.add_trace(
                go.Scatter(x=decomposition.seasonal.index, y=decomposition.seasonal, mode='lines', name='季节性'),
                row=3, col=1
            )
            
            # 残差
            fig5.add_trace(
                go.Scatter(x=decomposition.resid.index, y=decomposition.resid, mode='lines', name='残差'),
                row=4, col=1
            )
            
            # 更新布局
            fig5.update_layout(
                height=800,
                title_text='销售时间序列分解',
                showlegend=False
            )
            
            st.plotly_chart(fig5, use_container_width=True)
            
            # 分解解释
            st.markdown("""
            **时间序列分解解释：**
            
            - **观测值**：原始月度销售数据
            - **趋势**：长期销售增长或下降的模式
            - **季节性**：周期性重复的销售模式，如每年特定月份的销售高峰或低谷
            - **残差**：无法通过趋势或季节性解释的随机波动
            
            分解有助于理解销售的基本模式，为预测提供依据。
            """)
        except Exception as e:
            st.error(f"执行时间序列分解时出错: {str(e)}")
    else:
        st.info("需要至少12个月的数据才能进行有意义的季节性分解，或者需要安装statsmodels库。")
    
    # 销售影响因素分析
    st.write("### 销售影响因素分析")
    
    # 合并促销活动数据
    if "marketing" in data:
        marketing_df = data["marketing"]
        marketing_df['start_date'] = pd.to_datetime(marketing_df['start_date'])
        marketing_df['end_date'] = pd.to_datetime(marketing_df['end_date'])
        
        # 创建一个日期范围内的营销活动标记
        date_range = pd.date_range(start=daily_sales['date'].min(), end=daily_sales['date'].max())
        campaign_dates = pd.DataFrame({'date': date_range})
        
        # 标记每一天是否有活动
        campaign_dates['has_campaign'] = 0
        
        for _, campaign in marketing_df.iterrows():
            mask = (campaign_dates['date'] >= campaign['start_date']) & (campaign_dates['date'] <= campaign['end_date'])
            campaign_dates.loc[mask, 'has_campaign'] = 1
        
        # 合并销售数据和活动数据
        sales_with_campaigns = daily_sales.merge(campaign_dates, on='date', how='left')
        
        # 分析有无活动的销售差异
        campaign_effect = sales_with_campaigns.groupby('has_campaign')['total_amount'].mean().reset_index()
        campaign_effect['status'] = campaign_effect['has_campaign'].apply(lambda x: '有营销活动' if x == 1 else '无营销活动')
        
        # 创建活动影响图表
        fig6 = px.bar(
            campaign_effect,
            x='status',
            y='total_amount',
            title='营销活动对日均销售额的影响',
            labels={'status': '状态', 'total_amount': '平均日销售额'}
        )
        
        st.plotly_chart(fig6, use_container_width=True)
        
        # 计算提升效果
        no_campaign = campaign_effect[campaign_effect['has_campaign'] == 0]['total_amount'].values[0]
        with_campaign = campaign_effect[campaign_effect['has_campaign'] == 1]['total_amount'].values[0]
        lift = (with_campaign - no_campaign) / no_campaign * 100 if no_campaign > 0 else 0
        
        st.metric("营销活动销售提升效果", f"{lift:.1f}%")
    
    # 销售预测
    st.write("### 销售预测模型")
    
    # 选择预测方法
    forecast_method = st.selectbox(
        "选择预测方法",
        options=["简单移动平均", "加权移动平均", "指数平滑", "SARIMA", "Prophet"] if ADVANCED_MODELS_AVAILABLE else ["简单移动平均", "加权移动平均", "指数平滑"],
        index=0
    )
    
    # 选择预测时间范围
    forecast_periods = st.slider(
        "预测未来月数",
        min_value=1,
        max_value=12,
        value=3
    )
    
    # 准备预测数据
    forecast_data = monthly_sales[['date', 'total_amount']].copy()
    
    # 进行预测
    if forecast_method == "简单移动平均":
        # 选择窗口大小
        window_size = st.slider("选择移动平均窗口大小", min_value=1, max_value=6, value=3)
        
        # 计算移动平均
        forecast_data['forecast'] = forecast_data['total_amount'].rolling(window=window_size).mean()
        
        # 预测未来值
        last_window = forecast_data['total_amount'].iloc[-window_size:].values
        future_dates = pd.date_range(start=forecast_data['date'].iloc[-1] + pd.DateOffset(months=1), periods=forecast_periods, freq='MS')
        
        future_predictions = []
        for _ in range(forecast_periods):
            next_value = last_window.mean()
            future_predictions.append(next_value)
            last_window = np.roll(last_window, -1)
            last_window[-1] = next_value
        
        future_df = pd.DataFrame({
            'date': future_dates,
            'total_amount': [None] * forecast_periods,
            'forecast': future_predictions
        })
        
        # 合并历史和预测数据
        forecast_result = pd.concat([forecast_data, future_df])
        
    elif forecast_method == "加权移动平均":
        # 使用递减权重
        weights = [0.5, 0.3, 0.2]  # 权重必须总和为1
        weights = weights[::-1]  # 反转权重，使最近的观测值权重最高
        
        # 计算加权移动平均
        for i in range(len(weights), len(forecast_data)):
            weighted_sum = 0
            for j, weight in enumerate(weights):
                weighted_sum += forecast_data['total_amount'].iloc[i-j-1] * weight
            forecast_data.loc[forecast_data.index[i], 'forecast'] = weighted_sum
        
        # 预测未来值
        last_values = forecast_data['total_amount'].iloc[-len(weights):].values
        future_dates = pd.date_range(start=forecast_data['date'].iloc[-1] + pd.DateOffset(months=1), periods=forecast_periods, freq='MS')
        
        future_predictions = []
        for _ in range(forecast_periods):
            weighted_sum = 0
            for j, weight in enumerate(weights):
                weighted_sum += last_values[j] * weight
            future_predictions.append(weighted_sum)
            last_values = np.roll(last_values, -1)
            last_values[-1] = weighted_sum
        
        future_df = pd.DataFrame({
            'date': future_dates,
            'total_amount': [None] * forecast_periods,
            'forecast': future_predictions
        })
        
        # 合并历史和预测数据
        forecast_result = pd.concat([forecast_data, future_df])
        
    elif forecast_method == "指数平滑":
        # 选择平滑因子
        alpha = st.slider("选择平滑因子 (α)", min_value=0.1, max_value=0.9, value=0.3, step=0.1)
        
        # 计算指数平滑
        forecast_data['forecast'] = None
        forecast_data.loc[forecast_data.index[0], 'forecast'] = forecast_data['total_amount'].iloc[0]
        
        for i in range(1, len(forecast_data)):
            prev_forecast = forecast_data['forecast'].iloc[i-1]
            prev_actual = forecast_data['total_amount'].iloc[i-1]
            forecast_data.loc[forecast_data.index[i], 'forecast'] = alpha * prev_actual + (1 - alpha) * prev_forecast
        
        # 预测未来值
        last_forecast = forecast_data['forecast'].iloc[-1]
        future_dates = pd.date_range(start=forecast_data['date'].iloc[-1] + pd.DateOffset(months=1), periods=forecast_periods, freq='MS')
        
        # 对于简单指数平滑，所有未来预测值都等于最后的平滑值
        future_df = pd.DataFrame({
            'date': future_dates,
            'total_amount': [None] * forecast_periods,
            'forecast': [last_forecast] * forecast_periods
        })
        
        # 合并历史和预测数据
        forecast_result = pd.concat([forecast_data, future_df])
        
    elif forecast_method == "SARIMA" and ADVANCED_MODELS_AVAILABLE:
        try:
            # 准备数据
            ts_data = forecast_data.set_index('date')['total_amount']
            
            # 自动选择最佳SARIMA参数
            auto_model = pm.auto_arima(
                ts_data,
                seasonal=True,
                m=12,  # 月度数据的季节性周期
                d=None,  # 自动确定差分阶数
                D=None,  # 自动确定季节性差分阶数
                start_p=0, max_p=3,
                start_q=0, max_q=3,
                start_P=0, max_P=2,
                start_Q=0, max_Q=2,
                information_criterion='aic',
                trace=False,
                error_action='ignore',
                suppress_warnings=True,
                stepwise=True
            )
            
            # 显示模型参数
            model_order = auto_model.order
            seasonal_order = auto_model.seasonal_order
            st.info(f"最佳SARIMA模型: SARIMA{model_order}{seasonal_order}")
            
            # 拟合模型
            model = SARIMAX(
                ts_data,
                order=model_order,
                seasonal_order=seasonal_order,
                enforce_stationarity=False,
                enforce_invertibility=False
            )
            
            model_fit = model.fit(disp=False)
            
            # 预测
            forecast = model_fit.forecast(steps=forecast_periods)
            
            # 准备预测结果
            forecast_data['forecast'] = model_fit.fittedvalues
            
            future_dates = pd.date_range(start=forecast_data['date'].iloc[-1] + pd.DateOffset(months=1), periods=forecast_periods, freq='MS')
            
            future_df = pd.DataFrame({
                'date': future_dates,
                'total_amount': [None] * forecast_periods,
                'forecast': forecast.values
            })
            
            # 合并历史和预测数据
            forecast_result = pd.concat([forecast_data, future_df])
            
        except Exception as e:
            st.error(f"SARIMA预测出错: {str(e)}")
            # 如果SARIMA失败，回退到简单移动平均
            forecast_method = "简单移动平均"
            st.warning(f"回退到简单移动平均方法")
            
            # 计算移动平均
            window_size = 3
            forecast_data['forecast'] = forecast_data['total_amount'].rolling(window=window_size).mean()
            
            # 预测未来值
            last_window = forecast_data['total_amount'].iloc[-window_size:].values
            future_dates = pd.date_range(start=forecast_data['date'].iloc[-1] + pd.DateOffset(months=1), periods=forecast_periods, freq='MS')
            
            future_predictions = []
            for _ in range(forecast_periods):
                next_value = last_window.mean()
                future_predictions.append(next_value)
                last_window = np.roll(last_window, -1)
                last_window[-1] = next_value
            
            future_df = pd.DataFrame({
                'date': future_dates,
                'total_amount': [None] * forecast_periods,
                'forecast': future_predictions
            })
            
            # 合并历史和预测数据
            forecast_result = pd.concat([forecast_data, future_df])
    
    elif forecast_method == "Prophet" and ADVANCED_MODELS_AVAILABLE:
        try:
            # 准备Prophet所需的数据格式
            prophet_data = forecast_data[['date', 'total_amount']].rename(columns={'date': 'ds', 'total_amount': 'y'})
            
            # 创建和拟合模型
            model = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=False,
                daily_seasonality=False,
                seasonality_mode='additive',
                interval_width=0.95
            )
            
            # 添加月度季节性
            model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
            
            # 拟合模型
            model.fit(prophet_data)
            
            # 创建未来日期
            future = model.make_future_dataframe(periods=forecast_periods, freq='MS')
            
            # 预测
            forecast = model.predict(future)
            
            # 将预测结果合并到原始数据
            forecast_result = pd.DataFrame({
                'date': forecast['ds'],
                'total_amount': prophet_data['y'].reindex(prophet_data.index.union(forecast.index[-forecast_periods:])),
                'forecast': forecast['yhat']
            })
            
        except Exception as e:
            st.error(f"Prophet预测出错: {str(e)}")
            # 如果Prophet失败，回退到简单移动平均
            forecast_method = "简单移动平均"
            st.warning(f"回退到简单移动平均方法")
            
            # 计算移动平均
            window_size = 3
            forecast_data['forecast'] = forecast_data['total_amount'].rolling(window=window_size).mean()
            
            # 预测未来值
            last_window = forecast_data['total_amount'].iloc[-window_size:].values
            future_dates = pd.date_range(start=forecast_data['date'].iloc[-1] + pd.DateOffset(months=1), periods=forecast_periods, freq='MS')
            
            future_predictions = []
            for _ in range(forecast_periods):
                next_value = last_window.mean()
                future_predictions.append(next_value)
                last_window = np.roll(last_window, -1)
                last_window[-1] = next_value
            
            future_df = pd.DataFrame({
                'date': future_dates,
                'total_amount': [None] * forecast_periods,
                'forecast': future_predictions
            })
            
            # 合并历史和预测数据
            forecast_result = pd.concat([forecast_data, future_df])
    
    else:
        # 默认回退到简单移动平均
        st.warning(f"所选方法不可用，回退到简单移动平均")
        
        # 计算移动平均
        window_size = 3
        forecast_data['forecast'] = forecast_data['total_amount'].rolling(window=window_size).mean()
        
        # 预测未来值
        last_window = forecast_data['total_amount'].iloc[-window_size:].values
        future_dates = pd.date_range(start=forecast_data['date'].iloc[-1] + pd.DateOffset(months=1), periods=forecast_periods, freq='MS')
        
        future_predictions = []
        for _ in range(forecast_periods):
            next_value = last_window.mean()
            future_predictions.append(next_value)
            last_window = np.roll(last_window, -1)
            last_window[-1] = next_value
        
        future_df = pd.DataFrame({
            'date': future_dates,
            'total_amount': [None] * forecast_periods,
            'forecast': future_predictions
        })
        
        # 合并历史和预测数据
        forecast_result = pd.concat([forecast_data, future_df])
    
    # 格式化日期为月份名称
    forecast_result['month_name'] = forecast_result['date'].dt.strftime('%Y-%m')
    
    # 创建预测图表
    try:
        # 确保数据类型一致，将数据转换为同样的类型
        for col in ['total_amount', 'forecast']:
            if col in forecast_result.columns:
                forecast_result[col] = pd.to_numeric(forecast_result[col], errors='coerce')
        
        # 使用px.line创建图表，但确保数据类型一致
        fig7 = px.line(
            forecast_result,
            x='month_name',
            y=['total_amount', 'forecast'],
            title=f'销售预测 - {forecast_method}方法',
            labels={'value': '销售额', 'month_name': '月份', 'variable': '数据类型'},
            color_discrete_map={'total_amount': 'blue', 'forecast': 'red'}
        )
        
        # 添加预测区域标记
        last_historical_date = forecast_data['date'].iloc[-1]
        forecast_start_idx = forecast_result[forecast_result['date'] > last_historical_date].index.min()
        
        if forecast_start_idx is not None:
            try:
                # 确保forecast_start是数值型数据
                forecast_start = forecast_result.index[forecast_start_idx]  # 使用索引而不是字符串
                
                fig7.add_vline(
                    x=forecast_start,
                    line_dash="dash",
                    line_color="green",
                    annotation_text="预测开始",
                    annotation_position="top"
                )
            except Exception as e:
                st.warning(f"添加预测标记线时出错: {e}")
        
        st.plotly_chart(fig7, use_container_width=True)
    except Exception as e:
        st.error(f"创建预测图表时出错: {e}")
        # 如果出错，显示数据框架
        st.write("预测结果：")
        st.dataframe(forecast_result)
    
    # 计算预测表现指标（仅对历史部分）
    historical_data = forecast_result[~forecast_result['total_amount'].isna()]
    
    # 设置默认值
    mae = 0
    mape = 0
    rmse = 0
    
    if len(historical_data) > 0 and 'forecast' in historical_data.columns:
        actual = historical_data['total_amount'].values
        predicted = historical_data['forecast'].dropna().values
        
        if len(actual) == len(predicted) and len(actual) > 0:
            try:
                # 计算预测误差
                mae = np.mean(np.abs(actual - predicted))
                # 避免除零错误
                mape = np.mean(np.abs((actual - predicted) / np.maximum(actual, 0.0001))) * 100
                rmse = np.sqrt(np.mean((actual - predicted) ** 2))
            except Exception as e:
                st.warning(f"计算预测指标时出错: {e}")
    
    # 显示预测误差
    st.write("### 预测准确性指标 (历史数据)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("平均绝对误差 (MAE)", f"¥{mae:.2f}")
    
    with col2:
        st.metric("平均绝对百分比误差 (MAPE)", f"{mape:.2f}%")
    
    with col3:
        st.metric("均方根误差 (RMSE)", f"¥{rmse:.2f}")
    
    # 显示预测结果表格
    st.write("### 预测结果表格")
    
    forecast_table = forecast_result.iloc[-forecast_periods-6:].copy()  # 显示最后6个历史月份和预测月份
    forecast_table['year'] = forecast_table['date'].dt.year
    forecast_table['month'] = forecast_table['date'].dt.month
    forecast_table = forecast_table[['year', 'month', 'month_name', 'total_amount', 'forecast']]
    forecast_table.columns = ['年份', '月份', '年月', '实际销售额', '预测销售额']
    
    # 标记预测部分
    forecast_table['是否预测'] = forecast_table['实际销售额'].isna()
    
    st.dataframe(forecast_table.drop(columns=['是否预测']))
    
    # 计算预测总销售额
    predicted_total = forecast_result[forecast_result['total_amount'].isna()]['forecast'].sum()
    last_periods_total = forecast_data['total_amount'].iloc[-forecast_periods:].sum()
    
    growth_rate = (predicted_total - last_periods_total) / last_periods_total * 100 if last_periods_total > 0 else 0
    
    st.metric(
        f"预测未来{forecast_periods}个月总销售额", 
        f"¥{predicted_total:,.2f}", 
        f"{growth_rate:+.1f}% vs 前{forecast_periods}个月"
    )
    
    # 预测总结与建议
    st.write("### 预测总结与建议")
    
    # 分析预测趋势
    forecast_trend = "上升" if growth_rate > 5 else ("下降" if growth_rate < -5 else "平稳")
    
    # 季节性分析
    high_seasons = monthly_pattern.sort_values('total_amount', ascending=False)['month_name'].iloc[:3].tolist()
    low_seasons = monthly_pattern.sort_values('total_amount')['month_name'].iloc[:3].tolist()
    
    # 生成预测总结
    st.markdown(f"""
    #### 预测总结:
    
    预测表明，未来{forecast_periods}个月的销售趋势将呈现**{forecast_trend}**趋势，与前{forecast_periods}个月相比预计变化**{growth_rate:.1f}%**。
    
    **季节性特征:**
    - 历史销售高峰月份: {', '.join(high_seasons)}
    - 历史销售低谷月份: {', '.join(low_seasons)}
    
    **预测表现:**
    预测模型在历史数据上的MAPE为{mape:.2f}%，表明预测的总体准确度{('非常高' if mape < 10 else ('高' if mape < 20 else ('一般' if mape < 30 else '较低')))}。
    """)
    
    # 生成业务建议
    st.markdown("""
    #### 业务建议:
    
    **库存管理建议:**
    - 根据预测销售趋势，及时调整库存水平
    - 在销售高峰前增加库存，在低谷期减少库存
    - 关注预测误差，为核心产品保留安全库存
    
    **营销策略建议:**
    - 在预计销售下降的月份加大促销力度
    - 利用销售高峰期最大化利润而非促销
    - 关注季节性模式，针对不同月份制定不同的营销活动
    
    **资源分配建议:**
    - 根据预测的销售趋势调整人力资源安排
    - 根据预期销售高峰优化供应链管理
    - 提前做好资金规划，确保在需求高峰时有足够的流动资金
    """)
    
    # 影响预测的关键因素
    st.markdown("""
    #### 影响预测的关键因素:
    
    1. **季节性因素**: 月度和季度的销售循环模式
    2. **营销活动**: 促销和广告活动对销售的短期和长期影响
    3. **市场趋势**: 整体市场需求的变化
    4. **产品生命周期**: 新产品推出和老产品衰退的节奏
    5. **竞争因素**: 竞争对手的活动和市场份额变化
    
    *注: 本预测基于历史数据模式，不能完全预测突发事件或重大市场变化带来的影响。建议定期更新预测并结合业务判断使用。*
    """) 