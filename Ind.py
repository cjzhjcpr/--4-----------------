# Ind.py
import pandas as pd
import numpy as np


def MA(data, N1, N2, N3):
    # 计算不同周期的移动平均
    MAN1 = data['close'].rolling(window=N1).mean()
    MAN2 = data['close'].rolling(window=N2).mean()
    MAN3 = data['close'].rolling(window=N3).mean()

    return (MAN1, MAN2, MAN3)


def MACD(data):
    # 计算指数平滑移动平均线EMA
    EMA12 = data['close'].ewm(span=12, adjust=False).mean()
    EMA26 = data['close'].ewm(span=26, adjust=False).mean()
    DIF = EMA12 - EMA26
    DEA = DIF.ewm(span=9, adjust=False).mean()
    MACD = (DIF - DEA) * 2

    return MACD


def KDJ(data, N):
    # 计算随机指标KDJ
    if len(data) < N:
        print(f"Insufficient data length for KDJ calculation. Expected at least {N} days, got {len(data)} days.")
        return None, None, None

    Lmin = data['low'].rolling(window=N).min()
    Lmax = data['high'].rolling(window=N).max()
    RSV = (data['close'] - Lmin) / (Lmax - Lmin) * 100

    # 确保 RSV 序列的索引与 data 的索引一致
    RSV = RSV.reindex(data.index)

    K = np.zeros(len(RSV))
    D = np.zeros(len(RSV))
    J = np.zeros(len(RSV))

    for t in range(N, len(data)):
        if t == N:
            K[t] = RSV[t]
            D[t] = RSV[t]
        else:
            K[t] = (2 / 3) * K[t - 1] + (1 / 3) * RSV[t]
            D[t] = (2 / 3) * D[t - 1] + (1 / 3) * K[t]
        J[t] = 3 * D[t] - 2 * K[t]

    return (pd.Series(K, index=data.index), pd.Series(D, index=data.index), pd.Series(J, index=data.index))


def RSI(data, N):
    # 计算相对强弱指标RSI
    delta = data['close'].diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=N).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=N).mean()
    RS = gain / loss
    RSI = 100 - (100 / (1 + RS))

    return RSI


def BIAS(data, N):
    # 计算乖离率BIAS
    MA = data['close'].rolling(window=N).mean()
    BIAS = (data['close'] - MA) / MA * 100

    return BIAS


def OBV(data):
    # 计算能量潮OBV
    obv = (data['vol'] * data['close'].diff().apply(lambda x: 1 if x > 0 else -1 if x < 0 else 0)).cumsum()

    return obv


def cla(data):
    # 计算涨跌趋势
    y = data['close'].diff().apply(lambda x: 1 if x > 0 else -1 if x < 0 else 0)

    return y
