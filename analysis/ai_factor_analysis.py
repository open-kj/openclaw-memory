"""
ai_factor_analysis.py - 多因子评分模型
整合技术面/基本面/资金面/情绪面 → 0-10分
≥8买入建议，≤3卖出建议，3-8持有
"""
import requests
import sys
import os
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config.settings import TAVILY_API_KEY

def get_price(code):
    try:
        r = requests.get('https://qt.gtimg.cn/q=' + code, timeout=8)
        parts = r.text.split('~')
        if len(parts) > 32:
            return {'price': float(parts[3]), 'chg': float(parts[32]),
                    'vol': int(parts[6]) if parts[6].isdigit() else 0}
    except:
        return None

def get_money_flow_data(code):
    """获取资金流（复用capital_flow模块逻辑）"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://data.eastmoney.com'}
        market = 1 if code.startswith('sh') else 0
        secid = f'{market}.{code[2:]}'
        r = requests.get(
            'https://push2.eastmoney.com/api/qt/stock/get',
            params={'secid': secid, 'fields': 'f62,f184',
                    'ut': 'b2884a393a59ad64002292a3e90d46a5'},
            headers=headers, timeout=8
        )
        d = r.json().get('data', {})
        if d:
            return {'main_rate': d.get('f184', 0) or 0, 'main_net': d.get('f62', 0) or 0}
    except:
        pass
    return {'main_rate': 0, 'main_net': 0}

def get_sentiment(code, name):
    """
    情绪面：Tavily搜索新闻，情感判断
    返回：正面% / 负面% / 中性%
    """
    try:
        r = requests.post('https://api.tavily.com/search', json={
            'api_key': TAVILY_API_KEY,
            'query': code + ' ' + name + ' 最新 2026',
            'search_depth': 'basic',
            'max_results': 5
        }, timeout=12)
        titles = [item['title'] + item.get('content', '')[:100]
                  for item in r.json().get('results', [])]

        positive_kw = ['涨', '突破', '利好', '增长', '强势', '看好', '买入', '推荐']
        negative_kw = ['跌', '减持', '风险', '预警', '利空', '亏损', '警示', '下挫']
        pos = sum(1 for t in ' '.join(titles) for kw in positive_kw if kw in t)
        neg = sum(1 for t in ' '.join(titles) for kw in negative_kw if kw in t)
        total = len(titles)
        return {
            'positive_pct': pos / max(total, 1) * 100,
            'negative_pct': neg / max(total, 1) * 100,
            'sentiment': 'positive' if pos > neg else ('negative' if neg > pos else 'neutral'),
            'titles': titles
        }
    except:
        return {'positive_pct': 33, 'negative_pct': 33, 'sentiment': 'neutral', 'titles': []}

def calc_score(code, name, cost):
    """
    多因子评分：0-10分
    权重：技术面30% + 资金面30% + 情绪面20% + 基本面20%
    """
    score = 5.0  # 基准分
    factors = {}
    reasons = []

    # 1. 技术面（30%）：价格相对成本
    p = get_price(code)
    if p:
        price = p['price']
        chg_pct = p['chg']
        # 相对成本涨跌
        if cost > 0:
            cost_score = min(max((price - cost) / cost * 10 + 5, 0), 10)
            factors['tech'] = cost_score
            score = score * 0.7 + cost_score * 0.3
            if chg_pct > 3:
                reasons.append(f'今日涨幅{chg_pct:.1f}%强势')
            elif chg_pct < -3:
                reasons.append(f'今日跌幅{chg_pct:.1f}%偏弱')
    else:
        factors['tech'] = 5

    # 2. 资金面（30%）：主力净流入率
    mf = get_money_flow_data(code)
    if mf:
        main_rate = mf.get('main_rate', 0)
        # 主力净流入率>5%给高分，<-5%给低分
        if main_rate > 5:
            fund_score = 9
            reasons.append(f'主力净流入{main_rate:.1f}%')
        elif main_rate > 2:
            fund_score = 7
            reasons.append(f'主力净流入{main_rate:.1f}%')
        elif main_rate < -5:
            fund_score = 2
            reasons.append(f'主力净流出{abs(main_rate):.1f}%')
        elif main_rate < -2:
            fund_score = 4
            reasons.append(f'主力净流出{abs(main_rate):.1f}%')
        else:
            fund_score = 5
        factors['fund'] = fund_score
        score = score * 0.7 + fund_score * 0.3
    else:
        factors['fund'] = 5

    # 3. 情绪面（20%）
    sent = get_sentiment(code, name)
    if sent['sentiment'] == 'positive':
        sent_score = 8
        reasons.append('舆情正面')
    elif sent['sentiment'] == 'negative':
        sent_score = 3
        reasons.append('舆情负面')
    else:
        sent_score = 5
    factors['sentiment'] = sent_score
    score = score * 0.8 + sent_score * 0.2

    # 4. 基本面（20%）：简化为PE合理性和成本价
    if cost > 0:
        # 假设行业平均PE 30，合理价格 = cost（持有者视角）
        if price >= cost:
            basic_score = 7
        else:
            basic_score = 3
    else:
        basic_score = 5
    factors['basic'] = basic_score
    score = score * 0.8 + basic_score * 0.2

    final_score = round(min(max(score, 0), 10), 1)

    if final_score >= 8:
        advice = '建议买入'
    elif final_score <= 3:
        advice = '建议卖出'
    else:
        advice = '持有'

    return {
        'code': code,
        'name': name,
        'score': final_score,
        'advice': advice,
        'factors': {k: round(v, 1) for k, v in factors.items()},
        'reasons': reasons,
        'sentiment': sent,
        'price': p.get('price') if p else None,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
    }

if __name__ == '__main__':
    print('=== 多因子评分 ===')
    stocks = [
        ('sz300394', '天孚通信', 306.99),
        ('sz300223', '北京君正', 122.34),
        ('sz300548', '长芯博创', 148.57),
        ('sh688521', '芯原股份', 198.88),
    ]
    for code, name, cost in stocks:
        result = calc_score(code, name, cost)
        print(f'{name}({code}): {result["score"]}/10 → {result["advice"]}')
        print(f'  因子: {result["factors"]}')
        print(f'  原因: {", ".join(result["reasons"])}')
        print()
