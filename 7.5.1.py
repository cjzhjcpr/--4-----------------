# 提取综合排名前20的股票代码列表
import fun
r = fun.Fr()
c = r[0]
codelist = list(c.index[0:20])

# 构建排名前20个股票代码的查询字符（连接）
codelist_str = ','.join(codelist)
print(codelist_str)

# 批量获取20个股票代码交易数据stkdata，并导出到Excel
import tushare as ts

# 设置 Tushare API token
ts.set_token('64532b1c03637bc0c3ac92931a5d1b53cfaf75de87c22dfdc70ca6a0')
pro = ts.pro_api()

# 获取股票交易数据
stkdata = pro.daily(ts_code=codelist_str, start_date='20170101', end_date='20171231')

# 按股票代码和交易日期排序
stkdata = stkdata.sort_values(['ts_code', 'trade_date'])

# 重新设置索引
stkdata.index = range(len(stkdata))

# 导出到Excel
stkdata.to_excel('stkdata.xlsx')
