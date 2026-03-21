"""
tradingagents-analysis 精简版
只保留多智能体投研核心逻辑
去除了冗余部分
"""
import requests
import sys
import os
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')
API_KEY = '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'

def search_tavily(query, max_results=5):
    try:
        r = requests.post('https://api.tavily.com/search', json={
            'api_key': API_KEY,
            'query': query,
            'search_depth': 'basic',
            'max_results': max_results
        }, timeout=12)
        return r.json().get('results', [])
    except:
        return []

def get_price(code):
    try:
        r = requests.get('https://qt.gtimg.cn/q=' + code, timeout=8)
        parts = r.text.split('~')
        if len(parts) > 32:
            return {'price': float(parts[3]), 'chg': float(parts[32])}
    except:
        return None

# 5阶段分析师框架
ANALYSTS = [
    {'name': '技术面分析师', 'prompt': '技术分析 {name} 当前价格 {price}，分析均线、MACD、量能'},
    {'name': '基本面分析师', 'prompt': '基本面分析 {name}，分析营收、利润、ROE、行业地位'},
    {'name': '资金面分析师', 'prompt': '资金流向分析 {name}，北向资金、主力净流入'},
    {'name': '情绪面分析师', 'prompt': '市场情绪分析 {name}，舆论热度、资金情绪'},
    {'name': '综合策略师', 'prompt': '综合以上分析，给出 {name} 的投资建议和风险提示'},
]

def analyze_stock(code, name):
    """多智能体分析入口"""
    price_data = get_price(code)
    price = price_data.get('price', 'N/A') if price_data else 'N/A'
    chg = price_data.get('chg', 0) if price_data else 0

    print('=== 多智能体投研分析: {} ==='.format(name))
    print('代码: {} | 价格: {} | 涨跌: {}%'.format(code, price, chg))
    print()

    findings = {}
    for analyst in ANALYSTS:
        prompt = analyst['prompt'].format(name=name, price=price)
        results = search_tavily(prompt, max_results=3)
        findings[analyst['name']] = [r['title'] for r in results[:3]]

    print('【技术面分析师】')
    for t in findings.get('技术面分析师', []):
        print('  - ' + t[:55])
    print()
    print('【基本面分析师】')
    for t in findings.get('基本面分析师', []):
        print('  - ' + t[:55])
    print()
    print('【资金面分析师】')
    for t in findings.get('资金面分析师', []):
        print('  - ' + t[:55])
    print()
    print('【情绪面分析师】')
    for t in findings.get('情绪面分析师', []):
        print('  - ' + t[:55])
    print()
    print('【综合策略师】')
    for t in findings.get('综合策略师', []):
        print('  - ' + t[:55])

    return {'code': code, 'name': name, 'price': price, 'chg': chg, 'findings': findings}

if __name__ == '__main__':
    analyze_stock('sz300394', '天孚通信')
