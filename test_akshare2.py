import akshare as ak
import warnings
warnings.filterwarnings('ignore')

print("=== 1. 测试实时行情（备用源）===")
try:
    df = ak.stock_zh_a_hist(symbol="300394", period="daily", start_date="20260301", end_date="20260321")
    print(f"日线历史: {len(df)} 条")
    print(df.tail(3).to_string())
except Exception as e:
    print(f"日线 Error: {e}")

print("\n=== 2. 测试财务指标 ===")
try:
    df = ak.stock_financial_report_sina(stock="300394", symbol="资产负债表")
    print(f"资产负债表: {len(df)} 行")
    print(df.iloc[:3, :4].to_string())
except Exception as e:
    print(f"资产负债表 Error: {e}")

print("\n=== 3. 测试资金流向 ===")
try:
    df = ak.stock_money_flow_hsgt_em()
    print(f"沪深港通资金流向: {len(df)} 条")
    print(df.head(5).to_string())
except Exception as e:
    print(f"资金流向 Error: {e}")

print("\n=== 4. 测试指数行情 ===")
try:
    df = ak.stock_zh_index_spot_em()
    print(f"指数行情: {len(df)} 条")
    print(df[df['代码'].isin(['000001', '399001', '399006'])].to_string())
except Exception as e:
    print(f"指数行情 Error: {e}")
