import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import numpy as np


def Fr():
    # 读取数据
    data = pd.read_excel('Data.xlsx', index_col=0)  # 确保索引是股票代码

    # 只选择数值列
    numeric_cols = data.select_dtypes(include=[np.number]).columns
    data = data[numeric_cols]

    # 处理非正数
    data = data[data > 0]
    data = data.dropna()

    # 读取股票代码
    co = pd.read_excel('stkcode.xlsx', index_col=0)  # 确保索引是股票代码
    Co = pd.Series(co['name'].values, index=co.index)

    # 打印调试信息
    print("data.index:", data.index)
    print("co.index:", co.index)

    # 确保索引匹配
    common_indices = data.index.intersection(Co.index)
    if common_indices.empty:
        raise ValueError("No common indices found between data.index and co.index")

    # 仅使用共同的索引
    data_common = data.loc[common_indices]

    # 打印调试信息
    print("common_indices length:", len(common_indices))
    print("data_common length:", len(data_common))

    # 标准化
    scaler = StandardScaler()
    X = scaler.fit_transform(data_common)

    # PCA
    pca = PCA(n_components=0.95)  # 累计贡献率为95%
    Y = pca.fit_transform(X)
    gxl = pca.explained_variance_ratio_

    # 计算综合得分
    F = np.dot(Y, gxl)

    # 打印调试信息
    print("F length:", len(F))

    # 创建得分序列
    fs1 = pd.Series(F, index=data_common.index)
    Fscore1 = fs1.sort_values(ascending=False)

    Co1 = Co[common_indices]

    # 打印调试信息
    print("Co1 length:", len(Co1))

    fs2 = pd.Series(F, index=Co1.index)
    Fscore2 = fs2.sort_values(ascending=False)

    return Fscore1, Fscore2
