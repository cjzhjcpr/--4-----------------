import Ind
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression as LR

# 获取投资组合所有股票交易数据
stkdata = pd.read_excel('stkdata.xlsx')

# 确保数据中没有空值
stkdata.dropna(inplace=True)

# 获取投资组合所有股票代码列表
codelist = stkdata['ts_code'].unique().tolist()
r_total = 0  # 预定义投资组合收益率

# 对每一只股票交易数据计算技术分析指标（自变量）和涨跌趋势指标（因变量），并
# 划分训练和测试样本，利用逻辑回归模型预测及计算收益率
for code in codelist:
    data = stkdata[stkdata['ts_code'] == code]

    # 检查数据长度是否足够
    if len(data) < 50:  # 例如，至少需要50天的数据
        print(f"Skipping {code} due to insufficient data length")
        continue

    try:
        MA = Ind.MA(data, 5, 10, 20)
        macd = Ind.MACD(data)
        kdj = Ind.KDJ(data, 9)
        if kdj is None:
            print(f"Skipping {code} due to insufficient data for KDJ calculation")
            continue
        rsi6 = Ind.RSI(data, 6)
        rsi12 = Ind.RSI(data, 12)
        rsi24 = Ind.RSI(data, 24)
        bias5 = Ind.BIAS(data, 5)
        bias10 = Ind.BIAS(data, 10)
        bias20 = Ind.BIAS(data, 20)
        obv = Ind.OBV(data)
        y = Ind.cla(data)
    except KeyError as e:
        print(f"Error calculating indicators for {code}: {e}")
        continue

    # 交易日期、技术指标、涨跌趋势指标合并为一个数据Data
    tdate = {'交易日期': data['trade_date'].values}
    tdate = pd.DataFrame(tdate)
    Indicator = {
        'MA5': MA[0], 'MA10': MA[1], 'MA20': MA[2], 'MACD': macd,
        'K': kdj[0], 'D': kdj[1], 'J': kdj[2], 'RSI6': rsi6, 'RSI12': rsi12,
        'RSI24': rsi24, 'BIAS5': bias5, 'BIAS10': bias10, 'BIAS20': bias20, 'OBV': obv
    }
    Indicator = pd.DataFrame(Indicator)
    tempdata = tdate.join(Indicator)
    Y = {'涨跌趋势': y}
    Y = pd.DataFrame(Y)
    Data = tempdata.join(Y)
    Data = Data.dropna()  # 去掉空值
    Data = Data[Data.iloc[:, 6].values != 0]  # 去掉第6列为0的数据

    # 训练和预测数据划分
    x1 = Data['交易日期'].values >= 20170101
    x2 = Data['交易日期'].values <= 20171031
    index = x1 & x2
    x_train = Data.iloc[index, 1:15]
    y_train = Data.iloc[index, [15]]
    x_test = Data.iloc[~index, 1:15]
    y_test = Data.iloc[~index, [15]]

    # 检查训练数据是否为空
    if x_train.empty or y_train.empty:
        print(f"Skipping {code} due to empty training data")
        continue

    # 数据标准化
    scaler = StandardScaler()
    scaler.fit(x_train)
    x_train = scaler.transform(x_train)
    x_test = scaler.transform(x_test)

    # 逻辑回归模型
    clf = LR()
    clf.fit(x_train, y_train.values.ravel())  # 使用 ravel() 将 y_train 转换为 1D 数组
    result = clf.predict(x_test)  # 预测结果
    sc = clf.score(x_train, y_train)  # 模型准确率

    result = pd.DataFrame(result)  # 预测结果转换为数据框
    ff = Data.iloc[~index, 0]  # 提取预测样本的交易日期
    # 将预测结果与实际结果整合在一起，进行比较
    pm1 = {'交易日期': ff.values, '预测结果': result.iloc[:, 0].values, '实际结果': y_test.iloc[:, 0].values}
    result1 = pd.DataFrame(pm1)
    z = result1['预测结果'].values - result1['实际结果'].values
    R = len(z[z == 0]) / len(z)  # 预测准确率

    if sc > 0.7:
        r_list = []
        for t in range(len(result1) - 1):
            if result1['预测结果'].values[t] == 1:
                p2 = data.loc[data['trade_date'].values == result1['交易日期'].values[t + 1], 'close'].values
                p1 = data.loc[data['trade_date'].values == result1['交易日期'].values[t + 1], 'open'].values
                r = (p2 - p1) / p1
                r_list.append(r)
        r_stk = sum(r_list)
        r_total = r_total + r_stk

        print(f"{code} : {r_stk}")

print(f"投资组合收益率： {r_total}")

# 沪深300指数收益率计算
hs300 = pd.read_excel('hs300.xlsx')
x1 = hs300['trade_date'].values >= 20171101
x2 = hs300['trade_date'].values <= 20171231
index = x1 & x2
p = hs300.iloc[index, 2].values
r_hs300 = (p[-1] - p[0]) / p[0]
print(f"沪深300同期收益率： {r_hs300}")