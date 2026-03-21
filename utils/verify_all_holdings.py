import requests, sys
sys.stdout.reconfigure(encoding='utf-8')

print('=== 持仓全面多平台核实 ===')
print()

stocks = [
    ('sz300394', '天孚通信'),
    ('sz300223', '用户记录=炬芯科技,实际=?'),
    ('sz300548', '博创科技'),
    ('sh688521', '用户记录=芯原股份'),
]

for code, desc in stocks:
    print(f'[{code}] {desc}')
    try:
        r = requests.get(f'https://hq.sinajs.cn/list={code}',
            headers={'Referer': 'https://finance.sina.com.cn'}, timeout=8)
        content = r.text.split('"')[1]
        parts = content.split(',')
        name = parts[0]
        price = parts[3]
        chg = parts[32] if len(parts) > 32 else 'N/A'
        vol = parts[8] if len(parts) > 8 else 'N/A'
        print(f'  新浪: {name} 价={price} 涨跌幅={chg}%')
    except Exception as e:
        print(f'  新浪: 失败 {str(e)[:30]}')

    try:
        r2 = requests.get(f'https://qt.gtimg.cn/q={code}', timeout=8)
        p2 = r2.text.split('~')
        if len(p2) > 32:
            print(f'  腾讯: {p2[1]} 价={p2[3]} ({p2[32]}%)')
    except Exception as e:
        print(f'  腾讯: 失败 {str(e)[:30]}')
    print()

# 查真实炬芯科技
print('=== 真实炬芯科技 ===')
try:
    r3 = requests.get('https://hq.sinajs.cn/list=sh688049',
        headers={'Referer': 'https://finance.sina.com.cn'}, timeout=8)
    c3 = r3.text.split('"')[1]
    print(f'  sh688049 新浪: {c3.split(",")[0]} 价={c3.split(",")[3]}')
except Exception as e:
    print(f'  sh688049: 失败 {str(e)[:30]}')
