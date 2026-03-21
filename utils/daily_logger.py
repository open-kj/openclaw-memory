import os
from datetime import datetime

BASE = r'C:\Users\Administrator\.openclaw\workspace'
LOGS_DIR = os.path.join(BASE, 'logs')
STATE_DIR = os.path.join(BASE, 'memory')

os.makedirs(LOGS_DIR, exist_ok=True)

def today():
    return datetime.now().strftime('%Y-%m-%d')

def get_heartbeat_log():
    return os.path.join(LOGS_DIR, 'heartbeat-' + today() + '.log')

def get_state_log():
    return os.path.join(STATE_DIR, 'SESSION-STATE-' + today() + '.md')

def log_heartbeat(action, detail=''):
    ts = datetime.now().strftime('%H:%M:%S')
    line = '[{}] {} | {}\n'.format(ts, action, detail)
    with open(get_heartbeat_log(), 'a', encoding='utf-8') as f:
        f.write(line)
    return line.strip()

def snapshot_state(summary):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M')
    content = '# SESSION-STATE Snapshot - {}\n\n{}\n\n---\n*Auto-generated*\n'.format(ts, summary)
    with open(get_state_log(), 'w', encoding='utf-8') as f:
        f.write(content)
    return get_state_log()

def log_wal(action, detail, value=None):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    parts = ['[' + ts + ']', action, detail]
    if value is not None:
        parts.append('val=' + str(value))
    line = ' | '.join(parts) + '\n'
    wal_path = os.path.join(LOGS_DIR, 'wal-' + today() + '.log')
    with open(wal_path, 'a', encoding='utf-8') as f:
        f.write(line)
    return line.strip()

if __name__ == '__main__':
    log_heartbeat('TEST', 'daily_logger module initialized')
    log_wal('TEST', 'test wal entry', 123)
    snapshot_state('Total asset: 1,016,732 | Holdings: 4 | Cash: 294,992')
    print('OK - heartbeat:', get_heartbeat_log())
    print('OK - state:', get_state_log())
