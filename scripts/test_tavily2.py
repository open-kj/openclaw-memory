import requests, sys
sys.stdout.reconfigure(encoding='utf-8')
API = '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'
queries = [
    'sz300223 炬芯科技 电池管理芯片',
    '天孚通信 sz300394 光模块',
    '博创科技 sz300548 光模块',
]
for q in queries:
    r = requests.post('https://api.tavily.com/search', json={
        'api_key': API, 'query': q, 'search_depth': 'basic', 'max_results': 2
    }, timeout=12)
    d = r.json()
    print('===', q[:30], '===')
    for item in d.get('results', [])[:2]:
        print(' ', item.get('title','')[:60])
        print('  ', item.get('url','')[:60])
    print()
