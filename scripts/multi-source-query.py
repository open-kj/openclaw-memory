"""
多源并发查询脚本
同时从多个数据源获取信息，汇总结果
用法: python multi-source-query.py <stock_code> [stock_name]
"""
import requests
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = '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'

def query_tencent(code):
    try:
        r = requests.get(f'https://qt.gtimg.cn/q={code}', timeout=8)
        parts = r.text.split('~')
        if len(parts) > 35:
            return {'source': '腾讯财经', 'price': float(parts[3]), 'chg_pct': float(parts[32])}
    except:
        return None

def query_sina(code):
    try:
        r = requests.get(
            f'https://hq.sinajs.cn/list={code}',
            headers={'Referer': 'https://finance.sina.com.cn'},
            timeout=8
        )
        content = r.text.split('"')[1]
        parts = content.split(',')
        if len(parts) > 10:
            return {'source': '新浪财经', 'price': float(parts[3]), 'chg_pct': float(parts[32])}
    except:
        return None

def query_tavily(query, max_results=3):
    try:
        r = requests.post('https://api.tavily.com/search', json={
            'api_key': API_KEY,
            'query': query,
            'search_depth': 'basic',
            'max_results': max_results
        }, timeout=12)
        d = r.json()
        results = d.get('results', [])[:max_results]
        return {'source': 'Tavily', 'results': [{'title': x['title'][:50], 'url': x['url'][:70]} for x in results]}
    except:
        return None

def query_all(code, stock_name='股票'):
    print(f'=== 多源查询: {stock_name} ({code}) ===')
    print()

    with ThreadPoolExecutor(max_workers=5) as ex:
        futures = {
            '腾讯财经': ex.submit(query_tencent, code),
            '新浪财经': ex.submit(query_sina, code),
            'Tavily-个股新闻': ex.submit(query_tavily, f'{stock_name} 最新消息 2026'),
            'Tavily-行情分析': ex.submit(query_tavily, f'{stock_name} 今日行情分析'),
        }

        prices = {}
        for name, f in futures.items():
            try:
                result = f.result(timeout=15)
                if result:
                    if 'price' in result:
                        prices[name] = result['price']
                        print(f'  股价 | {name}: {result["price"]:.2f} ({result["chg_pct"]:+.2f}%)')
                    elif 'results' in result:
                        print(f'  新闻 | {name}:')
                        for item in result['results']:
                            print(f'    - {item["title"]}')
                            print(f'      {item["url"]}')
            except Exception as e:
                print(f'  错误 | {name}: {str(e)[:40]}')

        print()
        if len(prices) >= 2:
            diff = max(prices.values()) - min(prices.values())
            avg = sum(prices.values()) / len(prices)
            print(f'  验证: {len(prices)}个价格，平均={avg:.2f}，极差={diff:.2f}')
            if diff / avg > 0.005:
                print('  ⚠️ 价格差异>0.5%，建议核实')
            else:
                print('  ✅ 多源数据一致')

if __name__ == '__main__':
    if len(sys.argv) > 2:
        code = sys.argv[1]
        name = sys.argv[2]
    elif len(sys.argv) > 1:
        code = sys.argv[1]
        name = sys.argv[1]
    else:
        print('用法: python multi-source-query.py <股票代码> [股票名称]')
        sys.exit(0)
    query_all(code, name)
