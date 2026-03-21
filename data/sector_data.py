"""
sector_data.py - 板块数据
获取个股所属行业/概念板块的涨跌幅、领涨股、政策利好
"""
import requests
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

def get_stock_sector(code):
    """
    获取个股所属行业板块和概念板块
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.eastmoney.com'}
        market = 1 if code.startswith('sh') else 0
        secid = f'{market}.{code[2:]}'
        r = requests.get(
            'https://push2.eastmoney.com/api/qt/stock/get',
            params={
                'secid': secid,
                'fields': 'f58,f107,f104,f105,f123,f124,f127,f128',
                'ut': 'b2884a393a59ad64002292a3e90d46a5'
            },
            headers=headers, timeout=8
        )
        d = r.json().get('data', {})
        return {
            'name': d.get('f58', ''),       # 股票名称
            'industry': d.get('f127', ''),  # 所属行业
            'concept': d.get('f128', ''),   # 所属概念板块
            'price': d.get('f43', 0),        # 现价
            'chg_pct': d.get('f170', 0),     # 涨跌幅
        }
    except:
        return None

def get_industry_rank():
    """
    获取行业板块涨幅榜（东方财富）
    返回：按涨幅排序的板块列表
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://quote.eastmoney.com'}
        r = requests.get(
            'https://push2.eastmoney.com/api/qt/clist/get',
            params={
                'cb': 'jQuery',
                'pn': 1, 'pz': 50, 'po': 1,  # po=1按涨幅降序
                'np': 1,
                'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
                'fltt': 2, 'invt': 2,
                'fid': 'f3',  # f3=最新价
                'fs': 'm:90 t:2 f:!50',  # 行业板块
                'fields': 'f2,f3,f4,f12,f14,f20,f23',
            },
            headers=headers, timeout=8
        )
        d = r.json()
        items = d.get('data', {}).get('diff', [])
        results = []
        for item in items[:20]:  # 前20强
            results.append({
                'code': item.get('f12', ''),
                'name': item.get('f14', ''),
                'chg_pct': item.get('f3', 0),
                'lead_stock': item.get('f23', ''),  # 领涨股
            })
        return results
    except:
        return []

def get_concept_rank():
    """获取概念板块涨幅榜"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://quote.eastmoney.com'}
        r = requests.get(
            'https://push2.eastmoney.com/api/qt/clist/get',
            params={
                'pn': 1, 'pz': 30, 'po': 1,
                'np': 1,
                'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
                'fltt': 2, 'invt': 2,
                'fid': 'f3',
                'fs': 'm:90 t:3 f:!50',  # 概念板块
                'fields': 'f2,f3,f12,f14,f20',
            },
            headers=headers, timeout=8
        )
        d = r.json()
        items = d.get('data', {}).get('diff', [])
        return [{'code': i.get('f12', ''), 'name': i.get('f14', ''),
                 'chg_pct': i.get('f3', 0)} for i in items[:15]]
    except:
        return []

def check_sector_deviation(code, name, stock_chg_pct, sector_list):
    """
    检查个股与板块偏离度：偏离板块>2%时触发分析
    """
    stock_sector = get_stock_sector(code)
    if not stock_sector:
        return None

    # 在板块列表中查找该个股所属板块
    industry = stock_sector.get('industry', '')
    sector_avg_chg = 0
    for s in sector_list:
        if industry and (industry in s.get('name', '') or s.get('name', '') in industry):
            sector_avg_chg = s.get('chg_pct', 0)
            break

    deviation = abs(stock_chg_pct - sector_avg_chg) if sector_avg_chg else 0

    if deviation > 2:
        return {
            'code': code,
            'name': name,
            'stock_chg': stock_chg_pct,
            'industry': industry,
            'sector_chg': sector_avg_chg,
            'deviation': deviation,
            'alert': True
        }
    return {'alert': False, 'deviation': deviation}

def get_policy_news():
    """获取政策利好新闻（Tavily搜索）"""
    try:
        r = requests.post('https://api.tavily.com/search', json={
            'api_key': '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',
            'query': 'A股 政策利好 行业 2026',
            'search_depth': 'basic',
            'max_results': 5
        }, timeout=12)
        return [item['title'] for item in r.json().get('results', [])]
    except:
        return []

if __name__ == '__main__':
    print('=== 行业板块涨幅榜（前10）===')
    ranks = get_industry_rank()
    for r in ranks[:10]:
        print(f'{r["name"]}: {r["chg_pct"]:+.2f}% 领涨:{r["lead_stock"]}')

    print()
    print('=== 概念板块涨幅榜（前10）===')
    cr = get_concept_rank()
    for c in cr[:10]:
        print(f'{c["name"]}: {c["chg_pct"]:+.2f}%')

    print()
    print('=== 政策利好 ===')
    for news in get_policy_news()[:3]:
        print(f'  - {news[:50]}')
