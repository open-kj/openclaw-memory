import requests
import sys
sys.stdout.reconfigure(encoding='utf-8')

queries = [
    'A股今日行情分析 2026年3月',
    '炬芯科技 300223 最新消息',
    '天孚通信 光模块 最新',
    '下周A股预测 展望',
]

for q in queries:
    r = requests.post('https://api.tavily.com/search', json={
        'api_key': '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',
        'query': q,
        'search_depth': 'basic',
        'max_results': 2
    }, timeout=12)
    d = r.json()
    results = d.get('results', [])
    print(f'=== {q} ===')
    for res in results[:2]:
        title = res.get('title', '')[:60]
        url = str(res.get('url', ''))[:70]
        print(f'  {title}')
        print(f'  {url}')
    print()
