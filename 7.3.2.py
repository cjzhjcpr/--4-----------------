# -*- coding: utf-8 -*-
import tushare as ts
import pandas as pd

# Tushare API 初始化
ts.set_token('64532b1c03637bc0c3ac92931a5d1b53cfaf75de87c22dfdc70ca6a0')
pro = ts.pro_api()

# 股票基本信息获取，并保存为 Excel 文件
try:
    stkcode = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry')
    stkcode.to_excel('stkcode.xlsx', index=False)
    print("股票基本信息已成功导出到 'stkcode.xlsx'")
except PermissionError as e:
    print(f"无法写入 'stkcode.xlsx' 文件：{e}")
    print("请确保文件没有被其他程序占用，并且你有写入权限。")
    exit(1)

# 从利润表中获取营业收入、营业利润、利润总额、净利润指标数据
income = pro.income_vip(period='20161231', fields='ts_code,revenue,operate_profit,total_profit,n_income_attr_p')
income = income.drop_duplicates(subset=['ts_code'])
print(f"收入数据列名: {income.columns}")

# 从资产负债表中获取资产总计、固定资产指标数据
balance = pro.balancesheet_vip(period='20161231', fields='ts_code,total_assets,fix_assets')
balance = balance.drop_duplicates(subset=['ts_code'])
print(f"资产负债数据列名: {balance.columns}")

# 从财务指标表中获取净资产收益率、每股净资产、每股资本公积、每股收益指标数据
indicator = pro.fina_indicator_vip(period='20161231', fields='ts_code,roe,bps,capital_rese_ps,eps')
indicator = indicator.drop_duplicates(subset=['ts_code'])
print(f"财务指标数据列名: {indicator.columns}")

# 检查每个数据集中是否包含 'ts_code' 列
for df, name in zip([income, balance, indicator], ['income', 'balance', 'indicator']):
    if 'ts_code' not in df.columns:
        raise KeyError(f"数据集 {name} 中没有 'ts_code' 列，请检查数据文件")

# 检查并处理 NaN 值
def check_and_handle_nan(df, name):
    if df.isnull().values.any():
        print(f"数据集 {name} 包含 NaN 值，进行处理...")
        # 选择删除包含 NaN 的行
        df = df.dropna()
        # 或者选择填充 NaN 值
        # df = df.fillna(0)
    return df

income = check_and_handle_nan(income, 'income')
balance = check_and_handle_nan(balance, 'balance')
indicator = check_and_handle_nan(indicator, 'indicator')

# 数据集成，以代码为键，内连接，并把集成后的数据导出 Excel
tempdata = pd.merge(income, balance, how='inner', on='ts_code')
Data = pd.merge(tempdata, indicator, how='inner', on='ts_code')

# 确保合并后的数据集中包含 'ts_code' 列
if 'ts_code' not in Data.columns:
    raise KeyError("合并后的数据集中没有 'ts_code' 列，请检查数据文件")

# 再次检查并处理 NaN 值
Data = check_and_handle_nan(Data, 'Data')

# 将集成后的数据导出到 Excel
Data.to_excel('Data.xlsx', index=False)
print("数据已成功导出到 'Data.xlsx'")

## 另外，本章中的其他数据获取例子，也在本程序中
# 获取上汽集团2017年的交易数据，并导出 Excel
dta = pro.daily(ts_code='600104.SH', start_date='20170101', end_date='20171231')
dta = dta.sort_values('trade_date')
dta.to_excel('dta.xlsx')

# 获取沪深300指数2017年的交易数据，并导出 Excel
hs300 = pro.index_daily(ts_code='399300.SZ', start_date='20170101', end_date='20171231')
hs300 = hs300.sort_values('trade_date')
hs300.to_excel('hs300.xlsx')
