import urllib.request
stocks='sz300394,sh688521,sz002594,sh688981'
url='https://qt.gtimg.cn/q='+stocks
req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
resp=urllib.request.urlopen(req,timeout=8)
data=resp.read().decode('gbk')
names={'sz300394':'Tianfu','sh688521':'Xinyuan','sz002594':'BYD','sh688981':'SMIC'}
prices={}
for line in data.strip().split('\n'):
    parts=line.split('~')
    if len(parts)>34:
        code=parts[0].split('=')[0].replace('v_','')
        if code in names:
            price=float(parts[3])
            prev=float(parts[4])
            prices[code]=price
            pct=(price-prev)/prev*100
            print(f'{names[code]}: {price:.2f} ({pct:+.2f}%)')
print('')
for code,name,sl in [('sz300394','Tianfu',291.64),('sh688521','Xinyuan',188.94),('sz002594','BYD',103.45),('sh688981','SMIC',93.14)]:
    p=prices.get(code,0)
    if p>0:
        dist=(p-sl)/sl*100
        print(f'{name}: {p:.2f} vs SL {sl:.2f} ({dist:+.1f}%)')
