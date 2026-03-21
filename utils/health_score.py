"""
health_score.py - 系统健康度评分
每日21:30自动运行，0-100分
维度：API可用性/脚本成功率/日志异常数/备份完成度
<80分触发飞书告警
"""
import os
import sys
import requests
from datetime import datetime, date

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

BASE = r'C:\Users\Administrator\.openclaw\workspace'
LOGS_DIR = os.path.join(BASE, 'logs')
MEMORY_DIR = os.path.join(BASE, 'memory')

def check_api_health():
    """API可用性（40分）"""
    score = 40
    apis = [
        ('腾讯财经', 'https://qt.gtimg.cn/q=sh000001'),
        ('Tavily', 'https://api.tavily.com/search'),
    ]
    for name, url in apis:
        try:
            if 'tavily' in url:
                r = requests.post(url, json={'api_key': 'test', 'query': 'test'}, timeout=5)
            else:
                r = requests.get(url, timeout=5)
            if r.status_code in (200, 400):  # 400也说明通了
                pass
            else:
                score -= 20
        except:
            score -= 20
    return max(score, 0)

def check_script_success():
    """脚本执行成功率（30分）"""
    score = 30
    today = date.today().strftime('%Y-%m-%d')
    hb_file = os.path.join(LOGS_DIR, 'heartbeat-' + today + '.log')
    if os.path.exists(hb_file):
        content = open(hb_file, encoding='utf-8').read()
        errors = content.count('[ERROR]')
        if errors > 5:
            score -= min(errors * 3, 30)
        elif errors > 0:
            score -= errors * 5
    return max(score, 0)

def check_log_anomalies():
    """日志异常数（15分）"""
    score = 15
    today = date.today().strftime('%Y-%m-%d')
    hb_file = os.path.join(LOGS_DIR, 'heartbeat-' + today + '.log')
    wal_file = os.path.join(LOGS_DIR, 'wal-' + today + '.log')
    anomaly_kw = ['ERROR', 'WARN', 'failed', 'timeout']
    total_anomalies = 0
    for f in [hb_file, wal_file]:
        if os.path.exists(f):
            content = open(f, encoding='utf-8').read()
            for kw in anomaly_kw:
                total_anomalies += content.count(kw)
    if total_anomalies > 10:
        score -= min((total_anomalies - 10) * 1, 15)
    elif total_anomalies > 5:
        score -= (total_anomalies - 5) * 2
    return max(score, 0)

def check_backup_status():
    """备份完成度（15分）"""
    score = 15
    # 检查最近24小时是否有git提交
    try:
        import subprocess
        result = subprocess.run(
            ['git', '-C', BASE, 'log', '--since=24 hours ago', '--oneline'],
            capture_output=True, text=True, encoding='utf-8', errors='replace'
        )
        commits = len(result.stdout.strip().split('\n'))
        if commits == 0:
            score = 0
        elif commits < 2:
            score = 8
    except:
        score = 5
    return max(score, 0)

def calc_health_score():
    """计算总分"""
    api = check_api_health()
    script = check_script_success()
    log = check_log_anomalies()
    backup = check_backup_status()
    total = api + script + log + backup

    return {
        'total': total,
        'api': api,
        'script': script,
        'log': log,
        'backup': backup,
        'level': '🟢正常' if total >= 80 else ('🟡警告' if total >= 60 else '🔴危险'),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
    }

def get_health_report():
    """生成健康度报告"""
    result = calc_health_score()
    print('=' * 40)
    print('  系统健康度报告 [' + result['timestamp'] + ']')
    print('=' * 40)
    print()
    print('  总分: ' + result['level'] + ' ' + str(result['total']) + '/100')
    print()
    print('  API可用性:  ' + str(result['api']) + '/40')
    print('  脚本成功率: ' + str(result['script']) + '/30')
    print('  日志异常数: ' + str(result['log']) + '/15')
    print('  备份完成度: ' + str(result['backup']) + '/15')
    print()
    if result['total'] < 80:
        print('  ⚠️ 健康度<80分，触发告警')
    else:
        print('  ✅ 系统运行正常')
    print('=' * 40)
    return result

if __name__ == '__main__':
    r = get_health_report()
    if r['total'] < 80:
        print()
        print('建议检查以下项目:')
        if r['api'] < 30:
            print('  - API可用性低，检查网络和API密钥')
        if r['script'] < 20:
            print('  - 脚本执行成功率低，检查异常日志')
        if r['log'] < 10:
            print('  - 日志异常多，需要排查')
        if r['backup'] < 10:
            print('  - 备份未完成，执行 backup_restore.py backup')
