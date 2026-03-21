import akshare as ak
import pandas as pd

print("=== 测试 akshare 实时行情 ===")
try:
    df = ak.stock_zh_a_spot_em()
    print(f"获取到 {len(df)} 只股票")
    print("列名:", list(df.columns[:8]))
    
    codes = ['300394', '300223', '300548', '688521']
    for code in codes:
        row = df[df['代码'] == code]
        if not row.empty:
            print(f"{code}: {row['名称'].values[0]}, 最新价={row['最新价'].values[0]}, 涨跌幅={row['涨跌幅'].values[0]}%")
except Exception as e:
    print(f"Error: {e}")

print("\n=== 测试 akshare 财务数据 ===")
try:
    # 获取个股财务指标
    df = ak.stock_financial_analysis_indicator(symbol="300394", start_year="2024")
    print(f"财务指标获取成功: {len(df)} 条")
    if not df.empty:
        print(df[['报告日期', '净资产收益率(%)', '销售毛利率(%)', '净利润率(%)']].head(5).to_string())
except Exception as e:
    print(f"财务指标 Error: {e}")

print("\n=== 测试 akshare 资金流向 ===")
try:
    df = ak.stock_individual_fund_flow(stock="300394", market="sh")
    print(f"资金流向获取成功: {len(df)} 条")
    if not df.empty:
        print(df.tail(5).to_string())
except Exception as e:
    print(f"资金流向 Error: {e}")
