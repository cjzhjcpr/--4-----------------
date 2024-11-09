# -*- coding: utf-8 -*-
import Ind
import pandas as pd

# 读取数据
data = pd.read_excel('dta.xlsx')

# 检查并处理原始数据中的 NaN 值
if data.isnull().values.any():
    print("原始数据中存在 NaN 值，进行填充处理")
    data = data.fillna(method='ffill').fillna(method='bfill')

# 计算技术指标
MA = Ind.MA(data, 5, 10, 20)
macd = Ind.MACD(data)
kdj = Ind.KDJ(data, 9)
rsi6 = Ind.RSI(data, 6)
rsi12 = Ind.RSI(data, 12)
rsi24 = Ind.RSI(data, 24)
bias5 = Ind.BIAS(data, 5)
bias10 = Ind.BIAS(data, 10)
bias20 = Ind.BIAS(data, 20)
obv = Ind.OBV(data)
y = Ind.cla(data)

# 检查并处理技术指标中的 NaN 值
MA = [ma.ffill().bfill() for ma in MA]
macd = macd.ffill().bfill()
kdj = [pd.Series(k).ffill().bfill() for k in kdj]
rsi6 = rsi6.ffill().bfill()
rsi12 = rsi12.ffill().bfill()
rsi24 = rsi24.ffill().bfill()
bias5 = bias5.ffill().bfill()
bias10 = bias10.ffill().bfill()
bias20 = bias20.ffill().bfill()
obv = obv.ffill().bfill()
y = y.ffill().bfill()

# 将计算出的技术指标与交易日期以及股价的涨跌趋势利用字典整合在一起
pm = {'交易日期': data['trade_date'].values}
PM = pd.DataFrame(pm)

DF = {
    'MA5': MA[0],
    'MA10': MA[1],
    'MA20': MA[2],
    'MACD': macd,
    'K': kdj[0],
    'D': kdj[1],
    'J': kdj[2],
    'RSI6': rsi6,
    'RSI12': rsi12,
    'RSI24': rsi24,
    'BIAS5': bias5,
    'BIAS10': bias10,
    'BIAS20': bias20,
    'OBV': obv
}
DF = pd.DataFrame(DF)

s1 = PM.join(DF)

y1 = {'涨跌趋势': y}
ZZ = pd.DataFrame(y1)
s2 = s1.join(ZZ)

# 去掉空值
ss = s2.dropna()

# 将ss中第6列不为0的值提取出来,存放到Data中
Data = ss[ss.iloc[:, 6].values != 0]

# 打印结果
print(Data)
