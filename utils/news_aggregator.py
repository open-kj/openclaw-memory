"""
News Aggregator v2.0 - 合并 tech-news-digest RSS源
整合财联社/研报社/凤凰财经/新浪财经/东方财富/中金在线/证券时报
用法: python news_aggregator.py [类别]
"""
import requests
import sys
import os
from datetime import datetime
import feedparser

sys.stdout.reconfigure(encoding='utf-8')
API_KEY = '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'

# 合并后的RSS源（来自tech-news-digest cn-sources.json）
RSS_SOURCES = [
    {'id': 'cls',   'name': '财联社',   'url': 'https://www.cls.cn/rss', 'priority': True},
    {'id': 'yjzh',  'name': '研报社',   'url': 'https://yanjiushe.cn/rss/', 'priority': True},
    {'id': 'ifeng', 'name': '凤凰财经', 'url': 'https://finance.ifeng.com/rss/finance.xml', 'priority': True},
    {'id': 'sina',  'name': '新浪财经', 'url': 'https://finance.sina.com.cn/rss/finance.xml', 'priority': True},
    {'id': 'emoney','name': '东方财富', 'url': 'https://www.eastmoney.com/rss/zixuan.xml', 'priority': True},
    {'id': 'cnfol', 'name': '中金在线', 'url': 'https://rss.cnfol.com/', 'priority': False},
    {'id': 'ststar','name': '证券时报', 'url': 'https://www.stockstar.com/rss', 'priority': False},
]

CATEGORIES = {
    'finance': {
        'name': '财经新闻',
        'topics': ['A股', '大盘', '财经', '政策'],
    },
    'tech': {
        'name': '科技新闻',
        'topics': ['科技', 'AI', '人工智能', '半导体'],
    },
    'military': {
        'name': '军事新闻',
        'topics': ['军事', '国防', '军工'],
    },
}

def fetch_rss(source, max_items=5):
    """抓取单个RSS源"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (compatible; NewsBot/1.0)'}
        r = requests.get(source['url'], headers=headers, timeout=8)
        feed = feedparser.parse(r.content)
        items = []
        for entry in feed.entries[:max_items]:
            items.append({
                'title': entry.get('title', ''),
                'url': entry.get('link', ''),
                'source': source['name'],
                'published': entry.get('published', ''),
                'summary': entry.get('summary', '')[:120],
            })
        return items
    except:
        return []

def search_tavily(query, max_results=3):
    """Tavily搜索"""
    try:
        r = requests.post('https://api.tavily.com/search', json={
            'api_key': API_KEY,
            'query': query,
            'search_depth': 'basic',
            'max_results': max_results
        }, timeout=12)
        d = r.json()
        return [{'title': x['title'], 'url': x['url'], 'source': 'Tavily',
                 'published': '', 'summary': ''} for x in d.get('results', [])[:max_results]]
    except:
        return []

def deduplicate(items):
    seen = set()
    result = []
    for item in items:
        url = item.get('url', '')
        if url and url not in seen:
            seen.add(url)
            result.append(item)
    return result

def fetch_all_sources(max_per_source=3):
    """抓取所有RSS源"""
    all_items = []
    for source in RSS_SOURCES:
        items = fetch_rss(source, max_per_source)
        all_items.extend(items)
    return deduplicate(all_items)

def filter_by_topic(items, topics):
    """按话题过滤"""
    if not topics:
        return items
    result = []
    for item in items:
        text = (item['title'] + item.get('summary', '')).lower()
        for topic in topics:
            if topic.lower() in text:
                result.append(item)
                break
    return result

def format_output(cat_name, items, max_items=8):
    print()
    print('## ' + cat_name)
    print()
    for i, item in enumerate(items[:max_items], 1):
        print(str(i) + '. [' + item['title'][:55] + '](' + item['url'][:65] + ')')
        print('   来源:' + item['source'] + ' | ' + item.get('published', '')[:16])
        if item.get('summary'):
            print('   ' + item['summary'][:80])
        print()

def run(category='all', use_tavily=True, use_rss=True):
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    print('=' * 60)
    print('  News Aggregator v2.0 - ' + now)
    print('  Sources: RSS(' + str(sum(1 for s in RSS_SOURCES if s['priority'])) + '优先) + Tavily')
    print('=' * 60)

    cats = CATEGORIES.keys() if category == 'all' else [category]

    for cat in cats:
        if cat not in CATEGORIES:
            continue
        cfg = CATEGORIES[cat]
        print()
        print('>>> ' + cfg['name'] + ' <<<')

        items = []
        # RSS源（优先源）
        if use_rss:
            rss_items = fetch_all_sources(max_per_source=3)
            rss_filtered = filter_by_topic(rss_items, cfg['topics'])
            items.extend(rss_filtered)

        # Tavily搜索（补充）
        if use_tavily:
            for topic in cfg['topics'][:2]:
                tavily_results = search_tavily(topic + ' 2026', max_results=3)
                items.extend(tavily_results)

        # 去重+优先级排序
        unique = deduplicate(items)
        # 优先源排前面
        unique.sort(key=lambda x: 0 if x['source'] != 'Tavily' else 1)
        format_output(cfg['name'], unique, max_items=8)

    print('=' * 60)
    print('  Powered by Tavily + RSS | news-aggregator v2.0 (merged tech-news-digest)')
    print('=' * 60)

if __name__ == '__main__':
    cat = sys.argv[1] if len(sys.argv) > 1 else 'all'
    run(cat)
