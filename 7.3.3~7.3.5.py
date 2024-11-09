# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 20:53:57 2018

@author: Administrator
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# 读取数据
data = pd.read_excel('Data.xlsx')

# 检查数据类型
# print(data.dtypes)

# 确保 'ts_code' 列是字符串类型
data['ts_code'] = data['ts_code'].astype(str)

# 保留 'ts_code' 列，以便后续使用
ts_code = data['ts_code'].copy()

# 过滤掉非数值列
numeric_columns = data.select_dtypes(include=[np.number]).columns
data_numeric = data[numeric_columns]

# 过滤掉非正数
data_numeric = data_numeric[data_numeric > 0]

# 删除缺失值
data_numeric = data_numeric.dropna()

# 确保 'ts_code' 列与数据同步
ts_code = ts_code[data_numeric.index]

# 标准化数据
X = data_numeric.iloc[:, 1:]  # 排除第一列 ts_code
scaler = StandardScaler()
scaler.fit(X)
X_scaled = scaler.transform(X)

# 主成分分析
pca = PCA(n_components=0.95)  # 累计贡献率为95%
Y = pca.fit_transform(X_scaled)  # 满足累计贡献率为95%的主成分数据
gxl = pca.explained_variance_ratio_  # 贡献率

# 计算综合得分
F = np.zeros((len(Y)))
for i in range(len(gxl)):
    f = Y[:, i] * gxl[i]
    F += f

# 创建 Series 并排序
fs1 = pd.Series(F, index=ts_code.values)
Fscore1 = fs1.sort_values(ascending=False)  # 降序，True 为升序

# 读取股票代码数据
stk = pd.read_excel('stkcode.xlsx')
stk = pd.Series(stk['name'].values, index=stk['ts_code'].values)

# 过滤掉不在 stk 中的 ts_code
ts_code_filtered = ts_code[ts_code.isin(stk.index)]
F_filtered = F[ts_code.isin(stk.index)]

# 获取对应的股票名称
stk1 = stk[ts_code_filtered.values]

# 创建包含股票名称的 Series 并排序
fs2 = pd.Series(F_filtered, index=stk1.values)
Fscore2 = fs2.sort_values(ascending=False)  # 降序，True 为升序

# 输出结果
print("按股票代码排序的综合得分：")
print(Fscore1)
print("\n按股票名称排序的综合得分：")
print(Fscore2)
