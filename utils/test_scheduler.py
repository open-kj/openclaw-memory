import sys
sys.path.insert(0, r'C:\Users\Administrator\.openclaw\workspace')
from automation.scheduler import run_scheduler_cycle
result = run_scheduler_cycle()
print('Stop alerts:', [x['name'] for x in result.get('stop_alerts', [])])
print('Market alerts:', result.get('market_alerts', []))
