"""
news_aggregator v4.0 - 新闻舆情情感分析
修复：移除境外被墙源，保留国内可访问源
Windows兼容：移除 head 命令依赖
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

# 国内可访问RSS源（已移除被墙的境外源）
RSS_SOURCES = [
    {'name': '财联社', 'url': 'https://www.cls.cn/rss'},
    {'name': '新浪财经', 'url': 'https://finance.sina.com.cn/rss/finance.xml'},
    {'name': '东方财富', 'url': 'https://www.eastmoney.com/rss/zixuan.xml'},
    {'name': '证券时报', 'url': 'https://www.stockstar.com/rss'},
    {'name': '凤凰财经', 'url': 'https://finance.ifeng.com/rss/finance.xml'},
]

CATEGORIES = {
    'finance': {'name': '财经新闻', 'topics': ['A股', '大盘', '财经', '政策']},
    'tech':    {'name': '科技新闻', 'topics': ['科技', 'AI', '人工智能', '半导体']},
    'military':{'name': '军事新闻', 'topics': ['军事', '国防', '军工']},
}

def fetch_rss(source, max_items=3):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        r = requests.get(source['url'], headers=headers, timeout=8)
        feed = feedparser.parse(r.content)
        items = []
        for entry in feed.entries[:max_items]:
            text = (entry.get('title', '') + ' ' + entry.get('summary', '')[:200]).strip()
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
    except Exception as e:
        print(f'  [警告] {source["name"]} 获取失败: {str(e)[:30]}', file=sys.stderr)
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

def run(category='all'):
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    print('=' * 60)
    print('  News Aggregator v4.0 - ' + now)
    print('  舆情分析: 正面/负面/中性 | 负面>60%触发风险提示')
    print('=' * 60)

    cats = list(CATEGORIES.keys()) if category == 'all' else [category]

    for cat in cats:
        cfg = CATEGORIES[cat]
        print()
        print('>>> ' + cfg['name'] + ' <<<')
        items = []
        # RSS（国内源）
        for src in RSS_SOURCES:
            items.extend(fetch_rss(src, max_items=2))
        # Tavily补充（如果有API Key）
        if API_KEY and API_KEY != 'your-tavily-api-key':
            try:
                r = requests.post('https://api.tavily.com/search', json={
                    'api_key': API_KEY,
                    'query': ' '.join(cfg['topics']) + ' 2026',
                    'search_depth': 'basic', 'max_results': 5
                }, timeout=12)
                for item in r.json().get('results', []):
                    text = (item.get('title', '') + ' ' + item.get('content', '')[:200]).strip()
                    sentiment, pos, neg = analyze_sentiment_text(text)
                    items.append({
                        'title': item.get('title', '')[:55],
                        'sentiment': sentiment,
                        'source': 'Tavily',
                        'url': item.get('url', '')[:60]
                    })
            except Exception as e:
                print(f'  [警告] Tavily搜索失败: {str(e)[:30]}', file=sys.stderr)

        # 去重
        seen = set()
        unique = []
        for item in items:
            if item.get('url') and item['url'] not in seen and item.get('title'):
                seen.add(item['url'])
                unique.append(item)

        # 统计
        total = len(unique)
        pos_c = sum(1 for x in unique if x['sentiment'] == 'positive')
        neg_c = sum(1 for x in unique if x['sentiment'] == 'negative')

        print(f'总计: {total}条 | 正面:{pos_c} 负面:{neg_c} 中性:{total-pos_c-neg_c}')
        if total > 0 and neg_c / total > 0.6:
            print('⚠️  负面占比>60%，触发风险提示')

        for item in unique[:8]:
            icon = '🟢' if item['sentiment'] == 'positive' else ('🔴' if item['sentiment'] == 'negative' else '⚪')
            print(f'{icon} [{item["source"]}] {item["title"]}')

    print()
    print('=' * 60)
    print('  news-aggregator v4.0 | 国内RSS源已启用')
    print('=' * 60)

if __name__ == '__main__':
    cat = sys.argv[1] if len(sys.argv) > 1 else 'all'
    run(cat)
