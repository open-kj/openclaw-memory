import requests, sys
sys.stdout.reconfigure(encoding='utf-8')

# 验证 sz300223 真实名称
print('=== 多平台验证 sz300223 ===')
# 新浪
r1 = requests.get('https://hq.sinajs.cn/list=sz300223',
    headers={'Referer': 'https://finance.sina.com.cn'}, timeout=8)
content1 = r1.text.split('"')[1]
name1 = content1.split(',')[0]
price1 = content1.split(',')[3]
print(f'新浪: {name1} 价={price1}')

# 腾讯
r2 = requests.get('https://qt.gtimg.cn/q=sz300223', timeout=8)
parts2 = r2.text.split('~')
name2 = parts2[1] if len(parts2) > 1 else 'N/A'
price2 = parts2[3] if len(parts2) > 3 else 'N/A'
print(f'腾讯: {name2} 价={price2}')

# akshare
try:
    import akshare as ak
    df = ak.stock_info_shenzhen_code('sz300223')
    print(f'akshare: {df}')
except Exception as e:
    print(f'akshare: {str(e)[:50]}')

print()
print('=== 多平台验证 sh688521 ===')
r3 = requests.get('https://hq.sinajs.cn/list=sh688521',
    headers={'Referer': 'https://finance.sina.com.cn'}, timeout=8)
content3 = r3.text.split('"')[1]
name3 = content3.split(',')[0]
print(f'新浪 sh688521: {name3}')

print()
print('=== 多平台验证 sh688498 ===')
r4 = requests.get('https://hq.sinajs.cn/list=sh688498',
    headers={'Referer': 'https://finance.sina.com.cn'}, timeout=8)
content4 = r4.text.split('"')[1]
name4 = content4.split(',')[0]
print(f'新浪 sh688498: {name4}')
