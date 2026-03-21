"""
News Aggregator - 新闻聚合脚本
实现: news-aggregator skill v1.0.3
用法: python news_aggregator.py [类别]
类别: tech|military|finance|all (默认all)
"""
import requests
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')
API_KEY = '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'

CATEGORIES = {
    'finance': {
        'name': '财经新闻',
        'queries': [
            'A股 今日行情 2026',
            '财经 要闻 2026年3月',
            '科技股 军工股 行情分析 2026',
        ]
    },
    'tech': {
        'name': '科技新闻',
        'queries': [
            '科技 新闻 2026年3月',
            'AI 人工智能 最新进展 2026',
            '半导体 芯片 行情 2026',
        ]
    },
    'military': {
        'name': '军事新闻',
        'queries': [
            '军事 新闻 2026年3月',
            '国防 军工 最新动态 2026',
            '中国军事 装备 最新消息 2026',
        ]
    }
}

def search_tavily(query, max_results=4):
    try:
        r = requests.post('https://api.tavily.com/search', json={
            'api_key': API_KEY,
            'query': query,
            'search_depth': 'basic',
            'max_results': max_results
        }, timeout=15)
        d = r.json()
        return d.get('results', [])[:max_results]
    except:
        return []

def fetch_rss(url, max_items=5):
    """抓取RSS源（备用）"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=8)
        # 简单解析，实际用feedparser更好
        return []
    except:
        return []

def deduplicate(items):
    """去重"""
    seen = set()
    result = []
    for item in items:
        url = item.get('url', '')
        if url and url not in seen:
            seen.add(url)
            result.append(item)
    return result

def format_output(category, items):
    print()
    print(f"## {CATEGORIES[category]['name']}")
    print()
    for i, item in enumerate(items, 1):
        title = item.get('title', '无标题')[:60]
        url = item.get('url', '')
        snippet = item.get('content', item.get('snippet', ''))[:100]
        print(f"{i}. [{title}]({url})")
        if snippet:
            print(f"   要点：{snippet}...")
        print()

def run(category='all'):
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    print('=' * 60)
    print(f'  News Aggregator - {now}')
    print('=' * 60)

    if category == 'all':
        cats = CATEGORIES.keys()
    else:
        cats = [category]

    for cat in cats:
        if cat not in CATEGORIES:
            continue
        all_items = []
        for query in CATEGORIES[cat]['queries']:
            items = search_tavily(query, max_results=4)
            all_items.extend(items)
        # 去重
        unique = deduplicate(all_items)
        format_output(cat, unique[:8])  # 每类最多8条

    print('=' * 60)
    print('  Powered by Tavily Search | Skill: news-aggregator v1.0.3')
    print('=' * 60)

if __name__ == '__main__':
    cat = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if cat not in CATEGORIES and cat != 'all':
        print('用法: python news_aggregator.py [tech|military|finance|all]')
        sys.exit(0)
    run(cat)
