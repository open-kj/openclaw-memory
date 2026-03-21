"""stock_code_corrector 测试"""
import sys, os, requests, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config.settings import TAVILY_API_KEY
sys.stdout.reconfigure(encoding='utf-8')

KNOWN = {
    '炬芯科技': 'sh688049',
    '炬芯': 'sh688049',
    '源杰科技': 'sh688498',
    '源杰': 'sh688498',
    '芯原股份': 'sh688521',
    '芯原': 'sh688521',
    '北京君正': 'sz300223',
    '长芯博创': 'sz300548',
    '博创科技': 'sz300548',
    '天孚通信': 'sz300394',
}

def verify(code):
    try:
        r = requests.get(f'https://hq.sinajs.cn/list={code}',
            headers={'Referer': 'https://finance.sina.com.cn'}, timeout=8)
        name = r.text.split('"')[1].split(',')[0]
        return {'code': code, 'name': name, 'valid': True}
    except:
        return {'code': code, 'name': '', 'valid': False}

print('=== 股票代码纠错测试 ===')
print()
for name, code in KNOWN.items():
    result = verify(code)
    icon = '✅' if result['valid'] else '❌'
    print(f'{icon} {name} -> {code} = {result["name"]}')
