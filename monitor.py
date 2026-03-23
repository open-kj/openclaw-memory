"""
盘中监控脚本 - 统一版
最后更新: 2026-03-23
支持: 实时价格 + 止损判断 + 波段预警 + 支撑位警示
"""
import urllib.request
import sys
sys.stdout.reconfigure(encoding='utf-8')

# === 持仓配置 ===
POSITIONS = {
    'sz300394': {
        'name': '天孚通信',
        'qty': 618,
        'cost': 306.99,
        'stop': 291.64,
        'band_low': 305.00,
        'band_high': 320.00,
        'support': 300.00,
    },
    'sh688521': {
        'name': '芯原股份',
        'qty': 1000,
        'cost': 198.88,
        'stop': 188.94,
        'band_low': 195.00,
        'band_high': 208.00,
        'support': 192.00,
    },
    'sz002594': {
        'name': '比亚迪',
        'qty': 3200,
        'cost': 108.89,
        'stop': 103.45,
        'band_low': 105.00,
        'band_high': 115.00,
        'support': None,  # 无特殊支撑
    },
}

def get_price(code):
    url = f'https://qt.gtimg.cn/q={code}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read().decode('gbk')
            parts = data.split('~')
            if len(parts) > 10:
                return float(parts[3]), float(parts[32])  # price, pct
    except:
        return None, None

def check_position(code, cfg, price, pct):
    name = cfg['name']
    stop = cfg['stop']
    stop_dist = (price - stop) / stop * 100
    band_low = cfg['band_low']
    band_high = cfg['band_high']
    support = cfg['support']
    
    alerts = []
    stop_triggered = False
    
    # 止损检查
    if price <= stop:
        alerts.append(f"🔴 止损触发! 现价{price} <= 止损{stop}")
        stop_triggered = True
    
    # 波段高抛
    if price >= band_high and not stop_triggered:
        alerts.append(f"🟠 波段高抛预警: {price} >= {band_high}")
    
    # 波段低吸
    if price <= band_low and not stop_triggered:
        alerts.append(f"🟡 波段低吸预警: {price} <= {band_low}")
    
    # 支撑位警示
    if support and price <= support and not stop_triggered:
        alerts.append(f"⚠️ 支撑位警示: {price} <= {support}")
    
    return alerts, stop_triggered, stop_dist

def main():
    print("=== 盘中监控 ===")
    print(f"时间: 2026-03-23 盘中")
    
    all_stop_triggered = False
    any_alerts = False
    
    for code, cfg in POSITIONS.items():
        price, pct = get_price(code)
        if price is None:
            print(f"{cfg['name']}: 获取失败")
            continue
        
        alerts, stop_triggered, stop_dist = check_position(code, cfg, price, pct)
        
        if stop_triggered:
            all_stop_triggered = True
        
        status = "🔴" if stop_triggered else ("⚠️" if alerts else "✅")
        print(f"\n{status} {cfg['name']} ({code})")
        print(f"   现价: {price} ({pct:+.2f}%)")
        print(f"   止损: {cfg['stop']} (距止损 {stop_dist:+.1f}%)")
        
        for alert in alerts:
            print(f"   {alert}")
            any_alerts = True
    
    if not any_alerts:
        print("\n✅ 所有持仓正常，无触发条件")
    
    return all_stop_triggered

if __name__ == '__main__':
    triggered = main()
    sys.exit(0 if not triggered else 1)
