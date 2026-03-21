"""
news_aggregator v3.0 - 新闻舆情情感分析
新增新闻/股吧舆情情感分析（正面/负面/中性）
负面占比>60%时触发风险提示
"""
import requests
import sys
import os
import feedparser
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')
API_KEY = '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'

POSITIVE_KW = ['涨', '突破', '利好', '增长', '强势', '看好', '买入', '推荐', '新高', '首板', '涨停', '净流入', '增持']
NEGATIVE_KW = ['跌', '减持', '风险', '预警', '利空', '亏损', '警示', '下挫', '破位', '跌停', '净流出', '减持', '暴雷', '造假']
NEUTRAL_KW = ['平', '震荡', '观望', '持平']

RSS_SOURCES = [
    {'name': '财联社', 'url': 'https://www.cls.cn/rss'},
    {'name': '研报社', 'url': 'https://yanjiushe.cn/rss/'},
    {'name': '凤凰财经', 'url': 'https://finance.ifeng.com/rss/finance.xml'},
    {'name': '新浪财经', 'url': 'https://finance.sina.com.cn/rss/finance.xml'},
    {'name': '东方财富', 'url': 'https://www.eastmoney.com/rss/zixuan.xml'},
    {'name': '中金在线', 'url': 'https://rss.cnfol.com/'},
    {'name': '证券时报', 'url': 'https://www.stockstar.com/rss'},
]

CATEGORIES = {
    'finance': {'name': '财经新闻', 'topics': ['A股', '大盘', '财经', '政策']},
    'tech':    {'name': '科技新闻', 'topics': ['科技', 'AI', '人工智能', '半导体']},
    'military':{'name': '军事新闻', 'topics': ['军事', '国防', '军工']},
}

def fetch_rss(source, max_items=3):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(source['url'], headers=headers, timeout=8)
        feed = feedparser.parse(r.content)
        items = []
        for entry in feed.entries[:max_items]:
            text = entry.get('title', '') + entry.get('summary', '')[:200]
            sentiment, pos, neg = analyze_sentiment_text(text)
            items.append({
                'title': entry.get('title', '')[:60],
                'url': entry.get('link', ''),
                'source': source['name'],
                'sentiment': sentiment,
                'pos_count': pos,
                'neg_count': neg,
            })
        return items
    except:
        return []

def analyze_sentiment_text(text):
    """分析单条文本情感"""
    pos = sum(1 for kw in POSITIVE_KW if kw in text)
    neg = sum(1 for kw in NEGATIVE_KW if kw in text)
    if pos > neg and pos > 0:
        return 'positive', pos, neg
    elif neg > pos and neg > 0:
        return 'negative', pos, neg
    return 'neutral', pos, neg

def analyze_stock_sentiment(code, name):
    """
    分析个股舆情：搜索相关新闻 + 股吧
    返回：正面%/负面%/中性%，触发风险条件
    """
    try:
        r = requests.post('https://api.tavily.com/search', json={
            'api_key': API_KEY,
            'query': code + ' ' + name + ' 最新 2026',
            'search_depth': 'basic',
            'max_results': 10
        }, timeout=15)
        results = r.json().get('results', [])

        items = []
        for item in results:
            text = item.get('title', '') + item.get('content', '')[:200]
            sentiment, pos, neg = analyze_sentiment_text(text)
            items.append({'title': item['title'][:50], 'sentiment': sentiment,
                          'source': 'Tavily', 'url': item['url'][:60]})

        total = len(items)
        pos_c = sum(1 for x in items if x['sentiment'] == 'positive')
        neg_c = sum(1 for x in items if x['sentiment'] == 'negative')
        neu_c = sum(1 for x in items if x['sentiment'] == 'neutral')

        pos_pct = pos_c / max(total, 1) * 100
        neg_pct = neg_c / max(total, 1) * 100

        return {
            'code': code, 'name': name,
            'total': total,
            'positive': pos_c, 'negative': neg_c, 'neutral': neu_c,
            'positive_pct': round(pos_pct, 1),
            'negative_pct': round(neg_pct, 1),
            'risk_alert': neg_pct > 60,
            'items': items,
        }
    except:
        return None

def run(category='all'):
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    print('=' * 60)
    print('  News Aggregator v3.0 - ' + now)
    print('  舆情分析: 正面/负面/中性 | 负面>60%触发风险提示')
    print('=' * 60)

    cats = CATEGORIES.keys() if category == 'all' else [category]

    for cat in cats:
        cfg = CATEGORIES[cat]
        print()
        print('>>> ' + cfg['name'] + ' <<<')
        items = []
        # RSS
        for src in RSS_SOURCES:
            items.extend(fetch_rss(src, max_items=2))
        # Tavily补充
        try:
            r = requests.post('https://api.tavily.com/search', json={
                'api_key': API_KEY,
                'query': ' '.join(cfg['topics']) + ' 2026',
                'search_depth': 'basic', 'max_results': 5
            }, timeout=12)
            for item in r.json().get('results', []):
                text = item.get('title', '') + item.get('content', '')[:200]
                sentiment, pos, neg = analyze_sentiment_text(text)
                items.append({'title': item['title'][:55], 'sentiment': sentiment,
                              'source': 'Tavily', 'url': item['url'][:60]})
        except:
            pass

        # 去重
        seen = set()
        unique = []
        for item in items:
            if item['url'] not in seen and item['title']:
                seen.add(item['url'])
                unique.append(item)

        # 统计
        total = len(unique)
        pos_c = sum(1 for x in unique if x['sentiment'] == 'positive')
        neg_c = sum(1 for x in unique if x['sentiment'] == 'negative')

        print(f'总计: {total}条 | 正面:{pos_c} 负面:{neg_c} 中性:{total-pos_c-neg_c}')
        if neg_c / max(total, 1) > 0.6:
            print('⚠️  负面占比>60%，触发风险提示')

        for item in unique[:8]:
            icon = '🟢' if item['sentiment'] == 'positive' else ('🔴' if item['sentiment'] == 'negative' else '⚪')
            print(f'{icon} [{item["source"]}] {item["title"]}')

    print()
    print('=' * 60)
    print('  news-aggregator v3.0 | 舆情分析已启用')
    print('=' * 60)

if __name__ == '__main__':
    cat = sys.argv[1] if len(sys.argv) > 1 else 'all'
    run(cat)
